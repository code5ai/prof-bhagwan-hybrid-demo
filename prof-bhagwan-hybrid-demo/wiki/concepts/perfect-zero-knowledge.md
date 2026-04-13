---
type: concept
aliases: [Perfect Zero-Knowledge]
relationships:
  - target: zero-knowledge-proof
    type: is_a_type_of
  - target: grid-based-zkp-protocol
    type: is-property-of
tags: [cryptography, security-property, zero-knowledge]
sourced_from: Paper Zkp Full Paper
---

# Perfect Zero-Knowledge

A property of a ZKP where the verifier's view of the interaction is identically distributed to a simulated view, meaning the verifier gains absolutely zero information about the secret. A security property of the described protocol which guarantees that the verifier (the server) learns nothing about the user's password during authentication, not even computationally.

## Relationships

- **is_a_type_of**: [[zero-knowledge-proof|Zero Knowledge Proof]]
- **is-property-of**: [[grid-based-zkp-protocol|Grid Based Zkp Protocol]]

---
*Extracted from: Paper Zkp Full Paper*