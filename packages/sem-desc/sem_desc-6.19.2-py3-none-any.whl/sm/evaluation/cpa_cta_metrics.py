from dataclasses import dataclass
from typing import Dict, Mapping, Optional, Sequence, Set, Union

from sm.evaluation import sm_metrics
from sm.evaluation.utils import PrecisionRecallF1
from sm.outputs import (
    ClassNode,
    DataNode,
    SemanticModel,
    remove_isolated_nodes,
    replace_class_nodes_by_subject_columns,
)


@dataclass
class CTAEvalOutput(PrecisionRecallF1):
    n_corrects: float  # float as we allow for partial correctness
    n_examples: int
    n_predictions: int


def cpa(
    gold_sm: SemanticModel,
    pred_sm: SemanticModel,
    id_props: Set[str],
    scoring_fn: Optional[sm_metrics.ScoringFn] = None,
) -> sm_metrics.SmPrecisionRecallF1Output:
    gold_sm = gold_sm.deep_copy()
    pred_sm = pred_sm.deep_copy()

    _cpa_transformation(gold_sm, id_props)
    _cpa_transformation(pred_sm, id_props)

    return sm_metrics.precision_recall_f1(
        gold_sm=gold_sm, pred_sm=pred_sm, scoring_fn=scoring_fn
    )


def cta(
    gold_sm: SemanticModel,
    pred_sm: SemanticModel,
    id_props: Set[str],
    scoring_fn: Optional[sm_metrics.ScoringFn] = None,
    ignored_columns: Optional[Set[str]] = None,
) -> CTAEvalOutput:
    gold_cta = _get_cta(gold_sm, id_props)
    pred_cta = _get_cta(pred_sm, id_props)

    if ignored_columns is not None:
        gold_cta = {k: v for k, v in gold_cta.items() if k not in ignored_columns}
        pred_cta = {k: v for k, v in pred_cta.items() if k not in ignored_columns}

    if scoring_fn is None:
        scoring_fn = sm_metrics.ScoringFn()

    return _cta_real(gold_cta, pred_cta, scoring_fn)


def _cta_real(
    gold_cta: Mapping[str, Union[Sequence[str], Set[str], str]],
    pred_cta: Mapping[str, str],
    scoring_fn: sm_metrics.ScoringFn,
):
    score = 0.0
    for cindex in set(gold_cta.keys()).intersection(pred_cta.keys()):
        gc = gold_cta[cindex]
        pc = pred_cta[cindex]

        if not isinstance(gc, str):
            score += max(scoring_fn.get_match_score(pc, g) for g in gc)
        else:
            score += scoring_fn.get_match_score(pc, gc)

    if len(pred_cta) == 0:
        precision = 1.0
    else:
        precision = score / len(pred_cta)

    if len(gold_cta) == 0:
        recall = 1.0
    else:
        recall = score / len(gold_cta)

    if recall + precision == 0:
        f1 = 0
    else:
        f1 = 2 * precision * recall / (precision + recall)
    return CTAEvalOutput(
        precision=precision,
        recall=recall,
        f1=f1,
        n_corrects=score,
        n_examples=len(gold_cta),
        n_predictions=len(pred_cta),
    )


def _get_cta(sm: SemanticModel, id_props: Set[str]) -> Dict[str, str]:
    col2class = {}
    for n in sm.iter_nodes():
        if isinstance(n, ClassNode):
            outedges = sm.out_edges(n.id)
            id_edges = [outedge for outedge in outedges if outedge.abs_uri in id_props]
            if len(id_edges) > 1:
                raise Exception("Haven't supported multiple subject columns yet")
            if len(id_edges) == 0:
                continue
            dnode = sm.get_node(id_edges[0].target)
            assert isinstance(dnode, DataNode)
            col2class[str(dnode.col_index)] = n.abs_uri
    return col2class


def _cpa_transformation(sm: SemanticModel, id_props: Set[str]) -> None:
    replace_class_nodes_by_subject_columns(sm, id_props)
    remove_isolated_nodes(sm)
