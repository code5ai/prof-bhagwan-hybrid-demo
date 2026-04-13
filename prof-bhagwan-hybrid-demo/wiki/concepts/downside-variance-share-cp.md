---
type: concept
aliases: [Downside Variance Share (Cp)]
relationships:
  - target: identification-hierarchy
    type: is_used_in
  - target: reporting-put
    type: is_a_signature_of
  - target: policy-put
    type: is_a_signature_of
  - target: fixed-target-downside-variance-share
    type: is_estimated_by
tags: [econometrics, statistic, misreporting, identification]
sourced_from: Paper Cs26 Submission
---

# Downside Variance Share (Cp)

A statistic, also denoted C_rho, that measures the share of variance from outcomes below a threshold, used as the key identifying statistic to detect one-sided smoothing. A value less than 0.5 is a signature of a reporting put, while a value near 0.5 is a signature of a resource-constrained policy put.

## Relationships

- **is_used_in**: [[identification-hierarchy|Identification Hierarchy]]
- **is_a_signature_of**: [[reporting-put|Reporting Put]]
- **is_a_signature_of**: [[policy-put|Policy Put]]
- **is_estimated_by**: [[fixed-target-downside-variance-share|Fixed Target Downside Variance Share]]

---
*Extracted from: Paper Cs26 Submission*