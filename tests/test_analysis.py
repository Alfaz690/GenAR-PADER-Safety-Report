import pandas as pd

from src.analysis import compute_analysis


def test_unique_case_count_and_seriousness():
    df = pd.DataFrame(
        {
            "safetyreportid": ["1", "1", "2"],
            "occurcountry": ["India", "India", "USA"],
            "patient_patientonsetage": [70, 70, 30],
            "patient_patientsex": ["female", "female", "male"],
            "patient_reaction_reactionmeddrapt": [
                "Headache", "Fatigue", "Headache"
            ],
            "patient_reaction_reactionoutcome": [
                "Recovered", "Recovered", "Unknown"
            ],
            "serious": ["serious", "serious", "no"],
            "fulfillexpeditecriteria": ["yes", "yes", "no"],
            "receivedate": pd.to_datetime(
                ["2025-01-01", "2025-01-01", "2025-02-01"]
            ),
        }
    )

    result = compute_analysis(df)

    assert result["case_summary"]["total_cases"] == 2
    assert result["case_summary"]["serious_cases"] == 1
    assert result["case_summary"]["non_serious_cases"] == 1
