# ETL Pipeline Migration Testing — E-Commerce Sales Dataset

A QA-driven validation of a simulated e-commerce data migration: profiling raw, messy 
source data, documenting real defects, applying fixes, and proving the migration with 
an automated pytest regression suite.

**Approach:** test-engineer mindset — find and document defects first, then verify 
fixes with automated tests, rather than just "clean the data and move on."

## 🎯 Project Goal

Real-world data migrations fail silently — duplicate records slip through, numeric 
fields contain garbage text, calculated fields go unreconciled. This project simulates 
that scenario on a real messy dataset and builds a full QA process around it: test plan, 
test cases, defect log, automated regression suite, and a summary report.

## 🛠️ Tech Stack

- **Python** — pipeline logic
- **pandas** — data extraction & transformation
- **SQLite** — simulated destination warehouse
- **pytest** — automated regression testing
- **Kaggle Notebooks** — live, visual execution environment

## 📂 Project Structure

├── pipeline.py          # Extract, transform, load logic
├── test_pipeline.py     # Automated pytest regression suite
├── data/                # Source dataset (messy_ecommerce.csv)
├── TEST_PLAN.md          # Scope, strategy, entry/exit criteria
├── TEST_CASES.md         # Full test case matrix (18 cases)
├── DEFECTS.md            # Defect log (13 defects, severity-rated)
├── TEST_SUMMARY.md        # Final results report
└── README.md

## 🔄 Pipeline Overview

1. **Extract** — reads raw CSV (Messy E-Commerce Sales Dataset, Kaggle)
2. **Transform** — resolves 11 of 13 identified defects:
   - Strips whitespace from column names
   - Coerces Quantity/Price to numeric, recovering currency-formatted values
   - Removes invalid negative Quantity/Price
   - Resolves duplicate Order_IDs by tracing root cause (a discount mismatch)
   - Parses Order_Date to proper datetime
   - Standardizes Category casing/naming inconsistencies
   - Recalculates Total from cleaned Quantity × Price
3. **Load** — writes cleaned data into a SQLite warehouse table

## ✅ Testing Strategy

Testing followed a two-layer approach:
1. **Manual exploratory profiling** of raw data to identify defects (`DEFECTS.md`)
2. **Automated regression suite** (pytest) verifying each fix and guarding against regressions

Run tests locally:

```bash
pytest test_pipeline.py -v
```

## 📊 Results

| Metric | Result |
|---|---|
| Raw rows | 103 |
| Cleaned rows | 97 |
| Defects identified | 13 |
| Defects fixed | 11 |
| Defects flagged (not auto-corrected) | 1 |
| Automated tests passing | 12 / 12 (100%) |

One defect (an extreme Price outlier) was deliberately left unresolved and explicitly 
flagged rather than silently "fixed" — documented in `DEFECTS.md` (DEF-12) as an open 
item requiring stakeholder input, since there was no evidence to justify a correction.

## 🔗 Related

- 📓 Live notebook on Kaggle: [E-Commerce Data Migration — QA Test Suite & Defect Analysis]([your-kaggle-link-here](https://www.kaggle.com/code/kkhandekar/e-commerce-data-migration-qa-test-suite-defect))
- 📋 Full QA documentation: see `TEST_PLAN.md`, `TEST_CASES.md`, `DEFECTS.md`, `TEST_SUMMARY.md` in this repo

## 📌 Why This Project

Built to practice and demonstrate ETL/data-migration testing patterns used in real QA 
workflows — particularly around validating data migrations where silent data corruption 
is a common and costly failure mode. The goal wasn't just to clean data, but to test it 
like a production migration: document defects with evidence, fix what's fixable, flag 
what isn't, and prove it with automation.
