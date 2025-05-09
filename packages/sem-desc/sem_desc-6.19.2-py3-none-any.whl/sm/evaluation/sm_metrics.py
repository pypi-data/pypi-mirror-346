#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import os
from dataclasses import dataclass
from itertools import chain, permutations
from typing import Callable, Dict, Generator, List, Optional, Sequence, Set, Tuple

from loguru import logger
from pyrsistent import PVector, pvector
from sm.evaluation.utils import PrecisionRecallF1
from sm.outputs.semantic_model import ClassNode, DataNode, LiteralNode, SemanticModel

"""
Compute precision, recall and f1 score of the semantic model according to Mohsen paper.

Convention: x' and x are nodes in predicted model and gold model, respectively.
"""


class PermutationExplosion(Exception):
    pass


class Node(object):
    __slots__ = ("id", "label", "incoming_links", "outgoing_links")

    def __init__(self, id: int, label: str) -> None:
        self.id: int = id
        self.label: str = label
        self.incoming_links: List[Link] = []
        self.outgoing_links: List[Link] = []

    @staticmethod
    def add_incoming_link(node: "Node", link: "Link"):
        node.incoming_links.append(link)
        link.target = node

    @staticmethod
    def add_outgoing_link(node: "Node", link: "Link"):
        node.outgoing_links.append(link)
        link.source = node

    def __str__(self):
        return "Node(id=%s, label=%s)" % (self.id, self.label)


@dataclass(frozen=True, eq=True)
class NodeTriple:
    __slots__ = ("source_id", "link_label", "target_id")
    source_id: int
    link_label: str
    target_id: int

    def __setstate__(self, state):
        assert state[0] is None and isinstance(state[1], dict)
        for slot, value in state[1].items():
            object.__setattr__(self, slot, value)


class Link(object):
    __slots__ = ("id", "label", "source", "source_id", "target", "target_id")

    def __init__(self, id: int, label: str, source: Node, target: Node) -> None:
        self.id: int = id
        self.label: str = label
        self.source = source
        self.source_id: int = source.id
        self.target = target
        self.target_id: int = target.id


class LabelGroup(object):
    """Represent a group of nodes that have same label"""

    __slots__ = ("nodes", "node_triples", "size")

    def __init__(self, nodes: List[Node]) -> None:
        self.nodes: List[Node] = nodes
        self.node_triples: Set[NodeTriple] = {
            NodeTriple(link.source_id, link.label, link.target_id)
            for node in self.nodes
            for link in chain(node.incoming_links, node.outgoing_links)
        }
        self.size: int = len(nodes)

    def __repr__(self):
        return "(#nodes=%d)" % (len(self.nodes))

    # noinspection PyUnusedLocal
    @staticmethod
    def group_by_structures(group: "LabelGroup", pred_group: "LabelGroup"):
        """
        A structure of a node is defined by its links, or we can treat it as a set of triple.
        Unbounded nodes should be assumed to be different, therefore a node have unbounded nodes will have
        it own structure group.
        We need not consider triple that are impossible to map to node in pred_group. This trick will improve
        the performance.
        """
        # TODO: implement it
        return [StructureGroup([n]) for n in group.nodes]


class StructureGroup(object):
    """Represent a group of nodes that have same structure"""

    __slots__ = ("nodes", "size")

    def __init__(self, nodes: List[Node]) -> None:
        self.nodes: List[Node] = nodes
        self.size: int = len(nodes)


class PairLabelGroup(object):
    __slots__ = ("X", "X_prime", "label")

    def __init__(self, label: str, X: LabelGroup, X_prime: LabelGroup) -> None:
        self.label = label
        self.X: LabelGroup = X
        self.X_prime: LabelGroup = X_prime

    def __repr__(self):
        return "(label=%s, X=%s, X_prime=%s)" % (self.label, self.X, self.X_prime)


class DependentGroups(object):
    """Represent a list of groups of nodes that are dependent on each other"""

    __slots__ = ("pair_groups", "X_triples", "X_prime_triples", "x_pairs")

    def __init__(self, pair_groups: List[PairLabelGroup]):
        self.pair_groups: List[PairLabelGroup] = pair_groups
        self.X_triples: Set[NodeTriple] = set()
        self.X_prime_triples: Set[NodeTriple] = set()

        for pair in pair_groups:
            self.X_triples = self.X_triples.union(pair.X.node_triples)
            self.X_prime_triples = self.X_prime_triples.union(pair.X_prime.node_triples)

        # a mapping from (source id, target id) to list of predicates
        # use this for computing if we want to take into account the ancestor/descendant in the predicates
        self.x_pairs = {}
        for triple in self.X_triples:
            if (triple.source_id, triple.target_id) not in self.x_pairs:
                self.x_pairs[triple.source_id, triple.target_id] = []
            self.x_pairs[triple.source_id, triple.target_id].append(triple.link_label)

    def get_n_permutations(self):
        n_permutation = 1
        for pair_group in self.pair_groups:
            n = max(pair_group.X.size, pair_group.X_prime.size)
            m = min(pair_group.X.size, pair_group.X_prime.size)
            n_permutation *= math.factorial(n) / math.factorial(n - m)

        return n_permutation


class PartialBijection(object):
    """A bijection defined a one-one mapping from x' => x.
    A node is mapped to None means that it doesn't have a correspondent node in the other model.
    """

    __slots__ = ("prime2x", "x2prime")

    def __init__(self) -> None:
        # a map from x' => x (pred_sm to gold_sm)
        self.prime2x: Dict[int, Optional[int]] = {}
        # map from x => x'
        self.x2prime: Dict[int, Optional[int]] = {}

    @staticmethod
    def construct_from_mapping(
        mapping: Sequence[Tuple[Optional[int], Optional[int]]]
    ) -> "PartialBijection":
        """
        :param mapping: a list of map from x' => x
        """
        self = PartialBijection()
        self.prime2x = {x_prime: x for x_prime, x in mapping if x_prime is not None}
        self.x2prime = {x: x_prime for x_prime, x in mapping if x is not None}
        return self

    def extends(self, bijection: "PartialBijection") -> "PartialBijection":
        another = PartialBijection()
        another.prime2x = dict(self.prime2x)
        another.prime2x.update(bijection.prime2x)
        another.x2prime = dict(self.x2prime)
        another.x2prime.update(bijection.x2prime)
        return another

    def extends_(self, bijection: "PartialBijection") -> None:
        self.prime2x.update(bijection.prime2x)
        self.x2prime.update(bijection.x2prime)

    def is_gold_node_bounded(self, node_id: int) -> bool:
        return node_id in self.x2prime

    def is_pred_node_bounded(self, node_id: int) -> bool:
        return node_id in self.prime2x


class IterGroupMapsUsingGroupingArgs(object):
    __slots__ = ("node_index", "bijection", "G_sizes")

    def __init__(self, node_index: int, bijection: PVector, G_sizes) -> None:
        self.node_index: int = node_index
        self.bijection: PVector = bijection
        self.G_sizes = G_sizes


class IterGroupMapsGeneralApproachArgs(object):
    __slots__ = ("node_index", "bijection")

    def __init__(self, node_index: int, bijection: PVector) -> None:
        self.node_index: int = node_index
        self.bijection: PVector = bijection


class FindBestMapArgs(object):
    __slots__ = ("group_index", "bijection")

    def __init__(self, group_index: int, bijection: PartialBijection) -> None:
        self.group_index: int = group_index
        self.bijection = bijection


class ScoringFn:
    # noinspection PyMethodMayBeStatic
    def get_match_score(self, pred_predicate: str, target_predicate: str) -> float:
        return int(pred_predicate == target_predicate)


@dataclass
class SmPrecisionRecallF1Output(PrecisionRecallF1):
    bijection: PartialBijection
    n_corrects: float  # float as we allow for partial correctness
    n_examples: int
    n_predictions: int
    gold_triples: Set[NodeTriple]
    pred_triples: Set[NodeTriple]


def find_best_map(
    dependent_group: DependentGroups, bijection: PartialBijection, scoring_fn: ScoringFn
) -> PartialBijection:
    terminate_index: int = len(dependent_group.pair_groups)
    # This code find the size of this
    # array: sum([min(gold_group.size, pred_group.size) for gold_group, pred_group in dependent_group.groups])
    call_stack = [FindBestMapArgs(group_index=0, bijection=bijection)]
    n_called = 0

    best_map = None
    best_score = -1

    while True:
        call_args = call_stack.pop()
        n_called += 1
        if call_args.group_index == terminate_index:
            # it is terminated, calculate score
            score = eval_score(dependent_group, call_args.bijection, scoring_fn)
            if score > best_score:
                best_score = score
                best_map = call_args.bijection
        else:
            pair_group = dependent_group.pair_groups[call_args.group_index]
            X, X_prime = pair_group.X, pair_group.X_prime
            for group_map in iter_group_maps(X, X_prime, call_args.bijection):
                bijection = PartialBijection.construct_from_mapping(group_map)

                call_stack.append(
                    FindBestMapArgs(
                        group_index=call_args.group_index + 1,
                        bijection=call_args.bijection.extends(bijection),
                    )
                )

        if len(call_stack) == 0:
            break

    return best_map  # type: ignore


def get_unbounded_nodes(
    X: LabelGroup, is_bounded_func: Callable[[int], bool]
) -> List[Node]:
    """Get nodes of a label group which have not been bounded by a bijection"""
    unbounded_nodes = []

    for x in X.nodes:
        for link in x.incoming_links:
            if not is_bounded_func(link.source_id):
                unbounded_nodes.append(link.source)

        for link in x.outgoing_links:
            if not is_bounded_func(link.target_id):
                unbounded_nodes.append(link.target)

    return unbounded_nodes


def get_common_unbounded_nodes(
    X: LabelGroup, X_prime: LabelGroup, bijection: PartialBijection
) -> Set[str]:
    """Finding unbounded nodes in X and X_prime that have same labels"""
    unbounded_X = get_unbounded_nodes(X, bijection.is_gold_node_bounded)
    unbounded_X_prime = get_unbounded_nodes(X_prime, bijection.is_pred_node_bounded)

    labeled_unbounded_X = {}
    labeled_unbounded_X_prime = {}
    for x in unbounded_X:
        if x.label not in labeled_unbounded_X:
            labeled_unbounded_X[x.label] = []
        labeled_unbounded_X[x.label].append(x)

    for x in unbounded_X_prime:
        if x.label not in labeled_unbounded_X_prime:
            labeled_unbounded_X_prime[x.label] = []
        labeled_unbounded_X_prime[x.label].append(x)

    common_unbounded_nodes = set(labeled_unbounded_X.keys()).intersection(
        labeled_unbounded_X_prime.keys()
    )
    return common_unbounded_nodes


def group_dependent_elements(dependency_map: List[List[int]]) -> List[int]:
    # algorithm to merge the dependencies
    # input:
    #   - dependency_map: [<element_index, ...>, ...] list of dependencies where element at ith position is list of index of elements
    #           that element at ith position depends upon.
    # output:
    #   - dependency_groups: [<group_id>, ...] list of group id, where element at ith position is group id that element belongs to
    dependency_groups: List[int] = [-1 for _ in range(len(dependency_map))]
    invert_dependency_groups = {}

    for i, g in enumerate(dependency_map):
        dependent_elements = g + [i]
        groups = {dependency_groups[j] for j in dependent_elements}
        valid_groups = groups.difference([-1])
        if len(valid_groups) == 0:
            group_id = len(invert_dependency_groups)
            invert_dependency_groups[group_id] = set()
        else:
            group_id = next(iter(valid_groups))

        if -1 in groups:
            # map unbounded elements to group has group_id
            for j in dependent_elements:
                if dependency_groups[j] == -1:
                    dependency_groups[j] = group_id
                    invert_dependency_groups[group_id].add(j)

        for another_group_id in valid_groups.difference([group_id]):
            for j in invert_dependency_groups[another_group_id]:
                dependency_groups[j] = group_id
                invert_dependency_groups[group_id].add(j)

    return dependency_groups


def split_by_dependency(
    map_groups: List[PairLabelGroup], bijection: PartialBijection
) -> List[DependentGroups]:
    """This method takes a list of groups (X, X') and group them based on their dependencies.
    D = {D1, D2, …} s.t for all Di, Dj, (Xi, Xi') in Di, (Xj, Xj’) in Dj, they are independent

    Two groups of nodes are dependent when at least one unbounded nodes in a group is a label of other group.
    For example, "actor_appellation" has link to "type", so group "actor_appellation" depends on group "type"
    """
    group_label2idx = {map_group.label: i for i, map_group in enumerate(map_groups)}

    # build group dependencies
    dependency_map = [[] for _ in range(len(map_groups))]
    for i, map_group in enumerate(map_groups):
        X, X_prime = map_group.X, map_group.X_prime
        common_labels = get_common_unbounded_nodes(X, X_prime, bijection)

        for common_label in common_labels:
            group_id = group_label2idx[common_label]
            dependency_map[i].append(group_id)

    dependency_groups = group_dependent_elements(dependency_map)
    dependency_pair_groups: Dict[int, List[PairLabelGroup]] = {}
    dependency_map_groups: List[DependentGroups] = []

    for i, map_group in enumerate(map_groups):
        if dependency_groups[i] not in dependency_pair_groups:
            dependency_pair_groups[dependency_groups[i]] = []
        dependency_pair_groups[dependency_groups[i]].append(map_group)

    for pair_groups in dependency_pair_groups.values():
        dependency_map_groups.append(DependentGroups(pair_groups))

    return dependency_map_groups


def iter_group_maps(
    X: LabelGroup, X_prime: LabelGroup, bijection: PartialBijection
) -> Generator[List[Tuple[int, Optional[int]]], None, None]:
    """Generate all mapping between X and X_prime. Return a list of tuple of (x_prime, x)"""
    if X.size < X_prime.size:
        return iter_group_maps_general_approach(X, X_prime)
    else:
        G = LabelGroup.group_by_structures(X, X_prime)
        return iter_group_maps_using_grouping(X_prime, G)


def iter_group_maps_general_approach(
    X: LabelGroup, X_prime: LabelGroup
) -> Generator[List[Tuple[int, Optional[int]]], None, None]:
    """
    Generate all mapping from X to X_prime
    NOTE: |X| < |X_prime|

    Return mapping from (x_prime to x)
    """
    mapping_mold: List[Optional[int]] = [None for _ in range(X_prime.size)]

    for perm in permutations(range(X_prime.size), X.size):
        mapping: List[Tuple[int, Optional[int]]] = []
        for i, j in enumerate(perm):
            mapping_mold[j] = X.nodes[i].id

        for i in range(X_prime.size):
            mapping.append((X_prime.nodes[i].id, mapping_mold[i]))
            mapping_mold[i] = None
        yield mapping


def iter_group_maps_using_grouping(
    X_prime: LabelGroup, G: List[StructureGroup]
) -> Generator[List[Tuple[int, Optional[int]]], None, None]:
    """
    Generate all mapping from X_prime to G (nodes in X grouped by their structures)
    NOTE: |X_prime| <= |X|

    Return mapping from (x_prime to x)
    """
    G_sizes = pvector((g.size for g in G))
    bijection: PVector = pvector([-1 for _ in range(X_prime.size)])
    terminate_index: int = X_prime.size

    call_stack: List[IterGroupMapsUsingGroupingArgs] = [
        IterGroupMapsUsingGroupingArgs(
            node_index=0, bijection=bijection, G_sizes=G_sizes
        )
    ]

    while True:
        call_args = call_stack.pop()

        if call_args.node_index == terminate_index:
            # convert bijection into a final mapping
            G_numerator = [0 for _ in range(len(G))]
            bijection = call_args.bijection
            mapping = []
            for i in range(len(bijection)):
                x_prime = X_prime.nodes[i].id
                x = G[bijection[i]].nodes[G_numerator[bijection[i]]].id

                G_numerator[bijection[i]] += 1
                mapping.append((x_prime, x))

            yield mapping
        else:
            for i, G_i in enumerate(G):
                if call_args.G_sizes[i] == 0:
                    continue

                bijection = call_args.bijection.set(call_args.node_index, i)
                G_sizes = call_args.G_sizes.set(i, call_args.G_sizes[i] - 1)

                call_stack.append(
                    IterGroupMapsUsingGroupingArgs(
                        node_index=call_args.node_index + 1,
                        bijection=bijection,
                        G_sizes=G_sizes,
                    )
                )

        if len(call_stack) == 0:
            break


def prepare_args(
    gold_sm: "SemanticModel", pred_sm: "SemanticModel"
) -> List[PairLabelGroup]:
    """Prepare data for evaluation

    + data_node_mode = 0, mean we don't touch anything (note that the label of data_node must be unique)
    + data_node_mode = 1, mean we ignore label of data node (convert it to DATA_NODE, DATA_NODE2 if there are duplication columns)
    + data_node_mode = 2, mean we ignore data node
    """

    def convert_graph(graph: "SemanticModel"):
        node_index: Dict[int, Node] = {}

        for v in graph.iter_nodes():
            if isinstance(v, ClassNode):
                label = v.abs_uri
            elif isinstance(v, DataNode):
                label = f"attr-{v.col_index:02d}"
            else:
                assert isinstance(v, LiteralNode)
                label = v.value
            node_index[v.id] = Node(v.id, label)

        for i, e in enumerate(graph.iter_edges()):
            link = Link(i, e.abs_uri, node_index[e.source], node_index[e.target])
            Node.add_outgoing_link(node_index[e.source], link)
            Node.add_incoming_link(node_index[e.target], link)

        return node_index

    label2nodes = {}
    gold_id2node = convert_graph(gold_sm)
    pred_id2node = convert_graph(pred_sm)

    for node in gold_id2node.values():
        if node.label not in label2nodes:
            label2nodes[node.label] = ([], [])
        label2nodes[node.label][0].append(node)
    for node in pred_id2node.values():
        if node.label not in label2nodes:
            label2nodes[node.label] = ([], [])
        label2nodes[node.label][1].append(node)

    return [
        PairLabelGroup(label, LabelGroup(g[0]), LabelGroup(g[1]))
        for label, g in label2nodes.items()
    ]


def eval_score(
    dependent_groups: DependentGroups,
    bijection: PartialBijection,
    scoring_fn: ScoringFn,
) -> float:
    x_pairs = dependent_groups.x_pairs
    mapped_xprime_triples = {}
    for triple in dependent_groups.X_prime_triples:
        if (
            triple.source_id not in bijection.prime2x
            or triple.target_id not in bijection.prime2x
        ):
            continue

        s = bijection.prime2x[triple.source_id]
        o = bijection.prime2x[triple.target_id]
        if (s, o) in x_pairs:
            if (s, o) not in mapped_xprime_triples:
                mapped_xprime_triples[(s, o)] = []
            mapped_xprime_triples[(s, o)].append(triple.link_label)

    score = 0.0
    for so, edges in mapped_xprime_triples.items():
        if len(x_pairs[so]) == 1:
            gold_edge = x_pairs[so][0]
            # if save some computation time
            if len(edges) > 1:
                edge = max(
                    edges, key=lambda e: scoring_fn.get_match_score(e, gold_edge)
                )
            else:
                edge = edges[0]
            score += scoring_fn.get_match_score(edge, gold_edge)
        else:
            free_prime_edge_index = set(range(len(edges)))
            for gold_edge in x_pairs[so]:
                edge_idx = max(
                    free_prime_edge_index,
                    key=lambda idx: scoring_fn.get_match_score(edges[idx], gold_edge),
                )
                free_prime_edge_index.remove(edge_idx)
                score += scoring_fn.get_match_score(edges[edge_idx], gold_edge)

    return score


def precision_recall_f1(
    gold_sm: "SemanticModel",
    pred_sm: "SemanticModel",
    scoring_fn: Optional[ScoringFn] = None,
    debug_dir: Optional[str] = None,
    soft_permutation_threshold: int = 50000,
    hard_permutation_threshold: int = 1000000,
) -> SmPrecisionRecallF1Output:
    if scoring_fn is None:
        scoring_fn = ScoringFn()
    pair_groups: List[PairLabelGroup] = prepare_args(gold_sm, pred_sm)

    mapping = []
    map_groups: List[PairLabelGroup] = []
    for pair in pair_groups:
        X, X_prime = pair.X, pair.X_prime

        if max(X.size, X_prime.size) == 1:
            x_prime = None if X_prime.size == 0 else X_prime.nodes[0].id
            x = None if X.size == 0 else X.nodes[0].id
            mapping.append((x_prime, x))
        else:
            map_groups.append(pair)

    bijection = PartialBijection.construct_from_mapping(mapping)
    list_of_dependent_groups: List[DependentGroups] = split_by_dependency(
        map_groups, bijection
    )

    best_bijections = []
    n_permutations = sum(
        [
            dependent_groups.get_n_permutations()
            for dependent_groups in list_of_dependent_groups
        ]
    )

    # TODO: remove debugging code or change to logging
    if n_permutations > soft_permutation_threshold:
        logger.info("Number of permutation is: {}", n_permutations)

    if n_permutations > hard_permutation_threshold:
        if debug_dir is not None:
            gold_sm.draw(os.path.join(debug_dir, "gold.png"))
            pred_sm.draw(os.path.join(debug_dir, "pred.png"))
        logger.error(
            "Permutation explosion: got {} combinations from {} pair groups",
            n_permutations,
            len(list_of_dependent_groups),
        )
        for dependent_groups in list_of_dependent_groups:
            logger.info("- {}", dependent_groups.pair_groups)
        raise PermutationExplosion(
            f"Cannot run evaluation because number of permutation is too high: {n_permutations}."
        )

    for dependent_groups in list_of_dependent_groups:
        best_bijections.append(find_best_map(dependent_groups, bijection, scoring_fn))

    for best_bijection in best_bijections:
        bijection = bijection.extends(best_bijection)

    all_groups = DependentGroups(pair_groups)

    TP = eval_score(all_groups, bijection, scoring_fn)

    if len(all_groups.X_triples) == 0:
        # gold is empty, recall must be 1
        recall = 1
    else:
        recall = TP / len(all_groups.X_triples)

    if len(all_groups.X_prime_triples) == 0:
        # predict nothing, the precision must be 1
        precision = 1
    else:
        precision = TP / len(all_groups.X_prime_triples)

    if precision == 0 and recall == 0:
        f1 = 0.0
    else:
        f1 = 2 * precision * recall / (precision + recall)

    return SmPrecisionRecallF1Output(
        f1=f1,
        precision=precision,
        recall=recall,
        bijection=bijection,
        n_corrects=TP,
        n_examples=len(all_groups.X_triples),
        n_predictions=len(all_groups.X_prime_triples),
        gold_triples=all_groups.X_triples,
        pred_triples=all_groups.X_prime_triples,
    )
