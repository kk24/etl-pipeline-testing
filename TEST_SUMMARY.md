# Test Summary Report: E-Commerce Data Migration Validation

## Overview

This report summarizes the results of testing a simulated e-commerce data migration — 
from raw, messy source data through cleaning/transformation to a validated, migration-ready 
dataset — following the approach defined in `TEST_PLAN.md`.

## Dataset

- **Source:** Messy E-Commerce Sales Dataset (Kaggle)
- **Raw row count:** 103
- **Cleaned row count:** 97
- **Rows removed:** 6
  - 3 rows — invalid negative Quantity/Price (DEF-08, DEF-09)
  - 1 row — exact duplicate (DEF-10)
  - 2 rows — duplicate Order_ID with discount-calculation mismatch, root cause traced (DEF-13)

## Test Execution Summary

| Metric | Result |
|---|---|
| Total test cases defined | 18 |
| Test cases executed | 18 |
| Defects identified | 13 |
| Defects fixed | 11 |
| Defects flagged (not auto-corrected) | 1 |
| Defects fixed via root-cause resolution | 1 |
| Automated regression tests (pytest) | 12 |
| Automated tests passing | 12 / 12 (100%) |

## Defect Severity Breakdown

| Severity | Count | Resolved |
|---|---|---|
| High | 7 | 7 |
| Medium | 4 | 4 |
| Low | 2 | 2 |

## Key Findings

1. **Data type integrity was the most common defect category** — Quantity and Price fields 
   contained non-numeric text values (`"abd"`, `"4a"`, `"four hundred"`) and inconsistent 
   currency formatting (`"300$"`), which would have silently broken downstream calculations 
   if migrated as-is.
2. **A root-cause discovery, not just a symptom fix:** duplicate Order_IDs (DEF-06) were 
   initially assumed to be simple duplication errors. Investigation revealed the actual cause — 
   a discount calculation applied inconsistently (DEF-13), producing two versions of the same 
   order with different Totals. Resolving the root cause also resolved the duplicate-ID symptom.
3. **One defect was deliberately left unresolved** (DEF-12, an extreme Price outlier) due to 
   insufficient evidence to justify automatic correction — documented as an open item for 
   stakeholder review rather than silently "fixed" with an assumption.
4. **13 rows retain a null Total by design**, not as a missed defect — verified explicitly by 
   an automated test confirming these nulls correspond exactly to source rows where Quantity 
   or Price was unrecoverable.

## Test Result: PASS

All defined, fixable defects were resolved and verified via automated regression testing. 
The one unresolved item (DEF-12) is explicitly flagged rather than hidden, satisfying the 
exit criteria defined in the Test Plan (all defects documented with severity; automated 
suite passing).

## Artifacts

- Test Plan: `TEST_PLAN.md`
- Test Case Matrix: `TEST_CASES.md`
- Defect Log: `DEFECTS.md`
- Automated Test Suite: `test_pipeline.py` / Kaggle notebook (pytest, 12 tests)
- Live notebook: [Kaggle link]
