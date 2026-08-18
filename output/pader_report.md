# PADER-Style Safety Report

## 1. Reporting Period

**Product:** Bisoprolol
**Reporting period:** 2024-12-27 to 2025-12-26
**Report type:** PADER-style technical evaluation report

## 2. Narrative Summary and Analysis

The supplied Bisoprolol safety dataset contains 1024 unique cases. The reporting period calculated from `receivedate` is 2024-12-27 to 2025-12-26. Of the unique cases, 1023 were classified as serious and 1 as non-serious. The most frequently reported reactions at Preferred Term level were Acute kidney injury (22); Drug ineffective (12); Cerebral haemorrhage (7); Hypokalaemia (6); Cholestasis (6). These are descriptive observations from the supplied dataset and do not by themselves establish a safety signal.

## 3. Summary Analysis of Cases

There were 1024 unique cases, including 1023 serious and 1 non-serious cases. Age-group distribution was: 75+: 408; 65-74: 267; 45-64: 204; Unknown: 84; 18-44: 45; <18: 16. Sex distribution was: female: 503; male: 493; Unknown: 28. The leading countries by case count were: eu: 325; united kingdom: 278; france: 187; canada: 55; italy: 52; germany: 39; spain: 26; poland: 21; portugal: 9; Unknown: 7. Reported reaction outcomes were: recovered/resolved: 147; recovering/resolving: 82; recovered/resolved,recovered/resolved: 76; not recovered/not resolved/ongoing: 67; unknown: 66; recovered/resolved,recovered/resolved,recovered/resolved: 52; unknown,unknown: 35; recovered/resolved,recovered/resolved,recovered/resolved,recovered/resolved: 29; recovering/resolving,recovering/resolving: 29; unknown,unknown,unknown: 23; fatal: 18; fatal,fatal: 18; not recovered/not resolved/ongoing,not recovered/not resolved/ongoing: 15; unknown,unknown,unknown,unknown: 14; recovered/resolved,recovered/resolved,recovered/resolved,recovered/resolved,recovered/resolved: 10.

## 4. Reaction / Adverse Event Analysis

Reaction analysis is performed at the supplied Preferred Term level. The most frequent reactions were Acute kidney injury (22); Drug ineffective (12); Cerebral haemorrhage (7); Hypokalaemia (6); Cholestasis (6); Hyponatraemia (6); Joint swelling (5); Hepatic cytolysis (5); Drug interaction (5); Pneumonitis (4). Among serious case IDs, the most frequent reactions were Acute kidney injury (22); Drug ineffective (12); Cerebral haemorrhage (7); Cholestasis (6); Hyponatraemia (6); Hypokalaemia (6); Drug interaction (5); Hepatic cytolysis (5); Joint swelling (5); Pneumonitis (4). System Organ Class groupings were not generated because SOC data were not supplied.

## 5. Serious Cases / 15-Day Alerts

The dataset contains 1023 unique case(s) with `fulfillexpeditecriteria` indicating an expedited/15-day criterion. This section reports the supplied field value only; it does not infer expectedness or create additional case narratives.

## 6. Trends and Important Observations

Monthly case counts derived from `receivedate` were: 2024-12: 21; 2025-01: 75; 2025-02: 94; 2025-03: 83; 2025-04: 78; 2025-05: 80; 2025-06: 84; 2025-07: 109; 2025-08: 64; 2025-09: 76; 2025-10: 102; 2025-11: 75; 2025-12: 83. Case volume increased from 21 in 2024-12 to 83 in 2025-12. These descriptive patterns should not be interpreted as confirmed safety signals.

## 7. History of Safety-Related Actions

No history-of-safety-related-actions dataset was supplied. Accordingly, no regulatory action, label change, communication, or other safety action is asserted in this report.

## 8. Case Index / Listing

A case-level CSV listing is generated alongside this report from unique `safetyreportid` records. It contains the case ID, reaction summary, seriousness, reporting date, country, and outcome summary where those fields are available in the supplied data.

## Technical Notes and Limitations

- Case-level counts use unique `safetyreportid`.
- Reaction-level counts use individual reaction rows.
- Country analysis consistently uses `occurcountry`.
- Expectedness is out of scope because no product label/CCDS was supplied.
- SOC analysis is out of scope because the dataset does not supply SOC.
- No history-of-actions information was supplied.

## Human Review

This report is a generated draft and requires human review before being treated as final.