---
type: entity
aliases: [Sortino Ratio]
relationships:
  - target: sharpe-ratio
    type: compared_with
  - target: one-sided-reporting-rule
    type: affected_by
  - target: lower-partial-moments
    type: uses
tags: [performance-metric, finance, risk-adjusted-return]
sourced_from: Paper Cs26 Submission
---

# Sortino Ratio

A performance metric that is inflated strictly more than the Sharpe ratio by return smoothing because its denominator (downside deviation) is compressed by the full factor of misreporting intensity.

## Relationships

- **compared_with**: [[sharpe-ratio|Sharpe Ratio]]
- **affected_by**: [[one-sided-reporting-rule|One Sided Reporting Rule]]
- **uses**: [[lower-partial-moments|Lower Partial Moments]]

---
*Extracted from: Paper Cs26 Submission*