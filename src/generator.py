from pathlib import Path
from .evidence import build_evidence
from .llm import generate_text
from .offline_report import generate_offline_sections
from .prompts import SYSTEM_PROMPT, build_prompt


SECTION_EVIDENCE = {
    "narrative": [
        "E001", "E002", "E003", "E004", "E005", "E006", "E011", "E012"
    ],
    "cases": [
        "E001", "E002", "E003", "E007", "E008", "E009", "E006"
    ],
    "reactions": [
        "E004", "E005", "E006", "E007", "E008"
    ],
    "alerts": [
        "E010", "E004", "E005", "E006", "E012"
    ],
    "trends": [
        "E011", "E004", "E005", "E012"
    ],
    "history": [
        "E012"
    ],
    "case_index": [
        "E001", "E012"
    ],
}


def generate_sections(analysis: dict, use_ai: bool = True) -> dict[str, str]:
    if not use_ai:
        return generate_offline_sections(analysis)

    evidence = build_evidence(analysis)
    sections = {}

    for section, evidence_ids in SECTION_EVIDENCE.items():
        subset = {eid: evidence[eid] for eid in evidence_ids}
        prompt = SYSTEM_PROMPT + "\n" + build_prompt(section, subset)
        sections[section] = generate_text(prompt)

    return sections


def markdown_report(analysis: dict, sections: dict[str, str]) -> str:
    period = analysis["reporting_period"]

    lines = [
        "# PADER-Style Safety Report",
        "",
        "## 1. Reporting Period",
        "",
        f"**Product:** {analysis['dataset']['product']}",
        f"**Reporting period:** {period['start']} to {period['end']}",
        "**Report type:** PADER-style technical evaluation report",
        "",
        "## 2. Narrative Summary and Analysis",
        "",
        sections["narrative"],
        "",
        "## 3. Summary Analysis of Cases",
        "",
        sections["cases"],
        "",
        "## 4. Reaction / Adverse Event Analysis",
        "",
        sections["reactions"],
        "",
        "## 5. Serious Cases / 15-Day Alerts",
        "",
        sections["alerts"],
        "",
        "## 6. Trends and Important Observations",
        "",
        sections["trends"],
        "",
        "## 7. History of Safety-Related Actions",
        "",
        sections["history"],
        "",
        "## 8. Case Index / Listing",
        "",
        sections["case_index"],
        "",
        "## Technical Notes and Limitations",
        "",
        "- Case-level counts use unique `safetyreportid`.",
        "- Reaction-level counts use individual reaction rows.",
        "- Country analysis consistently uses `occurcountry`.",
        "- Expectedness is out of scope because no product label/CCDS was supplied.",
        "- SOC analysis is out of scope because the dataset does not supply SOC.",
        "- No history-of-actions information was supplied.",
        "",
        "## Human Review",
        "",
        "This report is a generated draft and requires human review before being treated as final.",
    ]

    return "\n".join(lines)


def save_report(markdown: str, path: str = "output/pader_report.md") -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(markdown, encoding="utf-8")
