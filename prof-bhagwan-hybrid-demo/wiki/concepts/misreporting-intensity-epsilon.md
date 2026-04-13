---
type: concept
aliases: [Misreporting Intensity (ε)]
relationships:
  - target: cp-test
    type: is_detected_by
  - target: sortino-ratio
    type: inflates
  - target: sharpe-ratio
    type: inflates
  - target: lower-partial-moment-lpm
    type: affects
tags: [parameter, misreporting, statistics]
sourced_from: Paper Cs26 Submission
---

# Misreporting Intensity (ε)

A parameter that quantifies the magnitude of one-sided misreporting, where a certain percentage of below-threshold outcomes are shifted above the threshold.

## Relationships

- **is_detected_by**: [[cp-test|Cp Test]]
- **inflates**: [[sortino-ratio|Sortino Ratio]]
- **inflates**: [[sharpe-ratio|Sharpe Ratio]]
- **affects**: [[lower-partial-moment-lpm|Lower Partial Moment Lpm]]

---
*Extracted from: Paper Cs26 Submission*