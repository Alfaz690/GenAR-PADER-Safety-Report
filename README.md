# GenAR — AI PADER-Style Safety Report Generator

## 1. What this project does

This prototype converts the supplied Bisoprolol ICSR safety dataset into an
evidence-backed PADER-style report.

The pipeline is:

```text
CSV
 -> validate
 -> deterministic analysis
 -> evidence package
 -> section-specific AI context
 -> LLM-generated draft
 -> validation
 -> human review
 -> final report
```

## 2. Why deterministic analysis is separate from AI

Python is used for exact calculations:

- unique case count
- serious/non-serious case count
- age groups
- sex
- country
- reaction frequency
- serious reaction frequency
- outcomes
- alerts
- monthly trends

The LLM is used for:

- neutral narrative writing
- interpreting approved observations
- organizing report sections

The LLM is not given the raw CSV and is not trusted to calculate report
numbers.

## 3. Dataset handling

Case-level counts use unique `safetyreportid`, because one case can contain
multiple reaction rows.

Reaction-level counts use reaction rows.

Country analysis uses `occurcountry`.

Age groups are created from `patient_patientonsetage`.

SOC analysis is not attempted because the supplied dataset does not provide SOC.

Expectedness is not attempted because no product label/CCDS is supplied.

History of safety-related actions is not invented because no such data is
supplied.

## 4. Setup

Create a virtual environment:

### Windows

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## 5. Configure the AI API

Copy:

```text
.env.example
```

to:

```text
.env
```

Then set:

```text
OPENAI_API_KEY=your_key
OPENAI_MODEL=gpt-4.1-mini
```

Do not commit `.env`.

## 6. Run deterministic analysis only

```bash
python -m src.main --csv "data/Bisoprolol_icsr_sample_1068rows.csv" --no-ai
```

This creates:

```text
output/analysis.json
output/evidence.json
```

## 7. Run the complete AI pipeline

```bash
python -m src.main --csv "data/Bisoprolol_icsr_sample_1068rows.csv"
```

This creates:

```text
output/analysis.json
output/evidence.json
output/validation.json
output/pader_report.md
```

## 8. Run the optional web UI

```bash
streamlit run app.py
```

Then upload the supplied CSV.

## 9. Testing

```bash
python -m pytest
```

## 10. Prompt design

Prompts are stored in:

```text
src/prompts.py
```

The system prompt establishes global safety rules. Section-specific rules are
added dynamically for:

- narrative
- cases
- reactions
- alerts
- trends
- history
- case index

The context contains only the evidence required by that section.

## 11. Grounding

The evidence layer assigns evidence IDs such as:

```text
E001 -> total unique cases
E002 -> serious cases
E004 -> most common reactions
E010 -> expedited/alert cases
E011 -> monthly trends
```

The goal is that every generated factual claim can be traced to deterministic
analysis.

## 12. Human review

The Streamlit UI includes Approve/Flag controls for generated sections.

A production system would store reviewer decisions and require approval before
finalization.

## 13. Known limitations

- Version 0 is a prototype.
- The simple numerical validator is intentionally conservative and should be
  replaced by a stronger claim/evidence validator in Version 1.
- No product label/CCDS is supplied, so expectedness is out of scope.
- No history-of-actions data is supplied.
- No SOC field is supplied.
- No real regulatory submission workflow is implemented.
- No authentication or production infrastructure is implemented.

## 14. Version 1 direction

See `version1/design.md`.

The long-term goal is not to hard-code a PADER generator. It is to create a
small reporting engine where report types, sections, required analyses and
generation instructions are configuration-driven.

## Offline / no-paid-API mode

The project can generate an evidence-grounded PADER-style draft without calling a paid LLM. This is useful for local demonstrations when an OpenAI API account has no quota.

Run:

```bash
python -m src.main --csv "data/Bisoprolol_icsr_sample_1068rows.csv" --no-ai
```

This produces `analysis.json`, `evidence.json`, `validation.json`, `pader_report.md`, and `case_index.csv` in `output/`.

If the normal command is run without usable OpenAI API access, the CLI automatically falls back to the deterministic evidence-grounded report generator. The fallback is **not represented as an LLM-generated report**; it is a transparent template-based mode for demonstration and testing.

The supplied dataset stores `receivedate` as `YYYYMMDD` values, so the validation layer parses those dates explicitly to avoid accidental 1970 timestamps.
