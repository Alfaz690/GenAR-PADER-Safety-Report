# Version 1 Design

The Version 0 prototype is intentionally simple. Version 1 would make the system
report-type driven instead of hard-coding PADER behavior.

## 1. Report configuration

Example:

```yaml
report_type: PADER
sections:
  - name: narrative
    analyses: [case_summary, top_reactions, trends]
  - name: cases
    analyses: [case_summary, demographics, outcomes]
```

A future PSUR/PBRER/DSUR configuration could reuse the same analysis functions.

## 2. Reusable analysis registry

Instead of calling analysis code directly, register analyses:

```text
case_summary
demographics
reaction_frequency
outcomes
monthly_trend
alerts
```

Each report section declares which analyses it needs.

## 3. Evidence tracing

Store:

```text
report
 -> section
 -> claim
 -> evidence_id
 -> analysis
 -> source field
```

This would allow a reviewer to click a generated sentence and inspect its
supporting data.

## 4. Evaluation

Run many synthetic/reporting-period test cases and compare:

- numerical accuracy
- unsupported claims
- section completeness
- evidence traceability
- consistency with deterministic calculations

## 5. Previous-report comparison

A future version could compare two reporting periods and generate only
data-supported changes.
