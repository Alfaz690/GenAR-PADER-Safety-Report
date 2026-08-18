import json
from pathlib import Path
from typing import Any


def build_evidence(analysis: dict[str, Any]) -> dict[str, Any]:
    """
    Wrap deterministic analysis in an explicit evidence structure.
    Every generated section receives only the evidence it needs.
    """
    return {
        "E001": {
            "claim": "Total unique cases",
            "value": analysis["case_summary"]["total_cases"],
            "source_field": "safetyreportid",
            "method": "unique count of safetyreportid",
        },
        "E002": {
            "claim": "Serious cases",
            "value": analysis["case_summary"]["serious_cases"],
            "source_field": "serious",
            "method": "unique safetyreportid where serious is yes/serious",
        },
        "E003": {
            "claim": "Non-serious cases",
            "value": analysis["case_summary"]["non_serious_cases"],
            "source_field": "serious",
            "method": "total unique cases minus serious cases",
        },
        "E004": {
            "claim": "Most common reactions",
            "value": analysis["top_reactions"],
            "source_field": "patient_reaction_reactionmeddrapt",
            "method": "reaction-level value counts",
        },
        "E005": {
            "claim": "Most common serious reactions",
            "value": analysis["top_serious_reactions"],
            "source_field": "patient_reaction_reactionmeddrapt + serious",
            "method": "reaction-level counts restricted to serious case IDs",
        },
        "E006": {
            "claim": "Outcomes",
            "value": analysis["outcomes"],
            "source_field": "patient_reaction_reactionoutcome",
            "method": "reaction-level value counts",
        },
        "E007": {
            "claim": "Age groups",
            "value": analysis["age_groups"],
            "source_field": "patient_patientonsetage",
            "method": "deterministic age buckets",
        },
        "E008": {
            "claim": "Sex distribution",
            "value": analysis["sex_distribution"],
            "source_field": "patient_patientsex",
            "method": "case-level value counts",
        },
        "E009": {
            "claim": "Country distribution",
            "value": analysis["country_distribution_top15"],
            "source_field": "occurcountry",
            "method": "case-level value counts",
        },
        "E010": {
            "claim": "15-day/expedited alert cases",
            "value": analysis["alerts"],
            "source_field": "fulfillexpeditecriteria",
            "method": "unique case IDs where expedited criterion is yes",
        },
        "E011": {
            "claim": "Monthly trend",
            "value": analysis["trends"],
            "source_field": "receivedate",
            "method": "unique case count by calendar month",
        },
        "E012": {
            "claim": "Known limitations",
            "value": analysis["limitations"],
            "source_field": "challenge dataset documentation",
            "method": "documented scope limitations",
        },
    }


def save_evidence(evidence: dict, path: str = "output/evidence.json") -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(
        json.dumps(evidence, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
