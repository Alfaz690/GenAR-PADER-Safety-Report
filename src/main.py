import argparse
import json
from pathlib import Path

from .analysis import compute_analysis
from .evidence import build_evidence, save_evidence
from .generator import generate_sections, markdown_report, save_report
from .loader import load_csv, normalize_text_columns
from .validator import validate_report
from .validation import validate_and_prepare
import pandas as pd


def run(csv_path: str, use_ai: bool = True):
    print("1. Loading dataset...")
    df = load_csv(csv_path)

    print("2. Normalizing text...")
    df = normalize_text_columns(df)

    print("3. Validating dataset...")
    df = validate_and_prepare(df)

    print("4. Running deterministic analysis...")
    analysis = compute_analysis(df)

    Path("output").mkdir(exist_ok=True)

    Path("output/analysis.json").write_text(
        json.dumps(analysis, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    evidence = build_evidence(analysis)
    save_evidence(evidence)

    if not use_ai:
        print("5. Generating offline evidence-grounded sections...")
        sections = generate_sections(analysis, use_ai=False)
    else:
        print("5. Generating AI sections...")
        try:
            sections = generate_sections(analysis, use_ai=True)
        except Exception as exc:
            print(f"AI generation unavailable ({type(exc).__name__}: {exc})")
            print("Falling back to deterministic evidence-grounded report generation.")
            sections = generate_sections(analysis, use_ai=False)

    print("6. Validating generated sections...")

    validation = validate_report(sections, analysis)

    Path("output/validation.json").write_text(
        json.dumps(validation, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    if not validation["overall_valid"]:
        print("WARNING: Some generated sections contain unsupported numbers.")
        print("Review output/validation.json before using the report.")

    print("7. Creating report...")
    report = markdown_report(analysis, sections)
    save_report(report)

    # Create a reviewer-friendly case index from the uploaded case-level data.
    case_cols = [
        "safetyreportid", "patient_reaction_reactionmeddrapt", "serious",
        "receivedate", "occurcountry", "patient_reaction_reactionoutcome"
    ]
    available = [c for c in case_cols if c in df.columns]
    case_index = df[available].copy()
    case_index["receivedate"] = case_index["receivedate"].dt.strftime("%Y-%m-%d")
    case_index = case_index.drop_duplicates().sort_values("safetyreportid")
    case_index.to_csv("output/case_index.csv", index=False, encoding="utf-8-sig")

    print("\nDONE")
    print("Generated:")
    print("  output/analysis.json")
    print("  output/evidence.json")
    print("  output/validation.json")
    print("  output/pader_report.md")
    print("  output/case_index.csv")

    return analysis


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="GenAR PADER-style report generator"
    )
    parser.add_argument(
        "--csv",
        required=True,
        help="Path to Bisoprolol_icsr_sample_1068rows.csv",
    )
    parser.add_argument(
        "--no-ai",
        action="store_true",
        help="Run deterministic analysis only.",
    )

    args = parser.parse_args()
    run(args.csv, use_ai=not args.no_ai)
