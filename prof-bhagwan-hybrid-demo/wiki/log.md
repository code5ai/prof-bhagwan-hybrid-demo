# Wiki Log

Append-only chronological record of ingests and queries.

---
## [2026-04-09] consistency_test | Op 2
## [2026-04-09] consistency_test | Op 1
## [2026-04-09] consistency_test | Op 0
## [2026-04-09] ingest | Test-Source
- pages_created: ["p1"]
- chunks: 100
## [2026-04-09] timestamp_test | Check timestamp
## [2026-04-09] test | ok
## [2026-04-09] test | None
## [2026-04-09] test | 
## [2026-04-09] test | List test
- pages: ["p1", "p2"]
## [2026-04-09] multi2 | Entry B
## [2026-04-09] multi1 | Entry A
## [2026-04-09] append_test | Should not overwrite
## [2026-04-09] test | Metadata Test
- key: value
## [2026-04-09] test | Format Check

## [2026-04-08] ingest | Full corpus — initial build

- Route: RAG (combined index) for all 17 files
- Books (5 .md files): Financial Modeling, Introductory Econometrics, Corporate Finance, Principles of Risk Management, Guide to Econometrics
- Research Papers (11 PDFs): Assessing Project Risk, Defaults and Interest Rates, Digital Identity in India, Exchange Risk Management, Information Aggregation (2 papers), International Debt Crisis, Organization Capital, Pricing Microfinance Loans, Transactions Costs, Why Real Interest Rates Vary
- Profile: prof-bhagwan-chowdhry_knowledge_base.md
- Total chunks: 5,760 (all with 3072-dim gemini-embedding-2-preview embeddings)
- PDFs converted to markdown in raw/research_papers_md/

## [2026-04-08] ingest | Wiki pages from profile

- Route: Wiki (full ingest) from digital profile
- Pages created: prof-bhagwan-chowdhry.md, financial-access-at-birth.md, fintech-for-billions.md, impact-investing.md, digital-identity-and-aadhaar.md, blockchain-and-digital-currencies.md, academic-freedom-and-university-governance.md
- index.md updated with all pages and RAG stubs

## [2026-04-08] wiki-redesign | Three-pass tacit knowledge extraction

- Route: Wiki (full redesign) — deep analysis of profile + research papers using tacit knowledge externalization methodology
- Pages deleted: financial-access-at-birth.md, fintech-for-billions.md, impact-investing.md, digital-identity-and-aadhaar.md, blockchain-and-digital-currencies.md, academic-freedom-and-university-governance.md
- Pages created (persona/ subfolder): thinking-patterns-and-frameworks.md, intellectual-evolution.md, financial-inclusion-architecture.md, mechanism-design-applied.md, rhetorical-style-and-pedagogy.md, mentor-network-and-influences.md, fame-and-knowledge-democratization.md
- Pages redesigned: prof-bhagwan-chowdhry.md (expanded from 55 to ~200 lines with intellectual DNA, tacit knowledge links)
- Pages updated: index.md (new structure with persona/ subfolder), log.md (this entry)
- Methodology: Three-pass analysis — Pass 1: content selection patterns (core convictions, signature examples, deliberate omissions), Pass 2: pedagogical sequencing (counterintuitive inversions, concrete arithmetic, multi-level treatment), Pass 3: underlying philosophy (mechanism design as unifying framework, SHUb as design standard, incentive-first lens)

## [2026-04-08 21:19 IST] ingest | Valuation Approaches and Metrics — Aswath Damodaran

- Route: RAG + wiki stub (31,224 words, exceeds 5,000-word threshold)
- Source: raw/books/Valuation-Damodaran_content.md
- Chunks: 70 (500-word windows, 50-word overlap, gemini-embedding-2-preview 3072-dim)
- Stub created: stub-valuation-damodaran.md
- Total RAG chunks: 5,830 (5,760 existing + 70 new)
- Index updated: added under RAG Stubs > Books

## [2026-04-09] test | Test entry creation

## [2026-04-09] ingest | Test Format Check

## [2026-04-09] ingest | Test Metadata
- pages: 5
- sources: ["test1", "test2"]

## [2026-04-09] query | Test Append

## [2026-04-09] ingest | Entry 1

## [2026-04-09] query | Entry 2

## [2026-04-09] ingest | Entry 3

## [2026-04-09] ingest | Test Dict
- pages_created: ["page1", "page2"]
- chunks: 100
- config: {"route": "RAG+stub"}

## [2026-04-09] test | None

## [2026-04-09] test | 

## [2026-04-09] test | ok

## [2026-04-09] test | Timestamp test

## [2026-04-09] ingest | Valuation-Damodaran
- route: RAG+stub
- pages_created: ["dcf.md", "wacc.md"]
- chunks: 150

## [2026-04-09] test | Entry 0

## [2026-04-09] test | Entry 1

## [2026-04-09] test | Entry 2

## [2026-04-09] test | Entry 3

## [2026-04-09] test | Entry 4

## [2026-04-09] test | Format Check

## [2026-04-09] test | Metadata Test
- key: value

## [2026-04-09] append_test | Should not overwrite

## [2026-04-09] multi1 | Entry A

## [2026-04-09] multi2 | Entry B

## [2026-04-09] test | List test
- pages: ["p1", "p2"]

## [2026-04-09] test | 

## [2026-04-09] test | None

## [2026-04-09] test | ok

## [2026-04-09] timestamp_test | Check timestamp

## [2026-04-09] ingest | Test-Source
- pages_created: ["p1"]
- chunks: 100

## [2026-04-09] consistency_test | Op 0

## [2026-04-09] consistency_test | Op 1

## [2026-04-09] consistency_test | Op 2

## [2026-04-09] test | Format Check

## [2026-04-09] test | Metadata Test
- key: value

## [2026-04-09] append_test | Should not overwrite

## [2026-04-09] multi1 | Entry A

## [2026-04-09] multi2 | Entry B

## [2026-04-09] test | List test
- pages: ["p1", "p2"]

## [2026-04-09] test | 

## [2026-04-09] test | None

## [2026-04-09] test | ok

## [2026-04-09] timestamp_test | Check timestamp

## [2026-04-09] ingest | Test-Source
- pages_created: ["p1"]
- chunks: 100

## [2026-04-09] consistency_test | Op 0

## [2026-04-09] consistency_test | Op 1

## [2026-04-09] consistency_test | Op 2

## [2026-04-09] test | Test entry creation

## [2026-04-09] ingest | Test Format Check

## [2026-04-09] ingest | Test Metadata
- pages: 5
- sources: ["test1", "test2"]

## [2026-04-09] query | Test Append

## [2026-04-09] ingest | Entry 1

## [2026-04-09] query | Entry 2

## [2026-04-09] ingest | Entry 3

## [2026-04-09] ingest | Test Dict
- pages_created: ["page1", "page2"]
- chunks: 100
- config: {"route": "RAG+stub"}

## [2026-04-09] test | None

## [2026-04-09] test | 

## [2026-04-09] test | ok

## [2026-04-09] test | Timestamp test

## [2026-04-09 18:27:29 UTC] query | What is CAPM?
- pages_consulted: ["capm.md", "risk.md"]
- wiki_updated: False

## [2026-04-09] ingest | Valuation-Damodaran
- route: RAG+stub
- pages_created: ["dcf.md", "wacc.md"]
- chunks: 150

## [2026-04-09] test | Entry 0

## [2026-04-09] test | Entry 1

## [2026-04-09] test | Entry 2

## [2026-04-09] test | Entry 3

## [2026-04-09] test | Entry 4

## [2026-04-09] test | Test entry creation

## [2026-04-09] ingest | Test Format Check

## [2026-04-09] ingest | Test Metadata
- pages: 5
- sources: ["test1", "test2"]

## [2026-04-09] query | Test Append

## [2026-04-09] ingest | Entry 1

## [2026-04-09] query | Entry 2

## [2026-04-09] ingest | Entry 3

## [2026-04-09] ingest | Test Dict
- pages_created: ["page1", "page2"]
- chunks: 100
- config: {"route": "RAG+stub"}

## [2026-04-09] test | None

## [2026-04-09] test | 

## [2026-04-09] test | ok

## [2026-04-09] test | Timestamp test

## [2026-04-09 18:43:58 UTC] query | What is CAPM?
- pages_consulted: ["capm.md", "risk.md"]
- wiki_updated: False

## [2026-04-09] ingest | Valuation-Damodaran
- route: RAG+stub
- pages_created: ["dcf.md", "wacc.md"]
- chunks: 150

## [2026-04-09] test | Entry 0

## [2026-04-09] test | Entry 1

## [2026-04-09] test | Entry 2

## [2026-04-09] test | Entry 3

## [2026-04-09] test | Entry 4

## [2026-04-09] test | Test entry creation

## [2026-04-09] ingest | Test Format Check

## [2026-04-09] ingest | Test Metadata
- pages: 5
- sources: ["test1", "test2"]

## [2026-04-09] query | Test Append

## [2026-04-09] ingest | Entry 1

## [2026-04-09] query | Entry 2

## [2026-04-09] ingest | Entry 3

## [2026-04-09] ingest | Test Dict
- pages_created: ["page1", "page2"]
- chunks: 100
- config: {"route": "RAG+stub"}

## [2026-04-09] test | None

## [2026-04-09] test | 

## [2026-04-09] test | ok

## [2026-04-09] test | Timestamp test

## [2026-04-09 18:54:07 UTC] query | What is CAPM?
- pages_consulted: ["capm.md", "risk.md"]
- wiki_updated: False

## [2026-04-09] ingest | Valuation-Damodaran
- route: RAG+stub
- pages_created: ["dcf.md", "wacc.md"]
- chunks: 150

## [2026-04-09] test | Entry 0

## [2026-04-09] test | Entry 1

## [2026-04-09] test | Entry 2

## [2026-04-09] test | Entry 3

## [2026-04-09] test | Entry 4

## [2026-04-13 22:20 IST] ingest | Book Blockchain By Chowdhry And Kim   Palgrave Handbook Of Technological Finance (1)
- source: prof-bhagwan-hybrid-demo\raw\books\book-Blockchain by Chowdhry and KIm - Palgrave Handbook of Technological Finance (1).md
- chunks: 15
- words: 6461

## [2026-04-13 22:20 IST] ingest | Book Blockchain By Chowdhry And Kim   Palgrave Handbook Of Technological Finance (2)
- source: prof-bhagwan-hybrid-demo\raw\books\book-Blockchain by Chowdhry and KIm - Palgrave Handbook of Technological Finance (2).md
- chunks: 108
- words: 48396

## [2026-04-13 22:20 IST] ingest | Paper Bhag Submission
- source: prof-bhagwan-hybrid-demo\raw\papers\paper-bhag_submission.md
- chunks: 13
- words: 5776

## [2026-04-13 22:20 IST] ingest | Paper Cfr
- source: prof-bhagwan-hybrid-demo\raw\papers\paper-CFR.md
- chunks: 14
- words: 5904

## [2026-04-13 22:20 IST] ingest | Paper Cs26 Submission
- source: prof-bhagwan-hybrid-demo\raw\papers\paper-CS26_Submission.md
- chunks: 32
- words: 14391

## [2026-04-13 22:20 IST] ingest | Paper Intlending
- source: prof-bhagwan-hybrid-demo\raw\papers\paper-IntLending.md
- chunks: 25
- words: 10825

## [2026-04-13 22:20 IST] ingest | Paper Investing For Impact
- source: prof-bhagwan-hybrid-demo\raw\papers\paper-Investing for Impact.md
- chunks: 40
- words: 17633

## [2026-04-13 22:20 IST] ingest | Paper Mmtrading
- source: prof-bhagwan-hybrid-demo\raw\papers\paper-MMTrading.md
- chunks: 24
- words: 10710

## [2026-04-13 22:20 IST] ingest | Paper Repurchase
- source: prof-bhagwan-hybrid-demo\raw\papers\paper-Repurchase.md
- chunks: 26
- words: 11398

## [2026-04-13 22:20 IST] ingest | Paper Rigged Economies Mssubmission
- source: prof-bhagwan-hybrid-demo\raw\papers\paper-Rigged_Economies_MSsubmission.md
- chunks: 43
- words: 18962

## [2026-04-13 22:20 IST] ingest | Paper Rnd
- source: prof-bhagwan-hybrid-demo\raw\papers\paper-RnD.md
- chunks: 30
- words: 13212

## [2026-04-13 22:20 IST] ingest | Paper Thresholds
- source: prof-bhagwan-hybrid-demo\raw\papers\paper-thresholds.md
- chunks: 16
- words: 7187

## [2026-04-13 22:20 IST] ingest | Paper Which Firms Innovate V3
- source: prof-bhagwan-hybrid-demo\raw\papers\paper-which_firms_innovate_v3.md
- chunks: 24
- words: 10402

## [2026-04-13 22:21 IST] ingest | Paper Zkp Full Paper
- source: prof-bhagwan-hybrid-demo\raw\papers\paper-zkp_full_paper.md
- chunks: 16
- words: 7185

## [2026-04-13 22:21 IST] ingest | In Pursuit Of The Perfect Porfolio William F Sharpe Xsxolz9U7Ji
- source: prof-bhagwan-hybrid-demo\raw\videos\In_Pursuit_of_the_Perfect_Porfolio_William_F_Sharpe_XsXOLZ9U7jI.md
- chunks: 17
- words: 7345

## [2026-04-13 22:21 IST] ingest | In Pursuit Of The Perfect Portfolio Charles D Ellis Fve3Djvygju
- source: prof-bhagwan-hybrid-demo\raw\videos\In_Pursuit_of_the_Perfect_Portfolio_Charles_D_Ellis_FvE3djVyGjU.md
- chunks: 19
- words: 8215

## [2026-04-13 22:21 IST] ingest | In Pursuit Of The Perfect Portfolio Harry M Markowitz Wdeoipcftdu
- source: prof-bhagwan-hybrid-demo\raw\videos\In_Pursuit_of_the_Perfect_Portfolio_Harry_M_Markowitz_wdeoIPCFtDU.md
- chunks: 13
- words: 5436

## [2026-04-13 22:21 IST] ingest | In Pursuit Of The Perfect Portfolio Jeremy Siegel 2Fwe5Bvzu C
- source: prof-bhagwan-hybrid-demo\raw\videos\In_Pursuit_of_the_Perfect_Portfolio_Jeremy_Siegel_2Fwe5bvZu_c.md
- chunks: 16
- words: 7125

## [2026-04-13 22:21 IST] ingest | In Pursuit Of The Perfect Portfolio John C Bogle 3Ujbhremus4
- source: prof-bhagwan-hybrid-demo\raw\videos\In_Pursuit_of_the_Perfect_Portfolio_John_C_Bogle_3uJbHREmUs4.md
- chunks: 23
- words: 9935

## [2026-04-13 22:21 IST] ingest | In Pursuit Of The Perfect Portfolio Martin L Leibowitz Jpcc8Ho5Zns
- source: prof-bhagwan-hybrid-demo\raw\videos\In_Pursuit_of_the_Perfect_Portfolio_Martin_L_Leibowitz_jpcC8ho5Zns.md
- chunks: 15
- words: 6374

## [2026-04-13 22:21 IST] ingest | In Pursuit Of The Perfect Portfolio Myron S Scholes D5Mdcrwxmgy
- source: prof-bhagwan-hybrid-demo\raw\videos\In_Pursuit_of_the_Perfect_Portfolio_Myron_S_Scholes_D5mDcrwxmgY.md
- chunks: 19
- words: 8543

## [2026-04-13 22:21 IST] ingest | In Pursuit Of The Perfect Portfolio Robert C Merton Ipkmu59Ub4C
- source: prof-bhagwan-hybrid-demo\raw\videos\In_Pursuit_of_the_Perfect_Portfolio_Robert_C_Merton_iPKmU59ub4c.md
- chunks: 16
- words: 7188

## [2026-04-13 22:21 IST] ingest | Mit15 401F08 Ses01 300K.Srt
- source: prof-bhagwan-hybrid-demo\raw\videos\MIT15_401F08_ses01_300k.srt.md
- chunks: 24
- words: 10752

## [2026-04-13 22:21 IST] ingest | Mit15 401F08 Ses02 300K.Srt
- source: prof-bhagwan-hybrid-demo\raw\videos\MIT15_401F08_ses02_300k.srt.md
- chunks: 28
- words: 12402

## [2026-04-13 22:21 IST] ingest | Mit15 401F08 Ses03 300K.Srt
- source: prof-bhagwan-hybrid-demo\raw\videos\MIT15_401F08_ses03_300k.srt.md
- chunks: 27
- words: 12139

## [2026-04-13 22:22 IST] ingest | Mit15 401F08 Ses04 300K.Srt
- source: prof-bhagwan-hybrid-demo\raw\videos\MIT15_401F08_ses04_300k.srt.md
- chunks: 26
- words: 11326

## [2026-04-13 22:22 IST] ingest | Mit15 401F08 Ses05 300K.Srt
- source: prof-bhagwan-hybrid-demo\raw\videos\MIT15_401F08_ses05_300k.srt.md
- chunks: 28
- words: 12494

## [2026-04-13 22:22 IST] ingest | Mit15 401F08 Ses06 300K.Srt
- source: prof-bhagwan-hybrid-demo\raw\videos\MIT15_401F08_ses06_300k.srt.md
- chunks: 29
- words: 12979

## [2026-04-13 22:22 IST] ingest | Mit15 401F08 Ses07 300K.Srt
- source: prof-bhagwan-hybrid-demo\raw\videos\MIT15_401F08_ses07_300k.srt.md
- chunks: 26
- words: 11575

## [2026-04-13 22:22 IST] ingest | Mit15 401F08 Ses08 300K.Srt
- source: prof-bhagwan-hybrid-demo\raw\videos\MIT15_401F08_ses08_300k.srt.md
- chunks: 28
- words: 12308

## [2026-04-13 22:22 IST] ingest | Mit15 401F08 Ses09 300K.Srt
- source: prof-bhagwan-hybrid-demo\raw\videos\MIT15_401F08_ses09_300k.srt.md
- chunks: 29
- words: 12949

## [2026-04-13 22:22 IST] ingest | Mit15 401F08 Ses10 300K.Srt
- source: prof-bhagwan-hybrid-demo\raw\videos\MIT15_401F08_ses10_300k.srt.md
- chunks: 27
- words: 12003

## [2026-04-13 22:22 IST] ingest | Mit15 401F08 Ses11 300K.Srt
- source: prof-bhagwan-hybrid-demo\raw\videos\MIT15_401F08_ses11_300k.srt.md
- chunks: 21
- words: 9445

## [2026-04-13 22:23 IST] ingest | Mit15 401F08 Ses12 300K.Srt
- source: prof-bhagwan-hybrid-demo\raw\videos\MIT15_401F08_ses12_300k.srt.md
- chunks: 23
- words: 10306

## [2026-04-13 22:23 IST] ingest | Mit15 401F08 Ses13 300K.Srt
- source: prof-bhagwan-hybrid-demo\raw\videos\MIT15_401F08_ses13_300k.srt.md
- chunks: 27
- words: 12102

## [2026-04-13 22:23 IST] ingest | Mit15 401F08 Ses14 300K.Srt
- source: prof-bhagwan-hybrid-demo\raw\videos\MIT15_401F08_ses14_300k.srt.md
- chunks: 28
- words: 12560

## [2026-04-13 22:23 IST] ingest | Mit15 401F08 Ses15 300K.Srt
- source: prof-bhagwan-hybrid-demo\raw\videos\MIT15_401F08_ses15_300k.srt.md
- chunks: 28
- words: 12580

## [2026-04-13 22:23 IST] ingest | Mit15 401F08 Ses16 300K.Srt
- source: prof-bhagwan-hybrid-demo\raw\videos\MIT15_401F08_ses16_300k.srt.md
- chunks: 27
- words: 11814

## [2026-04-13 22:23 IST] ingest | Mit15 401F08 Ses17 300K.Srt
- source: prof-bhagwan-hybrid-demo\raw\videos\MIT15_401F08_ses17_300k.srt.md
- chunks: 30
- words: 13052

## [2026-04-13 22:23 IST] ingest | Mit15 401F08 Ses18 300K.Srt
- source: prof-bhagwan-hybrid-demo\raw\videos\MIT15_401F08_ses18_300k.srt.md
- chunks: 29
- words: 12883

## [2026-04-13 22:23 IST] ingest | Mit15 401F08 Ses19 300K.Srt
- source: prof-bhagwan-hybrid-demo\raw\videos\MIT15_401F08_ses19_300k.srt.md
- chunks: 29
- words: 12997

## [2026-04-13 22:23 IST] ingest | Mit15 401F08 Ses20 300K.Srt
- source: prof-bhagwan-hybrid-demo\raw\videos\MIT15_401F08_ses20_300k.srt.md
- chunks: 19
- words: 8376

## [2026-04-13 22:26 IST] ingest | In Pursuit Of The Perfect Porfolio William F Sharpe Xsxolz9U7Ji
- route: RAG+stub
- pages_created: ["passive-investing", "capital-asset-pricing-model", "portfolio-optimization", "single-index-model", "market-portfolio", "accumulation-phase", "decumulation-phase", "robo-advisor", "reverse-optimization", "index-funds", "expense-ratios", "market-equilibrium", "rebalancing", "adaptive-asset-allocation", "saving", "longevity", "william-sharpe", "harry-markowitz", "john-mcquown", "fred-weston", "financial-engines", "index-fund", "rand-corporation", "ucla", "wells-fargo", "fischer-black", "bob-litterman", "capm", "vanguard", "ftse-index", "crsp-index", "barclays-indices", "social-security"]
- chunks: 17

## [2026-04-13 22:28 IST] ingest | In Pursuit Of The Perfect Portfolio Charles D Ellis Fve3Djvygju
- route: RAG+stub
- pages_created: ["the-losers-game-concept", "confidential-client-feedback", "in-depth-company-research", "problem-behind-the-problem", "winners-game-vs-losers-game", "winning-the-losers-game", "index-fund-investing", "market-efficiency", "yale-model", "time-horizon-in-asset-allocation", "60-40-portfolio", "investor-uniqueness", "holistic-portfolio-view", "total-portfolio", "risk-management", "low-cost-indexing", "charles-d-ellis", "greenwich-associates", "winning-the-losers-game", "simon-ramo", "harvard-business-school", "dl-j", "rockefeller-family-office", "new-york-stock-exchange", "yale-university", "david-swensen", "yale-school-of-management", "capital-group"]
- chunks: 19

## [2026-04-13 22:30 IST] ingest | In Pursuit Of The Perfect Portfolio Harry M Markowitz Wdeoipcftdu
- route: RAG+stub
- pages_created: ["modern-portfolio-theory", "present-value-of-future-dividends", "mean-variance-analysis", "diversification", "covariance", "utility-of-change-in-wealth", "customary-wealth", "factor-model", "capm (updated)", "mean-variance-efficient-portfolios", "linear-constraints", "after-tax-mean-variance-analysis", "the-perfect-portfolio", "risk-return-trade-off", "monte-carlo-simulation", "decision-support-system", "efficient-frontier", "harry-markowitz (updated)", "john-burr-williams", "william-sharpe (updated)", "milton-friedman", "peter-bernstein", "capital-asset-pricing-model", "portfolio-selection-book", "university-of-chicago", "harry-m-markowitz", "regulation-t", "markowitz-1959-work", "401k-plan", "market-portfolio", "markowitz-1952-idea", "robo-advisor", "risk-return-analysis-book"]
- chunks: 13

## [2026-04-13 22:31 IST] ingest | In Pursuit Of The Perfect Portfolio Jeremy Siegel 2Fwe5Bvzu C
- route: RAG+stub
- pages_created: ["siegels-paradox", "mean-reversion", "stocks-for-the-long-run", "internet-bubble", "growth-trap", "value-investing", "irrational-exuberance", "cape-ratio", "price-earnings-ratio", "fundamentally-weighted-indexing", "cap-weighted-index", "passive-indexing", "dollar-cost-averaging", "jeremy-siegel", "milton-friedman (updated)", "paul-samuelson", "robert-merton", "wharton-school", "new-york-stock-exchange (updated)", "nifty-fifty", "benjamin-graham", "vanguard (updated)", "tech-sector-bubble-1999", "bob-shiller", "mit", "john-campbell", "wisdomtree-investments", "etfs", "jonathan-steinberg", "tips", "high-yield-bonds"]
- chunks: 16

## [2026-04-13 22:34 IST] ingest | In Pursuit Of The Perfect Portfolio John C Bogle 3Ujbhremus4
- route: RAG+stub
- pages_created: ["senior-thesis-of-john-c-bogle", "go-go-era", "indexation", "diversification (updated)", "index-fund", "mutual-structure", "cost-matters-hypothesis", "efficient-market-hypothesis", "sources-of-market-returns", "investment-return", "speculative-return", "traditional-index-funds", "exchange-traded-funds", "sources-of-market-return", "reasonable-expectations", "the-perfect-portfolio (updated)", "asset-allocation", "50-50-stock-bond-portfolio", "investor-vs-speculator", "internal-rate-of-return", "catastrophe-hedge", "democratization-of-finance", "john-c-bogle", "wellington-fund", "fortune-magazine", "investment-company-act-of-1940", "r-l-morgan", "dow-jones-industrial-average", "national-association-of-investment-companies", "vanguard (updated)", "paul-samuelson (updated)", "first-index-investment-trust", "vanguard-500-index", "john-maynard-keynes", "newsweek", "gold"]
- chunks: 23

## [2026-04-13 22:35 IST] ingest | In Pursuit Of The Perfect Portfolio Martin L Leibowitz Jpcc8Ho5Zns
- route: RAG+stub
- pages_created: ["reinvestment-rate", "internal-rate-of-return (updated)", "asset-liability-management", "liability-returns", "alpha-hunters-and-beta-grazers", "beta", "alpha", "endowment-model", "covariance-matrix", "60-40-portfolio (updated)", "beta-sensitivity", "volatility", "stress-betas", "risk-tolerance", "staying-the-course", "risk-reward-tradeoff", "generalized-funding-ratio", "diversification (updated)", "unrewarded-risk", "portfolio-optimization (updated)", "structural-advantage", "contingency-plan", "liquidity-planning", "marty-leibowitz", "sydney-homer", "inside-the-yield-book", "morgan-stanley", "financial-analysts-journal", "rob-arnott", "harry-markowitz (updated)", "william-sharpe (updated)", "jack-treynor", "martin-l-leibowitz", "private-equity", "real-estate", "financial-analyst-journal", "journal-of-portfolio-management"]
- chunks: 15

## [2026-04-13 22:37 IST] ingest | In Pursuit Of The Perfect Portfolio Myron S Scholes D5Mdcrwxmgy
- route: RAG+stub
- pages_created: ["perfect-portfolio", "compound-return", "time-diversification", "replicating-portfolio", "derivatives", "options", "tail-risk", "hedging", "drawdown", "passive-management", "index-fund-management", "theory-and-empirical-testing", "information-in-prices", "absolute-vs-relative-returns", "tax-management", "convexity-cost", "risk-managed-fund", "relative-value-performance", "benchmark", "myron-scholes", "black-scholes-model", "fischer-black (updated)", "bob-merton", "wells-fargo-bank", "john-mcleod", "derivative-markets", "target-date-fund"]
- chunks: 19

## [2026-04-13 22:38 IST] ingest | In Pursuit Of The Perfect Portfolio Robert C Merton Ipkmu59Ub4C
- route: RAG+stub
- pages_created: ["continuous-time-stochastic-optimization", "lifetime-consumption-portfolio-problem", "intertemporal-optimization", "dynamic-portfolio-theory", "replicating-portfolio (updated)", "derivative-pricing-theory", "no-arbitrage-principle", "equilibrium-model", "meaningful-information", "defined-contribution-plan", "bifurcation-of-choice", "default-option", "dedicated-retirement-assets", "robert-c-merton", "paul-samuelson (updated)", "fischer-black (updated)", "myron-scholes (updated)", "mit (updated)", "black-scholes-model (updated)", "401k", "sec", "social-security (updated)", "financial-planner", "mit-retirement-plan"]
- chunks: 16

## [2026-04-13 22:40 IST] ingest | Mit15 401F08 Ses01 300K.Srt
- route: RAG+stub
- pages_created: ["finance", "time-in-finance", "risk-in-finance", "financial-analysis", "valuation-of-assets", "management-of-assets", "price-discovery-mechanism", "accounting", "stock-and-flow", "balance-sheet", "income-statement", "shareholder-wealth-maximization", "real-assets", "financial-assets", "personal-financial-management", "time-value-of-money", "modern-finance", "no-free-lunch-principle", "non-satiation", "self-interest-in-economics", "valuation", "discounting", "net-present-value (updated)", "corporate-finance", "james-simons", "renaissance-technologies", "warren-buffett", "jack-welch", "general-electric", "professor-wang"]
- chunks: 24

## [2026-04-13 22:43 IST] ingest | Mit15 401F08 Ses02 300K.Srt
- route: RAG+stub
- pages_created: ["government-sponsored-entity", "secondary-market-for-mortgages", "too-big-to-fail", "subprime-mortgages", "market-dislocation", "counter-parties", "full-faith-and-credit", "bankruptcy", "asset", "liability", "patent", "trade-secret", "value-operator", "market-price", "cashflow", "timeline-analysis", "time-based-currency-analogy", "temporal-exchange-rate", "net-present-value (updated)", "time-value-of-money (updated)", "impatience", "opportunity-cost-of-capital", "present-value", "discount-factor", "valuation-operator", "annuity", "perpetuity", "fannie-mae", "freddie-mac", "us-government", "treasury", "coca-cola", "google", "lipitor", "brealey-myers-allen", "the-market", "john-maynard-keynes (updated)"]
- chunks: 28

## [2026-04-13 22:45 IST] ingest | Mit15 401F08 Ses03 300K.Srt
- route: RAG+stub
- pages_created: ["net-present-value (updated)", "moral-hazard", "systemic-risk", "financial-firewall", "asset (updated)", "value-of-an-asset", "discount-factor (updated)", "interest-rate", "opportunity-cost", "perpetuity (updated)", "market-pricing", "price-return", "rate-of-return-for-a-perpetuity", "growing-perpetuity", "annuity (updated)", "annuity-discount-formula", "annuity-discount-factor", "interest-rate-compounding", "compounding", "annual-percentage-rate", "equivalent-annual-rate", "fannie-mae (updated)", "freddie-mac (updated)", "lehman-brothers", "console"]
- chunks: 27

## [2026-04-13 22:50 IST] ingest | Mit15 401F08 Ses04 300K.Srt
- route: RAG+stub
- pages_created: ["leverage", "volatility (updated)", "mark-to-market", "subprime-mortgage", "adjustable-rate-mortgage", "non-recourse-loan", "credit-score", "chapter-11", "inflation", "fear-and-greed", "10-k-and-10-q-filings", "mortgage-insurance", "bankruptcy (updated)", "purchasing-power", "time-value-of-money (updated)", "real-return", "nominal-return", "price-index", "fixed-income-securities", "fixed-income-market-participants", "fixed-income-issuers", "fixed-income-investors", "fixed-income-intermediaries", "coupon-bond", "bond-principal", "bond-coupon", "bond-valuation", "present-value (updated)", "inflation-risk", "pure-discount-bond", "discount-bond-pricing", "implicit-future-forecast-in-bond-prices", "lehman-brothers (updated)", "sec (updated)", "the-fed", "bear-stearns", "fannie-mae (updated)", "freddie-mac (updated)", "barclays", "merrill-lynch", "bank-of-america", "treasury-securities", "federal-agency-securities", "corporate-securities", "mortgage-backed-securities", "asset-backed-securities", "1987-stock-market-crash", "us-treasury-bills", "pure-discount-bond", "discounted-coupon-bond"]
- chunks: 26

## [2026-04-13 22:53 IST] ingest | Mit15 401F08 Ses05 300K.Srt
- route: RAG+stub
- pages_created: ["financial-distress", "costs-of-financial-distress", "credit-crisis", "pure-discount-bond (updated)", "spot-rate-of-interest", "yield-curve", "flight-to-liquidity", "forward-rate", "spot-rate", "future-spot-rate", "open-market-operations", "inflationary-pressures", "yield", "expectations-hypothesis", "liquidity-preference-hypothesis", "preferred-habitat-theory", "coupon-bond-valuation-via-strips", "no-arbitrage-principle (updated)", "short-selling", "the-fed (updated)", "aig", "lehman-brothers (updated)", "barclays (updated)", "bear-stearns (updated)", "jp-morgan", "strips", "the-federal-reserve", "us-treasuries", "federal-funds-rate", "the-treasury", "pure-discount-bond (updated)", "coupon-bond", "forward-contract", "us-treasury-securities", "cox-ingersoll-ross-model", "john-cox", "steve-ross"]
- chunks: 28

## [2026-04-13 22:55 IST] ingest | Mit15 401F08 Ses06 300K.Srt
- route: RAG+stub
- pages_created: ["yield-curve (updated)", "breaking-the-buck", "flight-to-liquidity (updated)", "short-selling (updated)", "default-risk", "inflation (updated)", "law-of-one-price", "arbitrage", "liquidity-crunch", "flight-to-safety", "transaction-costs", "simultaneous-linear-equations-in-finance", "linear-dependence", "duration", "macaulay-duration", "convexity", "treasury-bills", "money-market-fund", "sec (updated)", "the-reserve-fund", "treasurydirect-gov", "nomura", "lehman-brothers (updated)", "goldman-sachs", "us-government (updated)", "bear-stearns (updated)", "salomon-brothers", "macaulay"]
- chunks: 29

## [2026-04-13 22:57 IST] ingest | Mit15 401F08 Ses07 300K.Srt
- route: RAG+stub
- pages_created: ["yield-curve (updated)", "market-sentiment", "shorting", "liquidity", "financial-panic", "breaking-the-buck (updated)", "consolidation", "equity-valuation", "duration (updated)", "convexity (updated)", "credit-ratings", "investment-grade", "non-investment-grade", "credit-spread", "securitization", "disintermediation", "default-risk-pricing", "tranche", "senior-tranche", "junior-tranche", "default-rate", "debt-rating", "correlation", "financial-engineering", "rating-agency", "quantitative-analysis", "bailout", "equity-ownership", "andrew-lo", "us-government (updated)", "financial-rescue-package-2008", "wachovia", "citigroup", "reserve-fund", "fdic", "moodys", "s-and-p", "fitch", "standard-and-poors", "fitch-ratings", "hedge-fund", "pension-fund", "credit-rating-agencies", "us-treasury", "aig (updated)", "warren-buffett (updated)", "goldman-sachs (updated)"]
- chunks: 26

## [2026-04-13 23:00 IST] ingest | Mit15 401F08 Ses08 300K.Srt
- route: RAG+stub
- pages_created: ["equity", "residual-claimant", "limited-liability", "capital-formation", "short-sale", "capital-market-efficiency", "primary-market", "secondary-market", "dividend-discount-model (updated)", "dividends", "growth-companies", "electronic-communications-networks", "risk-adjusted-discount-rate", "risk-return-tradeoff", "market-determined-pricing", "general-stock-valuation-formula", "perpetuity-formula", "gordon-growth-model (updated)", "cost-of-capital", "dividend-yield", "annuity-discount-formula (updated)", "dividend-policy", "external-capital-markets", "andrew-lo (updated)", "pons-and-fleischmann-experiment", "general-electric (updated)", "credit-default-swap"]
- chunks: 28

## [2026-04-13 23:02 IST] ingest | Mit15 401F08 Ses09 300K.Srt
- route: RAG+stub
- pages_created: ["psychological-biases", "mark-to-market-accounting", "forward-contracts", "futures-contracts", "hedging (updated)", "speculating", "derivatives (updated)", "forward-contract", "futures-contract", "forward-price", "spot-price", "long-position", "short-position", "market-expectations", "cost-of-storage", "borrowing-cost", "counterparty-risk", "illiquidity", "physical-delivery", "collateral", "mark-to-market (updated)", "interest-rate-risk", "initial-margin", "maintenance-margin", "caterpillar", "warren-buffett (updated)", "homestake-mining", "battle-mountain-gold", "guay-and-kothari", "futures-clearing-corporation", "nymex"]
- chunks: 29

## [2026-04-13 23:05 IST] ingest | Mit15 401F08 Ses10 300K.Srt
- route: RAG+stub
- pages_created: ["futures-contract (updated)", "zero-npv-transaction", "margin-account", "notional-size", "daily-settlement", "credit-risk", "hedging (updated)", "forward-contract (updated)", "forward-pricing-model", "arbitrage-in-futures-forwards", "storage-costs", "convenience-yield", "financial-future", "cash-settlement", "leverage-in-futures", "margin", "derivative-security", "options (updated)", "warrants", "call-option", "put-option", "strike-price", "options-as-insurance", "option", "european-option", "early-exercise", "implied-volatility", "chicago-mercantile-exchange", "futures-clearing-corporation (updated)", "credit-default-swaps", "s-and-p-500", "s-and-p-500-futures-contract", "october-1987-crash", "new-york-stock-exchange (updated)", "gold (updated)", "gasoline", "sp-500", "etf", "iowa-electronic-markets", "black-scholes-model (updated)", "sp-500-index"]
- chunks: 27

## [2026-04-13 23:07 IST] ingest | Mit15 401F08 Ses11 300K.Srt
- route: RAG+stub
- pages_created: ["option-pricing", "payoff-diagram", "call-option (updated)", "put-option (updated)", "option-premium", "bet-on-volatility", "option-strategy", "butterfly-spread", "implied-volatility (updated)", "option-pricing-theory", "equity-as-a-call-option", "debt-as-a-short-put-position", "capital-structure-arbitrage", "martingale", "brownian-motion", "heat-equation", "option-pricing-formula", "credit-default-swap (updated)", "vix", "chicago-board-options-exchange", "gerolamo-cardano", "cardano", "liber-de-ludo-aleae", "louis-bachelier", "paris-bourse", "albert-einstein", "henri-poincare", "paul-samuelson (updated)", "fischer-black (updated)", "myron-scholes (updated)", "bob-merton (updated)", "the-pricing-of-options-and-corporate-liabilities", "the-jpe", "the-bell-journal"]
- chunks: 21

## [2026-04-13 23:09 IST] ingest | Mit15 401F08 Ses12 300K.Srt
- route: RAG+stub
- pages_created: ["single-period-binomial-model", "arbitrage-argument", "replicating-portfolio (updated)", "probability-independence", "binomial-option-pricing-model", "no-arbitrage-principle (updated)", "risk-neutral-probabilities", "arbitrage (updated)", "random-walk-iid-assumption", "markov-pricing", "parameter-calibration", "volatility (updated)", "derivatives (updated)", "hedging (updated)", "payoff-diagrams", "cost-of-capital (updated)", "expected-rate-of-return", "excess-returns", "risk-premium", "variance-of-returns", "standard-deviation-of-returns", "correlation (updated)", "efficient-markets", "black-scholes-model (updated)", "cox-ross-and-rubenstein", "black-scholes-formula", "black-and-scholes", "mortgage-backed-security", "louis-bachelier (updated)", "s-and-p-500 (updated)"]
- chunks: 23

## [2026-04-13 23:11 IST] ingest | Mit15 401F08 Ses13 300K.Srt
- route: RAG+stub
- pages_created: ["efficient-market", "risk-return-trade-off (updated)", "real-interest-rate", "total-return", "yield-to-maturity", "volatility (updated)", "market-anomalies", "size-effect", "january-effect", "value-premium", "book-to-market-ratio", "momentum-effect", "portfolio", "short-selling (updated)", "130-30-portfolio", "diversification (updated)", "portfolio-theory", "mean-variance-framework", "rational-investor", "shorting-and-longing", "value-weighted-index", "one-year-t-bill", "10-year-treasury-note", "shanghai-stock-exchange", "s&p-500", "general-motors", "motorola", "mutual-fund", "passive-index-fund", "wells-fargo (updated)", "vanguard (updated)", "warren-buffett (updated)", "hedge-funds", "merck", "mcdonalds"]
- chunks: 27

## [2026-04-13 23:14 IST] ingest | Mit15 401F08 Ses14 300K.Srt
- route: RAG+stub
- pages_created: ["risk-return-tradeoff (updated)", "mean-standard-deviation-graph", "expected-return-of-a-portfolio", "portfolio-variance", "covariance (updated)", "correlation (updated)", "diversification (updated)", "short-selling (updated)", "modern-portfolio-theory (updated)", "risk-reward-trade-off", "non-stationarity", "leverage (updated)", "correlation-in-finance", "efficient-frontier (updated)", "portfolio-risk-diversified", "limits-of-diversification", "portfolio-theory (updated)", "hedge-fund", "minimum-variance-boundary", "quantitative-analysis (updated)", "harry-markowitz (updated)", "motorola (updated)", "general-motors (updated)", "kondratiev-cycles", "treasury-bills (updated)", "15-433", "t-bills", "s-and-p (updated)", "warren-buffett (updated)", "james-simons (updated)", "renaissance-technologies (updated)"]
- chunks: 28

## [2026-04-13 23:17 IST] ingest | Mit15 401F08 Ses15 300K.Srt
- route: RAG+stub
- pages_created: ["efficient-frontier (updated)", "risk-reward-trade-off (updated)", "tangency-portfolio", "modern-portfolio-theory (updated)", "portfolio-diversification", "sharpe-ratio", "alpha (updated)", "diversification (updated)", "negative-correlation", "static-portfolio-theory", "mean-variance-optimization", "diminishing-marginal-utility", "covariance (updated)", "tangency-line", "mean-variance-preferences", "market-portfolio (updated)", "equilibrium-argument-supply-demand", "efficient-portfolio", "market-risk-premium", "beta (updated)", "capital-asset-pricing-model (updated)", "cost-of-capital (updated)", "warren-buffett (updated)", "t-bills (updated)", "andrew-lo (updated)", "campbells-soup", "wal-mart", "philip-morris", "freddie-mac (updated)", "mit (updated)", "s-p-500", "russell-2000", "bill-sharpe"]
- chunks: 28

## [2026-04-13 23:19 IST] ingest | Mit15 401F08 Ses16 300K.Srt
- route: RAG+stub
- pages_created: ["risk-reward-trade-off (updated)", "efficient-frontier (updated)", "capital-market-line", "security-market-line", "beta (updated)", "diversification (updated)", "alpha (updated)", "efficient-portfolio (updated)", "net-present-value-calculation", "performance-attribution", "market-risk-premium (updated)", "systematic-risk", "idiosyncratic-risk", "diversified-portfolio", "capm (updated)", "transactions-cost", "regression-equation-for-capm-testing", "law-of-large-numbers", "international-capm", "bill-sharpe (updated)", "tangency-portfolio", "market-portfolio (updated)", "capital-asset-pricing-model (updated)", "s&p-500 (updated)", "gillette", "microsoft"]
- chunks: 27

## [2026-04-13 23:23 IST] ingest | Mit15 401F08 Ses17 300K.Srt
- route: RAG+stub
- pages_created: ["capital-asset-pricing-model (updated)", "capital-budgeting", "alpha (updated)", "idiosyncratic-risk (updated)", "size-anomaly", "market-risk-premium (updated)", "beta (updated)", "volatility-sigma", "multiple-factor-models", "capital-market-line (updated)", "security-market-line (updated)", "equilibrium", "zero-beta-portfolio", "net-present-value (updated)", "value-additivity", "cash-flow", "accounting-earnings", "depreciation", "tax-shield", "straight-line-depreciation", "cash-flows", "bankruptcy-costs", "cost-of-capital (updated)", "comparable-companies-analysis", "pure-play-company", "synergies", "proprietary-trading", "risk-free-rate", "exploration-risk", "market-risk", "risk-adjusted-discount-rate (updated)", "non-systematic-risk", "systematic-risk (updated)", "black-capm", "fisher-black", "biogen", "motorola (updated)", "nasdaq", "fas-157", "bloomberg", "john-wiley-and-sons", "mcgraw-hill", "standard-and-poors (updated)", "saudi-aramco"]
- chunks: 30

## [2026-04-13 23:25 IST] ingest | Mit15 401F08 Ses18 300K.Srt
- route: RAG+stub
- pages_created: ["net-present-value (updated)", "adjusted-present-value", "payback-period", "profitability-index", "career-risk", "liquidity (updated)", "portfolio-theory (updated)", "tangency-portfolio (updated)", "scale-in-investing", "capital-budgeting (updated)", "capital-asset-pricing-model (updated)", "internal-rate-of-return (updated)", "yield-to-maturity (updated)", "hurdle-rate", "complex-numbers", "private-equity", "mezzanine-financing", "perfect-markets-assumption", "efficient-markets-hypothesis", "wisdom-of-crowds", "price-discovery", "political-considerations", "rationality", "brealey-and-myers (updated)", "lehman-brothers (updated)", "bear-stearns (updated)", "challenger-crash", "morton-thiokol", "maloney-and-mulhearn", "challenger-crash-research-paper", "richard-feynman"]
- chunks: 29

## [2026-04-13 23:28 IST] ingest | Mit15 401F08 Ses19 300K.Srt
- route: RAG+stub
- pages_created: ["efficient-markets (updated)", "behavioral-finance", "loss-aversion", "rationality-in-economics", "uncertainty-aversion", "risk-knights-definition", "uncertainty-knights-definition", "ellsberg-paradox", "behavioral-biases", "arbitrage (updated)", "limits-of-arbitrage", "rationality-requires-emotion", "triune-model-of-the-brain", "reptilian-brain", "mammalian-brain", "hominid-brain", "eye-blink-response-rate", "emotional-hyper-stimulation", "rational-finance", "adaptive-markets-hypothesis", "heuristics", "morton-thiokol (updated)", "daniel-kahneman", "amos-tversky", "frank-knight", "ellsberg", "john-maynard-keynes (updated)", "antonio-damasio", "elliot", "descartes-error", "paul-maclean", "andrew-lo (updated)"]
- chunks: 29

## [2026-04-13 23:30 IST] ingest | Mit15 401F08 Ses20 300K.Srt
- route: RAG+stub
- pages_created: ["adaptive-markets-hypothesis (updated)", "efficient-markets-hypothesis (updated)", "limited-arbitrage", "random-walk-hypothesis", "first-order-autocorrelation", "market-efficiency-cycle", "retail-investors", "institutional-investors", "adaptive-markets", "pain-protects-principle", "profits-as-an-anesthetic", "financial-gain-as-neurological-reward", "regulation-as-pre-commitment-device", "traditional-financial-analytics", "present-value (updated)", "perpetuities-and-annuities", "present-value-of-growth-opportunities", "futures-and-forwards", "marking-to-market", "portfolio-construction", "mean-variance-analysis (updated)", "capital-market-line (updated)", "security-market-line (updated)", "risk-adjusted-discount-rate (updated)", "great-depression", "holocaust", "internet-bubble", "glass-steagall-act", "capital-asset-pricing-model (updated)", "seth-alexander", "mit-endowment", "phil-cooper", "goldman-sachs (updated)"]
- chunks: 19

## [2026-04-13 23:32 IST] ingest | Book Blockchain By Chowdhry And Kim   Palgrave Handbook Of Technological Finance (1)
- route: RAG+stub
- pages_created: ["blockchain", "cryptographic-proof", "sha-256", "zero-knowledge-proof", "encryption", "public-key-cryptography", "digital-signature", "decentralized-autonomous-organization", "nakamoto-consensus", "soft-fork", "distributed-ledger-technology", "proof-of-work", "hashing", "double-sha-256", "private-keys", "block-reward", "block-time", "chain-splits", "memory-pool", "transaction-fees", "consensus-protocol", "byzantine-fault-tolerance", "liveness", "safety", "proof-of-stake", "private-permissioned-ledger", "directed-acyclic-graph", "bitcoin", "satoshi-nakamoto", "bitcoin-blockchain", "bitcoin-improvement-proposals", "hyperledger", "linux-foundation"]
- chunks: 15

## [2026-04-13 23:41 IST] ingest | Book Blockchain By Chowdhry And Kim   Palgrave Handbook Of Technological Finance (2)
- route: RAG+stub
- pages_created: ["financial-inclusion", "bottom-of-the-pyramid", "shub-framework", "voice-interface", "bank-balance-batao", "informal-lending-market", "financial-exclusion", "shub-test", "simplicity-filter", "human-touch-filter", "ubiquity-filter", "electronic-payments", "poka-yoke", "voice-recognition-technology", "bottom-of-the-pyramid-bop", "business-correspondent-model", "voice-notification-service", "voice-enabled-atms", "moneylender", "voice-guided-interface", "microlending", "microfinance-institutions", "village-banking", "microangels", "microangel", "strategic-default", "franchising-of-microangels", "digital-didi-model", "digital-literacy", "digital-didi-system", "redressal-mechanism", "digital-and-financial-literacy", "grievance-redressal-mechanism", "centralized-grievance-redressal-system", "digital-didis-and-bcs-network", "insurance-against-mistakes", "interest-rate-capping", "pmjdy-overdraft-facility", "zero-interest-rate-loan", "microfinance-institution-mfi", "mukti-money", "social-insurance", "risk-sharing", "formal-insurance", "informal-insurance", "community-targeted-insurance", "risk-diversification", "formal-informal-insurance-integration", "poverty-premium", "intangible-collateral", "ponzi-scheme", "investment-in-gold", "principal-protected-investment-strategy", "informal-savings", "zero-balance-accounts", "goal-linked-savings", "incentivized-formal-savings", "ayushman-bharat-plus", "package-rate-basis", "public-good", "marginal-cost", "positive-externalities", "marginal-costs-of-electronic-transactions", "cash-payment-method", "digital-financial-services", "bc-agents", "human-touch-in-digital-finance", "zero-transaction-costs", "pradhan-mantri-jan-dhan-yojana", "y-v-reddy", "reserve-bank-of-india", "pradhan-mantri-jan-dhan-yojana-pmjdy", "bop-group", "rupay", "business-correspondents-bcs", "cash", "moneylenders", "amitabh-bachchan", "alexa", "unified-payments-interface-upi", "paytm-sound-box", "national-payments-corporation-of-india-npci", "upi-123pay", "indian-institute-of-science-iisc", "syspin", "respin", "digital-identity-research-initiative-diri", "indian-school-of-business-isb", "national-bureau-of-economic-research-nber", "ujjivan-small-finance-bank", "ujjivan-mobile-banking-application", "muhammad-yunus", "grameen-bank", "sir-fazle-hasan-abed", "brac", "john-hatch", "finca", "bhagwan-chowdhry", "amit-bubna", "review-of-finance", "aadhaar", "bubna-chowdhry-model", "digi-prayas", "internet-saathi", "digital-empowerment-foundation", "axis-bank", "digital-didi", "gram-vaani", "national-institute-of-public-finance-and-policy-nipfp", "sms-unhappy", "shiva-kumar", "state-bank-of-india", "rbi-integrated-ombudsman-scheme", "upi", "compartamos-banco", "sks-microfinance", "bill-and-melinda-gates-foundation", "pmjdy", "code-of-hammurabi", "robert-j-shiller", "sarada-scheme", "ayushman-bharat", "niti-aayog", "pmjdy-account", "diri", "indian-school-of-business", "npci"]
- chunks: 108

## [2026-04-13 23:42 IST] ingest | Paper Cfr
- route: RAG+stub
- pages_created: ["market-risk-hedging", "financial-distress-costs", "multiplicative-uncertainty-effect", "variance-minimizing-hedge-ratio", "optimal-market-hedge-heuristic", "rate-of-return-regression", "optimal-hedge", "minimizing-cash-flow-variance", "minimizing-costs-of-financial-distress", "stock-return-regressions", "paper-cfr", "fischer-black (updated)", "rene-stulz"]
- chunks: 14

## [2026-04-13 23:46 IST] ingest | Paper Cs26 Submission
- route: RAG+stub
- pages_created: ["compression-statistics", "downside-variance-share", "one-sided-reporting-rule", "variance-compression", "reporting-put", "policy-put", "return-smoothing", "lower-partial-moments", "downside-variance-share-cp", "identification-hierarchy", "valid-auxiliary-series", "fixed-target-downside-variance-share", "hac-estimator", "student-t-distribution", "cp-test", "misreporting-intensity-epsilon", "lower-partial-moment-lpm", "distribution-free-scaling", "sortino-ratio", "sharpe-ratio (updated)", "bootstrap-statistical-method", "delta-method", "c-sigma-c-rho-diagnostic-space", "cp-statistic", "co-statistic", "joint-co-cp-test", "one-sided-misreporting", "symmetric-two-sided-smoothing", "bunching-methodology", "sortino-ratio", "sharpe-ratio", "justin-mccrary", "henrik-kleven-and-mazhar-waseem"]
- chunks: 32

## [2026-04-13 23:49 IST] ingest | Paper Intlending
- route: RAG+stub
- pages_created: ["international-lending-enforceability-model", "loan-syndication", "reputation-as-a-discipline-mechanism", "debt-overhang", "partial-default", "eaton-gersovitz-1981-model", "moral-hazard-in-lending", "incentive-compatibility-condition", "reputation-effects-in-lending", "zero-expected-profits-condition", "comparative-statics", "tough-bank-strategy", "weak-bank", "sequential-equilibrium", "capital-to-assets-ratio", "credit-contraction", "debtors-cartel", "bhagwan-chowdhry (updated)", "loan-syndicate", "tough-bank", "kreps-and-wilson-1982a", "milgrom-and-roberts-1982", "bertrand-equilibrium", "cho-kreps-intuitive-criterion", "cross-default-clause", "lindert-and-morton-1987", "chowdhry-1989", "ozler-1988"]
- chunks: 25

## [2026-04-13 23:52 IST] ingest | Paper Investing For Impact
- route: RAG+stub
- pages_created: ["impact-investing", "joint-financing", "impact-investor", "profit-motivated-investor", "pay-for-social-success-contract", "social-impact-guarantee", "multitask-agency-conflict", "pure-nonprofit-status", "social-venture", "impact-investor-underdiversification", "first-order-approach", "agency-cost-of-csr", "incentive-compatibility-constraint", "participation-constraint", "commercial-benchmark", "full-commitment-model", "renegotiation-proof-contract", "nonprofit-status", "for-profit-status", "socially-conscious-capital", "contractible-social-output", "guarantee-against-social-failure-contract", "control-rights", "managers-participation-constraint", "equilibrium-attention-choice", "cash-burning", "optimal-wage-contract", "social-attention", "commercial-firm-benchmark", "renegotiation-tension", "theory-of-the-maximum", "extreme-value-theorem", "social-impact-bond", "social-impact-guarantee", "pay-for-social-success-security"]
- chunks: 40

## [2026-04-13 23:54 IST] ingest | Paper Mmtrading
- route: RAG+stub
- pages_created: ["multimarket-trading", "informed-trading", "liquidity-trading", "market-makers", "small-liquidity-traders", "large-liquidity-traders", "insider-trading", "linear-pricing-rules", "market-depth", "order-flow-correlation", "price-informativeness", "large-liquidity-trader", "informed-trader", "discretionary-liquidity-traders", "trading-concentration", "noise-traders", "information-sharing", "market-maker-competition", "insider-trading-monitoring", "insider-surveillance-system", "market-liquidity-parameter-lambda", "zero-expected-profits", "competition-between-exchanges", "distinction-between-informed-insiders-and-non-insiders", "securities-acts-amendments-of-1975", "consolidated-tape", "intermarket-trading-system", "kyle-1985-model", "admati-and-pfleiderer-1988-model", "market-maker", "informed-trader", "liquidity-trader", "nyse", "pacific-stock-exchange"]
- chunks: 24

## [2026-04-13 23:57 IST] ingest | Paper Repurchase
- route: RAG+stub
- pages_created: ["repurchase-premium", "dividends (updated)", "stock-repurchase", "information-asymmetry", "free-cash-flow", "dividend-smoothing", "cost-of-carrying-cash", "pooling-equilibrium", "sequence-of-events-model", "optimal-payout-policy", "value-of-dividends-function", "dynamic-optimization-problem", "optimal-dividend-policy-function", "cost-of-carrying-cash-forward", "separating-equilibrium", "intrafirm-tender-offer", "incentive-compatibility-condition (updated)", "dynamic-programming", "first-order-condition", "strict-concavity", "myers-and-majluf-1984", "lintner-1956", "october-1987-market-crash", "contraction-mapping-theorem", "envelope-theorem"]
- chunks: 26

## [2026-04-14 00:01 IST] ingest | Paper Rigged Economies Mssubmission
- route: RAG+stub
- pages_created: ["regime-shifts-in-executive-compensation", "hidden-information-problem", "hidden-action-problem", "competitive-matching-market", "assortative-matching", "rent-extraction-view", "portable-managerial-talent", "hidden-action", "hidden-information", "optimal-contract", "efficiency-wages", "clawback-provisions", "matching-market", "high-powered-incentives", "supermodularity", "stable-matching", "positively-assortative-matching", "returns-to-managerial-talent", "manager-optimal-stable-matching", "firm-optimal-stable-matching", "minmax-stable-matching", "portability-of-managerial-talent", "regime-shift", "pay-escalation", "managerial-outside-option", "hidden-information-frictions", "pay-volatility-co-movement", "superstar-effect", "high-powered-equity-linked-incentives", "competitive-matching-model", "hidden-action-and-hidden-information", "incentive-constraint", "participation-constraint (updated)", "positive-assortative-matching", "first-order-stochastic-dominance", "blocking-in-matching-theory", "limited-liability-constraints", "crowding-out-of-governance-innovations", "moral-hazard-and-observability", "eclipse-of-the-public-corporation", "leveraged-buyouts", "supermodularity-and-complementarity", "principal-agent-matching-market", "shapiro-and-stiglitz-1984", "private-equity (updated)", "major-regulatory-changes", "acharya-and-volpin-2010", "private-equity-funds", "bengt-holmstrom", "michael-c-jensen", "donald-m-topkis", "alfred-d-chandler"]
- chunks: 43

## [2026-04-14 00:04 IST] ingest | Paper Rnd
- route: RAG+stub
- pages_created: ["capped-royalty-licensing-mandate", "lindahl-royalty", "patent-buyouts", "government-purchase", "tiered-pricing", "prize-mechanism", "shadow-cost-of-public-funds", "first-best", "free-rider-benchmark", "contribution-game", "efficiency-gap", "third-degree-price-discrimination", "collective-purchase", "lindahl-schedule", "constrained-royalty-lindahl-mechanism", "third-party-discrimination", "racing-equilibrium", "compensated-royalty-licensing-mandate-crlm", "access-inversion", "universal-health-coverage", "lindahl-conditions", "lindahl-optimal-prize", "k-tier-crlm", "parallel-trade", "medicines-patent-pool", "covax", "michael-kremer", "danzon-and-towse", "bergstrom-et-al-1986", "pfizer", "moderna"]
- chunks: 30

## [2026-04-14 00:05 IST] ingest | Paper Bhag Submission
- route: RAG+stub
- pages_created: ["mission-statement", "knowledge-spillovers", "goldilocks-theorem", "strategic-complements", "strategic-substitutes", "absorptive-capacity", "big-hairy-audacious-goal", "interdisciplinary-missions", "team-production", "identity-economics", "goal-setting-theory", "transparency-as-a-commitment-technology", "tournament-theory", "cheap-talk", "collins-and-porras", "john-f-kennedy", "griliches-1992", "jacobs-1970", "holmstrom-1982", "benabou-and-tirole-2006", "akerlof-and-kranton-2005", "locke-and-latham-1990", "tata-nano", "paris-agreement", "besley-and-ghatak-2005", "lazear-and-rosen-1981", "crawford-and-sobel-1982"]
- chunks: 13

## [2026-04-14 00:06 IST] ingest | Paper Thresholds
- route: RAG+stub
- pages_created: ["theory-of-thresholds", "fractional-integration", "long-memory", "threshold-crossing-time", "effective-precision", "supermodularity (updated)", "master-equation", "fractionally-integrated-process", "anti-persistence", "refractory-period", "through-the-cycle-smoothing", "local-whittle-estimator", "rescaled-range-statistic"]
- chunks: 16

## [2026-04-14 00:11 IST] ingest | Paper Which Firms Innovate V3
- route: RAG+stub
- pages_created: ["creative-destruction", "organizational-learning", "caricature-effect", "medium-term-trap", "real-options", "exploration-exploitation-framework", "options-theory", "real-options-framework", "learning-channel", "option-channel", "innovation-threshold", "expansion-option-value", "harvest-option", "learning-intensity", "expansion-capacity", "incumbent-trap", "mokyrs-institutional-prerequisites", "typology-of-firm-behaviors", "moonshot", "costly-pivot", "lean-scaler", "rational-harvest", "missed-bet", "rational-non-entry", "harvest-regime", "zombie-firms", "creative-destruction-blocking", "organization-capital", "market-uncertainty", "negative-current-npv-innovations", "separate-pockets", "real-options-incentive-design", "joseph-schumpeter", "aghion-and-howitt", "kenneth-arrow", "joel-mokyr", "james-march", "bernardo-and-chowdhry", "bowman-and-hurry", "kogut", "bernardo-and-chowdhry-2002", "aghion-and-howitt-1992", "mokyr-2017", "amazon-web-services", "google-glass", "kodak", "blockbuster", "bloom-bond-and-van-reenen-2007", "pisano-1994", "henderson-and-clark-1990", "artificial-intelligence", "amazons-aws"]
- chunks: 24

## [2026-04-14 00:12 IST] ingest | Paper Zkp Full Paper
- route: RAG+stub
- pages_created: ["zkp-password-authentication-protocol", "zero-knowledge-proof (updated)", "completeness", "information-theoretic-soundness", "perfect-zero-knowledge", "eavesdropper-resistance", "fanos-inequality", "secure-remote-password-protocol", "per-round-mutual-information", "binary-entropy-function", "fano-lower-bound", "fano-threshold", "maximum-likelihood-attack", "monotonicity-of-fano-protection", "stirlings-approximation", "encrypted-response-channel", "architectural-absence-of-password", "grid-based-zkp-protocol", "bhagwan-chowdhry (updated)", "vasundhara-sharma", "indian-school-of-business (updated)", "robert-fano"]
- chunks: 16

## [2026-04-14 00:19 IST] auto_wiki_builder | Automated wiki page generation complete
- model: claude-opus-4-6
- stubs_written: 42
- persona_written: 0
- index_rebuilt: True
- elapsed_s: 278.0
