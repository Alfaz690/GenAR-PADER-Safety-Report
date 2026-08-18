SYSTEM_PROMPT = """
You are a regulatory safety-report writing assistant for a technical evaluation.

Rules:
1. Use only the evidence provided in the user context.
2. Never invent numbers, cases, reactions, actions, dates, or conclusions.
3. Do not perform arithmetic when a computed value is supplied.
4. Use neutral, factual, regulatory-style language.
5. Distinguish observation from interpretation.
6. Do not call a numerical pattern a confirmed safety signal.
7. If the evidence is insufficient, explicitly say that the information was not provided.
8. Do not infer expectedness without product-label evidence.
9. Do not invent a history of safety-related actions.
10. Do not invent System Organ Class groupings when SOC data is unavailable.
"""


SECTION_RULES = {
    "narrative": """
Write a concise Narrative Summary and Analysis.
Include reporting period, total cases, seriousness, major reactions,
and important data-supported observations.
Do not add unsupported medical conclusions.
""",
    "cases": """
Write Summary Analysis of Cases.
Discuss case volume, serious/non-serious cases, age groups, sex,
country distribution, and outcomes using only supplied evidence.
""",
    "reactions": """
Write Reaction / Adverse Event Analysis.
Discuss the most frequent reactions and serious reactions.
Mention that analysis is at Preferred Term level if appropriate.
Do not invent SOC classifications.
""",
    "alerts": """
Write Serious Cases / 15-Day Alerts analysis.
Use only the alert evidence supplied.
Do not invent case narratives or expectedness.
""",
    "trends": """
Write Trends and Important Observations.
Describe only the supplied numerical patterns.
Do not label any pattern as a confirmed safety signal.
""",
    "history": """
Write the History of Safety-Related Actions section.
The supplied dataset contains no history-of-actions information.
State this clearly and do not invent actions.
""",
    "case_index": """
Explain the case index/listing and provide a concise note that the
individual case listing is generated from the supplied case-level data.
Do not invent individual case facts.
""",
}


def build_prompt(section: str, evidence_subset: dict) -> str:
    rules = SECTION_RULES[section]

    return f"""
SECTION:
{section}

TASK:
{rules}

APPROVED EVIDENCE:
{evidence_subset}

Write only the requested section.
Every number or factual claim must be directly supported by the evidence.
Use a professional, neutral safety-report style.
"""
