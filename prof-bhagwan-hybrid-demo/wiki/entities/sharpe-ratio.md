---
type: entity
aliases: [Sharpe Ratio]
relationships:
  - target: sortino-ratio
    type: compared_with
  - target: one-sided-reporting-rule
    type: affected_by
tags: [performance-metric, finance, risk-adjusted-return]
sourced_from: Paper Cs26 Submission
---

# Sharpe Ratio

A performance metric whose denominator (total volatility) is compressed by strictly less than the misreporting intensity factor, causing it to be inflated less than the Sortino ratio under return smoothing.

## Relationships

- **compared_with**: [[sortino-ratio|Sortino Ratio]]
- **affected_by**: [[one-sided-reporting-rule|One Sided Reporting Rule]]

---
*Extracted from: Paper Cs26 Submission*