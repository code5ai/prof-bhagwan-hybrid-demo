---
type: entity
aliases: [Federal Agency Securities]
relationships:
  - target: fixed-income-securities
    type: is_a
  - target: fannie-mae
    type: is_issued_by
  - target: freddie-mac
    type: is_issued_by
tags: [agency-debt, financial-instrument]
sourced_from: Mit15 401F08 Ses04 300K.Srt
---

# Federal Agency Securities

A segment of the fixed income market issued by government-sponsored entities like Fannie Mae and Freddie Mac that experienced significant growth.

## Relationships

- **is_a**: [[fixed-income-securities|Fixed Income Securities]]
- **is_issued_by**: [[fannie-mae|Fannie Mae]]
- **is_issued_by**: [[freddie-mac|Freddie Mac]]

---
*Extracted from: Mit15 401F08 Ses04 300K.Srt*