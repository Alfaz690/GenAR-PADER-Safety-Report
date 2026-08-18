from __future__ import annotations

from typing import Any


def _fmt_map(mapping: dict[str, Any], limit: int | None = None) -> str:
    items = list(mapping.items())
    if limit is not None:
        items = items[:limit]
    return "; ".join(f"{k}: {v}" for k, v in items) if items else "None reported."


def _fmt_reactions(items: list[dict[str, Any]], limit: int = 10) -> str:
    if not items:
        return "No reaction data were available."
    return "; ".join(f"{x['value']} ({x['count']})" for x in items[:limit])


def generate_offline_sections(analysis: dict) -> dict[str, str]:
    period = analysis["reporting_period"]
    summary = analysis["case_summary"]

    return {
        "narrative": (
            f"The supplied Bisoprolol safety dataset contains {summary['total_cases']} "
            f"unique cases. The reporting period calculated from `receivedate` is "
            f"{period['start']} to {period['end']}. Of the unique cases, "
            f"{summary['serious_cases']} were classified as serious and "
            f"{summary['non_serious_cases']} as non-serious. The most frequently "
            f"reported reactions at Preferred Term level were {_fmt_reactions(analysis['top_reactions'], 5)}. "
            "These are descriptive observations from the supplied dataset and do not by themselves establish a safety signal."
        ),
        "cases": (
            f"There were {summary['total_cases']} unique cases, including "
            f"{summary['serious_cases']} serious and {summary['non_serious_cases']} non-serious cases. "
            f"Age-group distribution was: {_fmt_map(analysis['age_groups'])}. "
            f"Sex distribution was: {_fmt_map(analysis['sex_distribution'])}. "
            f"The leading countries by case count were: {_fmt_map(analysis['country_distribution_top15'], 10)}. "
            f"Reported reaction outcomes were: {_fmt_map(dict((x['value'], x['count']) for x in analysis['outcomes']))}."
        ),
        "reactions": (
            "Reaction analysis is performed at the supplied Preferred Term level. "
            f"The most frequent reactions were {_fmt_reactions(analysis['top_reactions'])}. "
            f"Among serious case IDs, the most frequent reactions were {_fmt_reactions(analysis['top_serious_reactions'])}. "
            "System Organ Class groupings were not generated because SOC data were not supplied."
        ),
        "alerts": (
            f"The dataset contains {analysis['alerts']['alert_cases']} unique case(s) with `fulfillexpeditecriteria` indicating an expedited/15-day criterion. "
            "This section reports the supplied field value only; it does not infer expectedness or create additional case narratives."
        ),
        "trends": (
            f"Monthly case counts derived from `receivedate` were: {_fmt_map({x['month']: x['cases'] for x in analysis['trends']['monthly_cases']})}. "
            + (analysis['trends']['observation'] or "No first-versus-last-month change statement was generated because fewer than two valid months were available or the values were equal.")
            + " These descriptive patterns should not be interpreted as confirmed safety signals."
        ),
        "history": (
            "No history-of-safety-related-actions dataset was supplied. Accordingly, no regulatory action, label change, communication, or other safety action is asserted in this report."
        ),
        "case_index": (
            "A case-level CSV listing is generated alongside this report from unique `safetyreportid` records. "
            "It contains the case ID, reaction summary, seriousness, reporting date, country, and outcome summary where those fields are available in the supplied data."
        ),
    }
