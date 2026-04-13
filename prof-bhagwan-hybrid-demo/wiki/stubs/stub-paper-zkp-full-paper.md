---
type: stub
aliases: [Paper Zkp Full Paper, ZKP Password Authentication, Chowdhry Sharma ZKP]
relationships: []
tags: [rag-stub]
rag_source: prof-bhagwan-hybrid-demo\raw\papers\paper-zkp_full_paper.md
rag_chunks: 16
---

# Paper Zkp Full Paper

**Type**: RAG stub — full content in vector index, not in wiki

## Abstract

This paper by Bhagwan Chowdhry and Vasundhara Sharma (Indian School of Business, November 2022, revised March 2026) proposes a novel zero-knowledge proof (ZKP) protocol for password authentication that allows a user to prove knowledge of her password without ever writing, typing, or transmitting it. The protocol is built on a physical grid of colored and numbered balls and requires no special hardware for its digital implementation. The paper's main technical contribution is a complete information-theoretic analysis of eavesdropper resistance, using Fano's inequality and a maximum-likelihood achievability argument, establishing that resistance improves strictly with the number of password balls up to a remarkably large optimum. The work bridges the gap between cryptographic rigor and practical usability that has limited adoption of prior ZKP-based password protocols.

## Key Claims

- The protocol enables authentication without the user ever writing, typing, or transmitting her password, achieving zero-knowledge properties against the verifier
- A complete information-theoretic analysis of eavesdropper resistance is provided using Fano's inequality and a maximum-likelihood achievability argument — claimed to be the first such analysis for a ZKP-based password protocol of this type
- Eavesdropper resistance improves strictly (monotonically) with the number of password balls, up to a remarkably large optimum, yielding concrete design recommendations
- The user's memory task (two numbers and two colors from a grid) is comparable to a four-digit PIN but provides information-theoretic guarantees that PIN-based systems lack
- The protocol exploits the well-documented superiority of visual/spatial memory over verbal memory, sharing cognitive grounding with graphical password systems while adding formal ZKP properties they generally lack

## Topics Covered

Zero-knowledge proof protocols, password authentication, eavesdropper resistance analysis, Fano's inequality, maximum-likelihood achievability, information-theoretic security, colored ball grid mechanism, digital implementation architecture, graphical password systems, cognitive usability of authentication, setup and verification phases, design recommendations for password ball count

## How to Query

> "Explain the zero-knowledge proof password authentication protocol from Paper Zkp Full Paper"
> "What does Paper Zkp Full Paper say about eavesdropper resistance and Fano's inequality?"
> "How does the colored ball grid mechanism work in Paper Zkp Full Paper?"
> "What design recommendations does Paper Zkp Full Paper give for the number of password balls?"
> "What does Paper Zkp Full Paper say about the digital implementation architecture?"

---
*RAG stub — 16 chunks indexed. Source: `prof-bhagwan-hybrid-demo\raw\papers\paper-zkp_full_paper.md`*
