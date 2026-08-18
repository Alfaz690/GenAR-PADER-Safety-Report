import pandas as pd


REQUIRED_COLUMNS = [
    "safetyreportid",
    "occurcountry",
    "patient_patientonsetage",
    "patient_patientsex",
    "patient_reaction_reactionmeddrapt",
    "patient_reaction_reactionoutcome",
    "serious",
    "fulfillexpeditecriteria",
    "receivedate",
]


def validate_columns(df: pd.DataFrame) -> None:
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(missing))


def _parse_receivedate(series: pd.Series) -> pd.Series:
    """Parse common ICSR receivedate values safely.

    The supplied dataset stores dates as YYYYMMDD integers (e.g. 20241227).
    Treating those integers as Unix nanoseconds incorrectly produces 1970 dates,
    so 8-digit YYYYMMDD values are parsed explicitly first.
    """
    raw = series.astype("string").str.strip()
    yyyymmdd = pd.to_datetime(raw, format="%Y%m%d", errors="coerce")
    remaining = yyyymmdd.isna()
    if remaining.any():
        yyyymmdd.loc[remaining] = pd.to_datetime(
            raw.loc[remaining], errors="coerce"
        )
    return yyyymmdd


def validate_and_prepare(df: pd.DataFrame) -> pd.DataFrame:
    validate_columns(df)

    out = df.copy()

    out["safetyreportid"] = out["safetyreportid"].astype("string").str.strip()
    out["receivedate"] = _parse_receivedate(out["receivedate"])

    out["patient_patientonsetage"] = pd.to_numeric(
        out["patient_patientonsetage"], errors="coerce"
    )

    for col in ["serious", "fulfillexpeditecriteria"]:
        out[col] = out[col].astype("string").str.strip().str.lower()

    if out["safetyreportid"].isna().any():
        raise ValueError("Some rows have missing safetyreportid values.")

    return out
