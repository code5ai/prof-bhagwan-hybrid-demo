---
type: stub
aliases: [Paper Cs26 Submission, Detecting Lies When Truth is Unobservable]
relationships: []
tags: [rag-stub]
rag_source: prof-bhagwan-hybrid-demo\raw\papers\paper-CS26_Submission.md
rag_chunks: 32
---

# Paper Cs26 Submission

**Type**: RAG stub — full content in vector index, not in wiki

## Abstract

This working paper by Bhagwan Chowdhry (ISB/UCLA) and Konark Saxena (ESCP Business School), dated March 2026, develops a statistical framework for detecting manipulation in reported outcomes when the true values are unobservable. The core insight is that when agents hide bad outcomes, downside variation shrinks faster than total variation, leaving a detectable statistical fingerprint. The authors formalise two compression statistics—C_σ (volatility compression) and C_p (ratio of downside semivariance to total variance)—and show that mean-based tests have no power because the reporting bias is indistinguishable from a higher true mean. The framework is applied to settings including hedge fund returns, GDP reporting by autocratic governments, and other contexts where external benchmarks are unavailable.

## Key Claims

- Agents who hide bad outcomes leave a statistical fingerprint: downside variation shrinks faster than total variation, enabling detection even when truth is unobservable
- Two compression statistics are formalised: C_σ (standard deviation of reported outcomes measuring volatility compression) and C_p (bounded downside variance share), where C_p falls strictly below one-half under a one-sided reporting put applied to a symmetric distribution
- The reporting bias equals ε times the put-option premium struck at the embarrassment threshold τ, making the put-option framing analytically precise rather than merely metaphorical
- Mean-based tests carry no power because an outside observer seeing only E[Y] cannot distinguish a dishonest agent with true mean μ from an honest agent whose true mean happens to equal E[Y]
- A key empirical challenge is distinguishing a "reporting put" (agent smooths reported numbers without changing reality) from a "policy put" (genuine intervention compresses true outcomes before reporting), which Proposition 5 addresses

## Topics Covered

One-sided reporting rule and misreporting intensity, compression statistics (C_σ and C_p), put-option analogy for reporting bias, fat-tailed distributions and manipulation detection, hedge fund return smoothing and illiquidity, GDP manipulation in autocratic regimes, bunching and density discontinuity methods, reporting put vs policy put identification, downside semivariance analysis, variance-based fraud detection, benchmark-free manipulation tests, symmetric distribution properties under manipulation

## How to Query

> "Explain the compression statistics C_σ and C_p from Paper Cs26 Submission"
> "What does Paper Cs26 Submission say about distinguishing reporting puts from policy puts?"
> "How does the one-sided reporting rule work in Detecting Lies When Truth is Unobservable?"
> "What does Paper Cs26 Submission say about why mean-based tests fail to detect manipulation?"
> "How does Paper Cs26 Submission apply to hedge fund return manipulation?"

---
*RAG stub — 32 chunks indexed. Source: `prof-bhagwan-hybrid-demo\raw\papers\paper-CS26_Submission.md`*
