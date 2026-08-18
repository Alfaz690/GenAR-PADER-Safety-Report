from __future__ import annotations

from collections import Counter
from typing import Any
import pandas as pd


def _is_yes(value: Any) -> bool:
    if pd.isna(value):
        return False
    return str(value).strip().lower() in {
        "yes", "y", "true", "1", "serious"
    }


def _is_no(value: Any) -> bool:
    if pd.isna(value):
        return False
    return str(value).strip().lower() in {
        "no", "n", "false", "0", "non-serious", "nonserious"
    }


def age_bucket(age: Any) -> str:
    if pd.isna(age):
        return "Unknown"

    try:
        age = float(age)
    except (TypeError, ValueError):
        return "Unknown"

    if age < 18:
        return "<18"
    if age < 45:
        return "18-44"
    if age < 65:
        return "45-64"
    if age < 75:
        return "65-74"
    return "75+"


def _clean_category(series: pd.Series, unknown="Unknown") -> pd.Series:
    s = series.astype("string").str.strip()
    return s.mask(s.isna() | (s == ""), unknown)


def _count_series(series: pd.Series, top_n: int = 10) -> list[dict]:
    s = _clean_category(series)
    counts = s.value_counts(dropna=False).head(top_n)
    return [
        {"value": str(idx), "count": int(count)}
        for idx, count in counts.items()
    ]


def _case_level_first(df: pd.DataFrame) -> pd.DataFrame:
    """
    Collapse multiple reaction rows to one case-level record.
    Case-level fields are taken from the first non-null value within each case.
    Reaction-level fields remain in the original dataframe.
    """
    work = df.copy()

    def first_non_null(series):
        non_null = series.dropna()
        return non_null.iloc[0] if not non_null.empty else None

    case_cols = [
        "safetyreportid",
        "occurcountry",
        "patient_patientonsetage",
        "patient_patientsex",
        "serious",
        "fulfillexpeditecriteria",
        "receivedate",
    ]

    available = [c for c in case_cols if c in work.columns]

    return (
        work.groupby("safetyreportid", dropna=False)[available]
        .agg(first_non_null)
        .reset_index(drop=True)
    )


def compute_analysis(df: pd.DataFrame) -> dict:
    case_df = _case_level_first(df)

    total_cases = int(df["safetyreportid"].nunique())

    serious_mask = df["serious"].map(_is_yes)
    serious_case_ids = set(df.loc[serious_mask, "safetyreportid"].dropna().astype(str))
    serious_cases = len(serious_case_ids)
    non_serious_cases = total_cases - serious_cases

    age = df[["safetyreportid", "patient_patientonsetage"]].copy()
    age["age_group"] = age["patient_patientonsetage"].map(age_bucket)
    age_case = age.drop_duplicates("safetyreportid")
    age_counts = age_case["age_group"].value_counts().to_dict()

    sex_case = case_df["patient_patientsex"].astype("string").str.strip().replace(
        {"": "Unknown", "<NA>": "Unknown"}
    ).fillna("Unknown")
    sex_counts = {
        str(k): int(v) for k, v in sex_case.value_counts().items()
    }

    country_case = case_df["occurcountry"].astype("string").str.strip().replace(
        {"": "Unknown", "<NA>": "Unknown"}
    ).fillna("Unknown")
    country_counts = {
        str(k): int(v) for k, v in country_case.value_counts().head(15).items()
    }

    reaction_series = df["patient_reaction_reactionmeddrapt"]
    top_reactions = _count_series(reaction_series, 15)

    serious_reactions = df.loc[
        df["safetyreportid"].astype(str).isin(serious_case_ids),
        "patient_reaction_reactionmeddrapt"
    ]
    top_serious_reactions = _count_series(serious_reactions, 15)

    outcome_counts = _count_series(
        df["patient_reaction_reactionoutcome"], 15
    )

    alert_mask = df["fulfillexpeditecriteria"].map(_is_yes)
    alert_case_ids = sorted(
        df.loc[alert_mask, "safetyreportid"].dropna().astype(str).unique().tolist()
    )

    monthly = (
        df.dropna(subset=["receivedate"])
        .assign(month=lambda x: x["receivedate"].dt.to_period("M").astype(str))
        .groupby("month")["safetyreportid"]
        .nunique()
        .reset_index(name="cases")
    )
    monthly_trends = [
        {"month": str(row["month"]), "cases": int(row["cases"])}
        for _, row in monthly.iterrows()
    ]

    # A simple transparent trend flag: compare first and last month.
    trend_observation = None
    if len(monthly_trends) >= 2:
        first = monthly_trends[0]
        last = monthly_trends[-1]
        if first["cases"] != last["cases"]:
            direction = "increased" if last["cases"] > first["cases"] else "decreased"
            trend_observation = (
                f"Case volume {direction} from {first['cases']} in "
                f"{first['month']} to {last['cases']} in {last['month']}."
            )

    reporting_start = df["receivedate"].min()
    reporting_end = df["receivedate"].max()

    return {
        "dataset": {
            "rows": int(len(df)),
            "unique_cases": total_cases,
            "product": "Bisoprolol",
        },
        "reporting_period": {
            "start": reporting_start.strftime("%Y-%m-%d")
            if pd.notna(reporting_start) else None,
            "end": reporting_end.strftime("%Y-%m-%d")
            if pd.notna(reporting_end) else None,
        },
        "case_summary": {
            "total_cases": total_cases,
            "serious_cases": serious_cases,
            "non_serious_cases": non_serious_cases,
            "serious_percentage": round(
                (serious_cases / total_cases) * 100, 2
            ) if total_cases else 0,
            "non_serious_percentage": round(
                (non_serious_cases / total_cases) * 100, 2
            ) if total_cases else 0,
        },
        "age_groups": {str(k): int(v) for k, v in age_counts.items()},
        "sex_distribution": sex_counts,
        "country_distribution_top15": country_counts,
        "top_reactions": top_reactions,
        "top_serious_reactions": top_serious_reactions,
        "outcomes": outcome_counts,
        "alerts": {
            "alert_cases": len(alert_case_ids),
            "case_ids": alert_case_ids[:100],
        },
        "trends": {
            "monthly_cases": monthly_trends,
            "observation": trend_observation,
        },
        "limitations": [
            "No history-of-actions dataset was supplied.",
            "No product label/CCDS was supplied, so expectedness is out of scope.",
            "No System Organ Class field was supplied; analysis is at Preferred Term level.",
            "Country analysis uses occurcountry consistently.",
            "Case-level counts use unique safetyreportid; reaction-level counts use reaction rows.",
        ],
    }
