---
type: concept
aliases: [Forward Contract]
relationships:
  - target: forward-price
    type: has_component
  - target: long-position
    type: involves
  - target: short-position
    type: involves
  - target: hedging
    type: is_used_for
  - target: counterparty-risk
    type: has_risk
  - target: illiquidity
    type: has_characteristic
  - target: physical-delivery
    type: can_involve
  - target: futures-contract
    type: is_alternative_to
  - target: spot-price
    type: value_is_based_on
  - target: futures-contract
    type: is_contrasted_with
tags: [financial-instrument, derivative, contract, derivatives, risk-management, otc]
sourced_from: Mit15 401F08 Ses09 300K.Srt
---

# Forward Contract

A customized, nonstandard, and legally binding agreement between two parties to exchange an asset at a specified future date for a price agreed upon today, which has a value of zero at inception and requires no money down. A private contract between two parties, a buyer and a seller, to exchange a commodity at an agreed-upon price on a future date. A financial agreement where two parties agree on a price for a future transaction but do not mark to market daily and have no intermediary, allowing the contract's value to fluctuate until settlement.

## Relationships

- **has_component**: [[forward-price|Forward Price]]
- **involves**: [[long-position|Long Position]]
- **involves**: [[short-position|Short Position]]
- **is_used_for**: [[hedging|Hedging]]
- **has_risk**: [[counterparty-risk|Counterparty Risk]]
- **has_characteristic**: [[illiquidity|Illiquidity]]
- **can_involve**: [[physical-delivery|Physical Delivery]]
- **is_alternative_to**: [[futures-contract|Futures Contract]]
- **value_is_based_on**: [[spot-price|Spot Price]]
- **is_contrasted_with**: [[futures-contract|Futures Contract]]

---
*Extracted from: Mit15 401F08 Ses09 300K.Srt*

---
*Also referenced in: Mit15 401F08 Ses10 300K.Srt*