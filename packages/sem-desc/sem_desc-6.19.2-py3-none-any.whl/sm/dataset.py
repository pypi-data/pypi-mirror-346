from __future__ import annotations

import csv
import random
import shutil
from contextlib import contextmanager
from dataclasses import dataclass
from hashlib import md5
from io import BytesIO, StringIO
from operator import attrgetter
from pathlib import Path
from typing import (
    Generator,
    Generic,
    Literal,
    Optional,
    Protocol,
    Sequence,
    TypeVar,
    Union,
)
from urllib.parse import urlparse
from zipfile import Path as ZipPath
from zipfile import ZipFile

import orjson
import pandas as pd
import serde.csv
import serde.yaml
from ruamel.yaml import YAML
from serde import json
from serde.helper import DEFAULT_ORJSON_OPTS, get_open_fn
from slugify import slugify
from tqdm.auto import tqdm
from typing_extensions import Self

from sm.inputs.prelude import ColumnBasedTable, Context, Link
from sm.misc.funcs import batch
from sm.misc.matrix import Matrix
from sm.namespaces.namespace import Namespace
from sm.outputs import deser_simple_tree_yaml, ser_simple_tree_yaml
from sm.outputs.semantic_model import SemanticModel

T = TypeVar("T", covariant=True)
T1 = TypeVar("T1")


@dataclass
class Example(Generic[T]):
    id: str
    sms: list[SemanticModel]
    table: T

    def replace_table(self, table: T1) -> Example[T1]:
        return Example(id=self.id, sms=self.sms, table=table)


@dataclass
class FullTable:
    table: ColumnBasedTable
    context: Context
    links: Matrix[list[Link]]

    def nrows(self) -> int:
        return self.table.nrows()

    def ncols(self) -> int:
        return self.table.ncols()

    def sample_rows(self, num_rows: int) -> FullTable:
        """Sample a subset of rows"""
        if self.nrows() > num_rows:
            indices = random.sample(range(self.nrows()), num_rows)
            return self.select_rows(indices)
        return self

    def select_rows(self, indices: list[int]) -> FullTable:
        """Select a subset of rows based on a boolean mask"""
        return FullTable(
            table=self.table.select_rows(indices),
            context=self.context,
            links=Matrix([self.links.data[i] for i in indices]),
        )

    def keep_columns(self, columns: list[int], reindex: bool = False) -> FullTable:
        """Keep only the specified columns"""
        if reindex:
            links = Matrix([[row[ci] for ci in columns] for row in self.links.data])
        else:
            # if not re-indexing the columns, we need to keep the original
            # shape (non-selected columns will be empty lists)
            ignore_cols = [
                col.index for col in self.table.columns if col.index not in columns
            ]
            links = self.links.shallow_copy()
            for row in links.data:
                for ci in ignore_cols:
                    row[ci] = []
        return FullTable(
            table=self.table.keep_columns(columns, reindex),
            context=self.context,
            links=links,
        )

    def remove_empty_links(self) -> Self:
        return self.__class__(
            table=self.table,
            context=self.context,
            links=self.links.map(
                lambda links: [link for link in links if link.end > link.start]
            ),
        )

    def to_dict(self):
        return {
            "version": 2,
            "table": self.table.to_dict(),
            "context": self.context.to_dict(),
            "links": [
                [[link.to_dict() for link in cell] for cell in row]
                for row in self.links.data
            ],
        }

    @classmethod
    def from_dict(cls, obj: dict):
        version = obj["version"]
        if not (version == "1.2" or version == "1.1" or version == 2):
            raise ValueError(f"Unknown version: {version}")

        table = ColumnBasedTable.from_dict(obj["table"])
        if "links" in obj:
            links = Matrix(
                [
                    [[Link.from_dict(link) for link in cell] for cell in row]
                    for row in obj["links"]
                ]
            )
        else:
            links = Matrix.default(table.shape(), list)

        return cls(
            table=table,
            context=Context.from_dict(obj["context"]),
            links=links,
        )

    @classmethod
    def from_column_based_table(cls, table: ColumnBasedTable) -> FullTable:
        context = Context()
        links = Matrix.default(table.shape(), list)
        return cls(table=table, context=context, links=links)


@dataclass
class Dataset:
    location: Path

    @contextmanager
    def _open(self) -> Generator[Union[ZipPath, Path], None, None]:
        if self.is_zip_file():
            # it is a zip file
            with ZipFile(self.location, mode="r") as zf:
                root = ZipPath(zf)
                if self.description_dir(root).exists():
                    yield root
                else:
                    subdirs = list(root.iterdir())
                    if len(subdirs) == 1 and self.description_dir(subdirs[0]).exists():
                        yield subdirs[0]
                    else:
                        raise ValueError("Invalid dataset format")
        else:
            yield self.location

    def description_dir(self, root: Union[Path, ZipPath]) -> Union[Path, ZipPath]:
        return root / "descriptions"

    def table_dir(self, root: Union[Path, ZipPath]) -> Union[Path, ZipPath]:
        return root / "tables"

    def is_zip_file(self):
        return self.location.name.endswith(".zip")

    def load(self, verbose: bool = False) -> list[Example[FullTable]]:
        """Load dataset from a folder or a single zip file. Assuming the following structure:

        descriptions (containing semantic descriptions of tables)
        ├── <table_fs_id>
        │   ├── version.01[.json|.yml|.st.yml]
        │   ├── version.02[.json|.yml|.st.yml]
        │   └── ...
            or
        ├── <table_fs_id>[.json|.yml|.st.yml]
        ├── ...
        tables (containing list of tables, the type of table depends on )
        ├── <table_fs_id>[.json|.csv|.xlsx][.gz|.bz2|.lz4]
        ├── ...

        We also support compressing formats such as .zip.
        descriptions
        ├── part-<num>.zip (no nested version folders)
        │   ├── <table_fs_id>[.json|.yml|.st.yml]
        |   |   ...
        tables
        ├── part-<num>.zip
        │   ├── <table_fs_id>[.json|.csv|.xlsx]
        |   |   ...

        The description can be specified in either json or yaml format. For more information on
        how the semantic models are deserialized from the format, checkout the corresponding
        deserialization functions.

        Args:
            data_dir:

        Returns:
        """
        examples = []
        with self._open() as root:
            descdir = self.description_dir(root)
            tabledir = self.table_dir(root)

            for infile in tqdm(
                sorted(tabledir.iterdir(), key=attrgetter("name")), disable=not verbose
            ):
                suffixes = Path(infile.name).suffixes
                if infile.name.startswith(".") or len(suffixes) == 0:
                    continue

                if suffixes[-1] != ".zip":
                    example_id = infile.name[: -sum(len(x) for x in suffixes)]
                    table = self._deser_table(
                        example_id, infile.read_bytes(), suffixes[0]
                    )

                    if descdir.exists():
                        if (descdir / example_id).exists():
                            desc_file = max(
                                (descdir / example_id).iterdir(),
                                key=lambda file: int(file.name.split(".")[1]),
                            )
                            assert desc_file is not None
                        else:
                            desc_file = descdir / f"{example_id}.json"
                            if not desc_file.exists():
                                desc_file = descdir / f"{example_id}.yml"
                                if not desc_file.exists():
                                    desc_file = descdir / f"{example_id}.st.yml"
                            assert (
                                desc_file.exists()
                            ), f"Description file not found for {example_id}"

                        sms = self._deser_sm(
                            table.table,
                            desc_file.read_bytes(),
                            "".join(desc_file.suffixes),
                        )
                    else:
                        sms = []

                    examples.append(
                        Example(id=table.table.table_id, sms=sms, table=table)
                    )
                else:
                    assert (
                        infile.name.endswith(".zip")
                        and isinstance(infile, Path)
                        and isinstance(descdir, Path)
                        and not self.is_zip_file()
                    ), "Must not be a zip file"
                    part: dict[str, FullTable] = {}
                    with ZipFile(infile, mode="r") as zf:
                        for file in zf.infolist():
                            if not file.filename.endswith(".json"):
                                continue

                            table_id = Path(file.filename).stem
                            with zf.open(file, mode="r") as f:
                                table = self._deser_table(
                                    table_id, f.read(), Path(file.filename).suffixes[0]
                                )
                            part[table_id] = table

                    if descdir.exists():
                        lst = []
                        with ZipFile(descdir / infile.name, mode="r") as zf:
                            for file in zf.infolist():
                                table_id = Path(file.filename).stem
                                if table_id not in part:
                                    continue

                                with zf.open(file, mode="r") as f:
                                    sms = self._deser_sm(
                                        part[table_id].table,
                                        f.read(),
                                        "." + "".join(file.filename.split(".")[1:]),
                                    )
                                    lst.append(
                                        Example(
                                            id=part[table_id].table.table_id,
                                            sms=sms,
                                            table=part[table_id],
                                        )
                                    )
                    else:
                        lst = [
                            Example(id=table.table.table_id, sms=[], table=table)
                            for table in part.values()
                        ]
                    assert len(lst) == len(part)
                    examples.extend(lst)

            return examples

    def save(
        self,
        examples: list[Example[FullTable]],
        individual_table_compressed: Optional[Literal["gz", "bz2", "lz4"]] = None,
        batch_compressed: bool = False,
        batch_size: int = 100,
        sm_fmt: Literal["json", "simple-tree"] = "json",
        sm_fmt_indent: Literal[0, 2] = 0,
        table_fmt: Literal["json", "txt"] = "json",
        table_fmt_indent: Literal[0, 2] = 0,
        clean_previous_data: bool = True,
        ns: Optional[Namespace] = None,
        multi_desc_version: bool = False,
    ):
        """Save dataset to a folder, single, or multiple zip files. Assuming the following structure:

        Args:
            multiversion: if True, we create a description folder for each example id so that we can have multiple versioned files
        """
        if self.is_zip_file():
            with ZipFile(self.location, "w") as root:
                assert isinstance(root, ZipFile)
                for e in examples:
                    ename = get_friendly_fs_id(e.table.table.table_id)
                    root.writestr(
                        "descriptions/" + ename + f".{fmt_to_ext(sm_fmt)}",
                        data=self._ser_sm(
                            e.sms, e.table.table, sm_fmt, sm_fmt_indent, ns
                        ),
                        # data=orjson.dumps([sm.to_dict() for sm in e.sms]),
                    )
                    root.writestr(
                        "tables/" + ename + f".{fmt_to_ext(table_fmt)}",
                        data=self._ser_table(e.table, table_fmt, table_fmt_indent),
                    )
            return

        descdir = self.description_dir(self.location)
        tabledir = self.table_dir(self.location)
        assert (
            not self.is_zip_file()
            and isinstance(descdir, Path)
            and isinstance(tabledir, Path)
        )

        if descdir.exists() and clean_previous_data:
            shutil.rmtree(descdir)
        descdir.mkdir(parents=True, exist_ok=True)

        if tabledir.exists() and clean_previous_data:
            shutil.rmtree(tabledir)
        tabledir.mkdir(parents=True, exist_ok=True)

        if batch_compressed:
            for i, bexamples in enumerate(batch(batch_size, examples)):
                bexamples: list[Example[FullTable]]
                filename = f"part-{i:04d}.zip"
                with ZipFile(descdir / filename, "w") as dzf, ZipFile(
                    tabledir / filename, "w"
                ) as tzf:
                    for e in bexamples:
                        ename = get_friendly_fs_id(e.table.table.table_id)
                        dzf.writestr(
                            ename + f".{fmt_to_ext(sm_fmt)}",
                            data=self._ser_sm(
                                e.sms, e.table.table, sm_fmt, sm_fmt_indent, ns
                            ),
                        )
                        tzf.writestr(
                            ename + f".{fmt_to_ext(table_fmt)}",
                            data=self._ser_table(e.table, table_fmt, table_fmt_indent),
                        )
        else:
            for e in examples:
                filename = get_friendly_fs_id(e.table.table.table_id)

                if multi_desc_version:
                    desc_outfile = (
                        descdir / filename / f"version.01.{fmt_to_ext(sm_fmt)}"
                    )
                    desc_outfile.parent.mkdir(parents=True, exist_ok=True)
                else:

                    desc_outfile = descdir / f"{filename}.{fmt_to_ext(sm_fmt)}"
                desc_outfile.write_bytes(
                    self._ser_sm(e.sms, e.table.table, sm_fmt, sm_fmt_indent, ns)
                )

                table_outfile = tabledir / (
                    filename + f".{fmt_to_ext(table_fmt)}.{individual_table_compressed}"
                    if individual_table_compressed is not None
                    else filename + f".{fmt_to_ext(table_fmt)}"
                )
                with get_open_fn(table_outfile)(table_outfile, "wb") as f:
                    f.write(self._ser_table(e.table, table_fmt, table_fmt_indent))

    @staticmethod
    def _deser_table(table_id: str, data: bytes, ext: str) -> FullTable:
        if ext == ".json":
            return FullTable.from_dict(orjson.loads(data))
        if ext == ".csv":
            column_based_table = ColumnBasedTable.from_dataframe(
                pd.read_csv(BytesIO(data)),
                table_id=table_id,
            )
            return FullTable(
                table=column_based_table,
                context=Context(),
                links=Matrix.default(column_based_table.shape(), list),
            )
        if ext == ".xlsx":
            column_based_table = ColumnBasedTable.from_dataframe(
                pd.read_excel(BytesIO(data)),
                table_id=table_id,
            )
            return FullTable(
                table=column_based_table,
                context=Context(),
                links=Matrix.default(column_based_table.shape(), list),
            )
        if ext == ".txt":
            part1_csv, part2_json = data.split(b"\n" + b"-" * 80 + b"\n\n")
            column_based_table = ColumnBasedTable.from_dataframe(
                pd.read_csv(BytesIO(part1_csv)),
                table_id=table_id,
            )
            obj = orjson.loads(part2_json)
            return FullTable(
                table=column_based_table,
                context=Context.from_dict(obj["context"]),
                links=Matrix(
                    [
                        [[Link.from_dict(link) for link in cell] for cell in row]
                        for row in obj["links"]
                    ]
                ),
            )

        raise ValueError(f"Unknown file type: {ext}")

    @staticmethod
    def _ser_table(
        table: FullTable,
        table_fmt: Literal["json", "txt"] = "json",
        table_fmt_indent: Literal[0, 2] = 0,
    ):
        if table_fmt == "json":
            if table_fmt_indent > 0:
                orjson_opts = DEFAULT_ORJSON_OPTS | orjson.OPT_INDENT_2
            else:
                orjson_opts = DEFAULT_ORJSON_OPTS

            return orjson.dumps(table.to_dict(), option=orjson_opts)

        if table_fmt == "txt":
            out = StringIO()
            nrows, ncols = table.table.shape()

            writer = csv.writer(
                out, delimiter=",", quoting=csv.QUOTE_MINIMAL, lineterminator="\n"
            )
            writer.writerow([c.name for c in table.table.columns])
            for ri in range(nrows):
                writer.writerow(
                    [table.table.columns[ci].values[ri] for ci in range(ncols)]
                )

            out.write("\n" + "-" * 80 + "\n\n")
            if table_fmt_indent > 0:
                orjson_opts = DEFAULT_ORJSON_OPTS | orjson.OPT_INDENT_2
            else:
                orjson_opts = DEFAULT_ORJSON_OPTS

            out.write(
                orjson.dumps(
                    {
                        "context": table.context.to_dict(),
                        "links": [
                            [[link.to_dict() for link in cell] for cell in row]
                            for row in table.links.data
                        ],
                    },
                    option=orjson_opts,
                ).decode()
            )
            return out.getvalue().encode()

        raise ValueError(f"Unsupported format: {table_fmt}")

    @staticmethod
    def _deser_sm(table: ColumnBasedTable, data: bytes, ext: str):
        if ext.endswith(".json"):
            return [SemanticModel.from_dict(sm) for sm in orjson.loads(data)]
        if ext.endswith(".st.yml"):
            return [deser_simple_tree_yaml(table, BytesIO(data))]
        if ext.endswith(".yml"):
            yaml = YAML()
            raw = yaml.load(BytesIO(data))
            ns = Namespace.from_prefix2ns(raw["prefixes"])
            sms = [SemanticModel.from_yaml_dict(sm, ns) for sm in raw["models"]]
            return sms
        raise ValueError(f"Unknown file type: {ext}")

    @staticmethod
    def _ser_sm(
        sm: Union[SemanticModel, Sequence[SemanticModel]],
        table: ColumnBasedTable,
        fmt: Literal["json", "simple-tree"],
        fmt_indent: Literal[0, 2] = 0,
        ns: Optional[Namespace] = None,
    ):
        if fmt == "json":
            if isinstance(sm, SemanticModel):
                sm = [sm]
            return orjson.dumps(
                [x.to_dict() for x in sm],
                option=orjson.OPT_INDENT_2 if fmt_indent > 0 else None,
            )
        elif fmt == "simple-tree":
            if isinstance(sm, Sequence):
                assert len(sm) == 1
                sm = sm[0]

            assert ns is not None
            file = BytesIO()

            ser_simple_tree_yaml(table, sm, ns, file)
            return file.getvalue()
        else:
            raise ValueError(f"Unsupported format: {fmt}")


def get_friendly_fs_id(id: str) -> str:
    if id.startswith("http://") or id.startswith("https://"):
        if id.find("dbpedia.org") != -1:
            return (
                slugify(
                    urlparse(id).path.replace("/resource/", "").replace("/", "_")
                ).replace("-", "_")
                + "_"
                + md5(id.encode()).hexdigest()
            )

        if id.find("wikipedia.org") != -1:
            return (
                slugify(
                    urlparse(id).path.replace("/wiki/", "").replace("/", "_")
                ).replace("-", "_")
                + "_"
                + md5(id.encode()).hexdigest()
            )

        raise NotImplementedError()
    return slugify(id.replace("/", "_"), lowercase=False).replace("-", "_")


def fmt_to_ext(fmt: Literal["json", "txt", "simple-tree"]) -> str:
    if fmt == "simple-tree":
        return "st.yml"
    return fmt


class SampleableTable(Protocol):
    def nrows(self) -> int: ...

    def select_rows(self, indices: list[int]) -> Self: ...


ST = TypeVar("ST", bound=SampleableTable, covariant=True)


def sample_table_data(
    examples: Sequence[Example[ST]], n_rows: int, seed: Optional[int] = None
) -> Sequence[Example[ST]]:
    """Sample data from each table in examples.

    Args:
        examples: list of examples
        n_rows: number of rows to sample per table
        seed: random seed
    """
    rng = random.Random(seed)
    new_exs = []
    for ex in examples:
        tbl_nrows = ex.table.nrows()
        if tbl_nrows <= n_rows:
            new_exs.append(ex)
        else:
            indices = rng.sample(range(tbl_nrows), n_rows)
            new_exs.append(
                Example(id=ex.id, sms=ex.sms, table=ex.table.select_rows(indices))
            )

    return new_exs
