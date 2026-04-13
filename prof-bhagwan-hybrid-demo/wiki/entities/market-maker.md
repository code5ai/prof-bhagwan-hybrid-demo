---
type: entity
aliases: [Market Maker]
relationships:
  - target: insider-surveillance-system
    type: can_institute
  - target: market-liquidity-parameter-lambda
    type: sets
  - target: zero-expected-profits
    type: operates_under
tags: [market-participant, market-microstructure]
sourced_from: Paper Mmtrading
---

# Market Maker

A market participant who sets the liquidity parameter (λ) and can voluntarily institute an insider surveillance system to achieve zero-expected profits.

## Relationships

- **can_institute**: [[insider-surveillance-system|Insider Surveillance System]]
- **sets**: [[market-liquidity-parameter-lambda|Market Liquidity Parameter Lambda]]
- **operates_under**: [[zero-expected-profits|Zero Expected Profits]]

---
*Extracted from: Paper Mmtrading*