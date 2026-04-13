---
type: entity
aliases: [Informed Trader]
relationships:
  - target: insider-surveillance-system
    type: is_deterred_by
  - target: liquidity-trader
    type: trades_against
tags: [market-participant, insider-trading]
sourced_from: Paper Mmtrading
---

# Informed Trader

A market participant whose aggressive trading strategy in one period can be made to adversely affect their expected profits in a subsequent period via an insider surveillance system.

## Relationships

- **is_deterred_by**: [[insider-surveillance-system|Insider Surveillance System]]
- **trades_against**: [[liquidity-trader|Liquidity Trader]]

---
*Extracted from: Paper Mmtrading*