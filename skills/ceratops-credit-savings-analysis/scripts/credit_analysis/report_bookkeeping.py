"""Pure report bookkeeping over validated semantic decisions.

The controller owns evidence, model judgments, and persistence. These helpers
validate result shapes, order surface sets, and reconcile temporary-control
report links without performing I/O or adjudicating findings.
"""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from .single_thread_analysis import CreditAnalysisError


def _closed_result(value: Mapping[str, Any], fields: set[str], label: str) -> None:
    if set(value) != fields:
        missing = sorted(fields - set(value))
        extra = sorted(set(value) - fields)
        detail = []
        if missing:
            detail.append("missing " + ", ".join(missing))
        if extra:
            detail.append("unknown " + ", ".join(extra))
        raise CreditAnalysisError(f"{label} fields are invalid: {'; '.join(detail)}")


def _result_deduped_strings(
    value: Any, label: str, *, empty: bool = False
) -> list[str]:
    """Normalize only exact duplicate descriptive strings while preserving order."""

    if (
        not isinstance(value, list)
        or (not empty and not value)
        or not all(isinstance(item, str) and item for item in value)
    ):
        qualifier = "string list" if empty else "nonempty string list"
        raise CreditAnalysisError(f"{label} must be a {qualifier}")
    return list(dict.fromkeys(value))


def _result_objects(value: Any, label: str) -> list[dict[str, Any]]:
    if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
        raise CreditAnalysisError(f"{label} must be an object list")
    return list(value)


def _holistic_surface_ids(
    value: Any,
    label: str,
    surface_order: Sequence[str],
) -> list[str]:
    """Validate a surface set and normalize it to the frozen public order."""

    surfaces = _result_deduped_strings(value, label)
    if not set(surfaces) <= set(surface_order):
        raise CreditAnalysisError(f"{label} contains an unknown surface")
    return [surface for surface in surface_order if surface in set(surfaces)]


def _holistic_temporary_control_merges(
    raw_merges: Any,
    *,
    review_by_id: Mapping[str, Mapping[str, Any]],
    finding_by_id: Mapping[str, Mapping[str, Any]],
    surface_order: Sequence[str],
) -> list[dict[str, Any]]:
    """Complete report links without changing validated review decisions.

    Explicit links must pass validation before missing links are filled. A
    finding with missing links must have one exact review owner and at most
    one existing merge; otherwise choosing a merge would require judgment.
    New control keys reuse the linked finding's durable control verbatim.
    Neither the raw report nor its review/finding records are mutated.
    """

    raw_merges = _result_objects(
        raw_merges, "temporary-control merges"
    )
    merges: list[dict[str, Any]] = []
    merged_reviews: set[str] = set()
    merge_keys: set[tuple[str, str]] = set()
    required_merged = {
        review_id for review_id, review in review_by_id.items()
        if review["finding_id"] is not None
    }
    for review_id in sorted(required_merged):
        owner = review_by_id[review_id].get("owning_producer")
        if not isinstance(owner, str) or not owner.strip():
            raise CreditAnalysisError(
                f"temporary-control review {review_id} owner is invalid"
            )
    for index, merge in enumerate(raw_merges, start=1):
        label = f"temporary-control merge {index}"
        _closed_result(
            merge,
            {"control_key", "owning_producer", "review_ids", "contributing_surfaces", "finding_id"},
            label,
        )
        for field in ("owning_producer", "control_key"):
            value = merge.get(field)
            if not isinstance(value, str) or not value.strip():
                raise CreditAnalysisError(f"{label} {field} is invalid")
        merge_key = (merge["owning_producer"], merge["control_key"])
        if merge_key in merge_keys:
            raise CreditAnalysisError("temporary-control owner/control is merged twice")
        merge_keys.add(merge_key)
        review_ids = _result_deduped_strings(merge.get("review_ids"), f"{label} reviews")
        if not set(review_ids) <= set(review_by_id):
            raise CreditAnalysisError(f"{label} review ownership is invalid")
        eligible_review_ids = [
            review_id
            for review_id in review_ids
            if review_by_id[review_id]["finding_id"] is not None
        ]
        _holistic_surface_ids(
            merge.get("contributing_surfaces"),
            f"{label} surfaces",
            surface_order,
        )
        if not eligible_review_ids:
            continue
        if set(eligible_review_ids) & merged_reviews:
            raise CreditAnalysisError(f"{label} review ownership is invalid")
        if any(
            review_by_id[review_id]["owning_producer"] != merge["owning_producer"]
            for review_id in eligible_review_ids
        ):
            raise CreditAnalysisError(f"{label} producer ownership is invalid")
        finding_id = merge.get("finding_id")
        if not isinstance(finding_id, str) or finding_id not in finding_by_id or any(
            review_by_id[review_id]["finding_id"] != finding_id
            for review_id in eligible_review_ids
        ):
            raise CreditAnalysisError(f"{label} finding ownership is invalid")
        merged_reviews.update(eligible_review_ids)
        surfaces = [
            surface
            for surface in surface_order
            if any(
                surface in review_by_id[review_id]["contributing_surfaces"]
                for review_id in eligible_review_ids
            )
        ]
        merges.append(
            {
                **merge,
                "review_ids": eligible_review_ids,
                "contributing_surfaces": surfaces,
            }
        )
    # The review's explicit finding ID is the association. Do not infer a
    # connection from prose similarity, candidate overlap, or call overlap.
    missing_by_finding: dict[str, list[str]] = {}
    missing_review_ids = required_merged - merged_reviews
    for review_id, review in review_by_id.items():
        if review_id in missing_review_ids:
            missing_by_finding.setdefault(review["finding_id"], []).append(review_id)
    for finding_id, missing_ids in missing_by_finding.items():
        owners = {
            review["owning_producer"]
            for review in review_by_id.values()
            if review["finding_id"] == finding_id
        }
        existing = [merge for merge in merges if merge["finding_id"] == finding_id]
        if len(owners) != 1 or len(existing) > 1:
            raise CreditAnalysisError(
                f"temporary-control finding {finding_id} merge ownership is ambiguous"
            )
        owner = next(iter(owners))
        if existing:
            target = existing[0]
        else:
            control = finding_by_id[finding_id]["proposed_durable_control"]
            key = (owner, control)
            if key in merge_keys:
                raise CreditAnalysisError(
                    f"temporary-control finding {finding_id} owner/control is ambiguous"
                )
            merge_keys.add(key)
            target = {
                "control_key": control,
                "owning_producer": owner,
                "review_ids": [],
                "contributing_surfaces": [],
                "finding_id": finding_id,
            }
            merges.append(target)
        target["review_ids"] = [*target["review_ids"], *missing_ids]
        target["contributing_surfaces"] = [
            surface for surface in surface_order
            if any(
                surface in review_by_id[review_id]["contributing_surfaces"]
                for review_id in target["review_ids"]
            )
        ]
        merged_reviews.update(missing_ids)
    if merged_reviews != required_merged:
        raise CreditAnalysisError("temporary-control confirmed findings were not merged once")
    return merges
