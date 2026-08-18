from pathlib import Path
import pandas as pd


def load_csv(csv_path: str) -> pd.DataFrame:
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    df = pd.read_csv(path, low_memory=False)
    if df.empty:
        raise ValueError("Dataset is empty.")

    return df


def normalize_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    for col in out.columns:
        if out[col].dtype == "object":
            out[col] = out[col].astype("string").str.strip()

    return out
