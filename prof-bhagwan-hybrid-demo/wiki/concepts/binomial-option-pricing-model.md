---
type: concept
aliases: [Binomial Option Pricing Model]
relationships:
  - target: risk-neutral-probabilities
    type: uses
  - target: no-arbitrage-principle
    type: relies_on
  - target: random-walk-iid-assumption
    type: relies_on
  - target: black-scholes-formula
    type: converges_to
  - target: parameter-calibration
    type: requires
tags: [option-pricing, financial-modeling, numerical-method]
sourced_from: Mit15 401F08 Ses12 300K.Srt
---

# Binomial Option Pricing Model

A method for pricing options using a discrete-time tree of up and down movements over multiple periods, which converges to the Black-Scholes formula as the number of periods goes to infinity.

## Relationships

- **uses**: [[risk-neutral-probabilities|Risk Neutral Probabilities]]
- **relies_on**: [[no-arbitrage-principle|No Arbitrage Principle]]
- **relies_on**: [[random-walk-iid-assumption|Random Walk Iid Assumption]]
- **converges_to**: [[black-scholes-formula|Black Scholes Formula]]
- **requires**: [[parameter-calibration|Parameter Calibration]]

---
*Extracted from: Mit15 401F08 Ses12 300K.Srt*