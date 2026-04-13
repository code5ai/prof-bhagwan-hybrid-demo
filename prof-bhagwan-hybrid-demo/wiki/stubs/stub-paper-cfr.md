---
type: stub
aliases: [Paper Cfr, How Should Firms Hedge Market Risk]
relationships: []
tags: [rag-stub]
rag_source: prof-bhagwan-hybrid-demo\raw\papers\paper-CFR.md
rag_chunks: 14
---

# Paper Cfr

**Type**: RAG stub — full content in vector index, not in wiki

## Abstract

This paper by Bhagwan Chowdhry and Eduardo Schwartz, published in the *Critical Finance Review* (2016), examines how firms should optimally hedge market risk. The authors show that while a large hedge against the market index minimizes the variance of cash flows, it does not minimize the costs of financial distress associated with low cash flow realizations, because multiple sources of uncertainty interact multiplicatively in determining the level of future cash flows. The paper demonstrates that the optimal market hedge is much more conservative than the textbook beta-based hedge ratio, and in their example, with $15 of debt, the optimal hedge is only $15 rather than the full $100 of market risk exposure. This result challenges the standard recommendation of using regression-based beta as the optimal hedge ratio.

## Key Claims

- The textbook approach of using the regression beta as the optimal hedge ratio is incorrect when the goal is to minimize financial distress costs rather than return variance
- Different sources of uncertainty (market and idiosyncratic) affect a firm's cash flow levels multiplicatively due to compounding, even when they appear additively separable in short-horizon stock returns
- A large market hedge can actually worsen the worst-case cash flow outcome, potentially causing bankruptcy in states where the firm would otherwise survive unhedged
- The optimal market hedge is much more conservative than hedging the full market-risk exposure, scaled to the firm's debt level rather than its total market exposure
- Few firms in practice hedge by shorting the market index, consistent with the paper's finding that full market hedging is suboptimal — a fact Fischer Black noted as "embarrassing" for standard theory

## Topics Covered

Optimal hedging, market risk, financial distress costs, beta hedge ratio, multiplicative compounding of risk factors, idiosyncratic risk, variance minimization vs. distress minimization, forward contracts on market index, corporate risk management, cash flow variability, short-run return dynamics, debt and bankruptcy thresholds

## How to Query

> "Explain the optimal market hedge ratio from Paper Cfr"
> "What does Paper Cfr say about why beta is not the correct hedge ratio?"
> "How does multiplicative compounding affect hedging decisions in Paper Cfr?"
> "What is the financial distress argument against full market hedging in Paper Cfr?"

---
*RAG stub — 14 chunks indexed. Source: `prof-bhagwan-hybrid-demo\raw\papers\paper-CFR.md`*
