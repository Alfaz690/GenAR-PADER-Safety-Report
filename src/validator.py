import re
import math
from typing import Any


def extract_integers(text: str) -> list[int]:
    return [int(x.replace(",", "")) for x in re.findall(r"\b\d[\d,]*\b", text)]


def validate_section_numbers(text: str, allowed_numbers: set[int]) -> dict[str, Any]:
    numbers = extract_integers(text)
    unsupported = sorted(set(n for n in numbers if n not in allowed_numbers))

    return {
        "valid": len(unsupported) == 0,
        "numbers_found": numbers,
        "unsupported_numbers": unsupported,
    }


def _numbers_from_analysis(value):
    numbers = set()
    if isinstance(value, bool) or value is None:
        return numbers
    if isinstance(value, int):
        numbers.add(value)
    elif isinstance(value, float) and math.isfinite(value):
        numbers.add(int(value))
        numbers.add(value)
    elif isinstance(value, str):
        numbers.update(extract_integers(value))
    elif isinstance(value, dict):
        for key, item in value.items():
            numbers.update(_numbers_from_analysis(key))
            numbers.update(_numbers_from_analysis(item))
    elif isinstance(value, (list, tuple)):
        for item in value:
            numbers.update(_numbers_from_analysis(item))
    return numbers


def validate_report(sections: dict[str, str], analysis: dict) -> dict:
    # Allow every numeric value that was deterministically produced from the
    # dataset. This avoids false flags for percentages, dates and trend counts.
    allowed = _numbers_from_analysis(analysis)

    result = {}
    for name, text in sections.items():
        result[name] = validate_section_numbers(text, allowed)

    result["overall_valid"] = all(item["valid"] for item in result.values())
    return result
