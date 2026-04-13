---
type: entity
aliases: [Bitcoin Blockchain]
relationships:
  - target: bitcoin
    type: is_ledger_for
  - target: sha-256
    type: uses
  - target: nakamoto-consensus
    type: uses
  - target: proof-of-work
    type: uses
  - target: double-sha-256
    type: uses
tags: [blockchain, distributed-ledger, bitcoin, cryptocurrency]
sourced_from: Book Blockchain By Chowdhry And Kim   Palgrave Handbook Of Technological Finance (1)
---

# Bitcoin Blockchain

The specific distributed ledger for Bitcoin, where miners compete to find a winning "nonce" to close out a block of transaction records and add it to the chain. A trustless, permissionless ledger secured by a hashcash-based proof-of-work protocol and the double SHA-256 hash function.

## Relationships

- **is_ledger_for**: [[bitcoin|Bitcoin]]
- **uses**: [[sha-256|Sha 256]]
- **uses**: [[nakamoto-consensus|Nakamoto Consensus]]
- **uses**: [[proof-of-work|Proof Of Work]]
- **uses**: [[double-sha-256|Double Sha 256]]

---
*Extracted from: Book Blockchain By Chowdhry And Kim   Palgrave Handbook Of Technological Finance (1)*