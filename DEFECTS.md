# Defect Log: E-Commerce Data Migration

| Defect ID | Title | Severity | Related TC | Description | Resolution |
|---|---|---|---|---|---|
| DEF-01 | Leading whitespace in column names | Low | TC-01 | `Customer_Name` and `Category` columns have a leading space in their header names | Fixed — stripped via `.str.strip()` on column names |
| DEF-02 | Non-numeric values in Quantity field | High | TC-03 | Quantity contains text value `"4a"` plus 5 nulls | Fixed — coerced to numeric; unrecoverable values set to null |
| DEF-03 | Non-numeric and inconsistent formats in Price field | High | TC-04 | Price contains `"abd"` (x2), `"four hundred"`, `"300$"` plus 5 nulls | Partially fixed — `"300$"` recovered by stripping currency symbol; `"abd"`/`"four hundred"` unrecoverable, set to null |
| DEF-04 | Total field does not reconcile with Quantity × Price | High | TC-05 | 14 records have null Total; traced to upstream Price/Quantity defects | Fixed — Total recalculated from cleaned Quantity × Price; 13 rows remain null where source data was unrecoverable (by design, verified via test) |
| DEF-05 | Missing values in Category field | Medium | TC-06 | 8 records have null Category | Fixed — filled with explicit `"Unknown"` label rather than left as silent NaN |
| DEF-06 | Duplicate Order_ID values | High | TC-07 | 3 Order_IDs appear more than once | Fixed — see DEF-13 for resolution logic (root cause identified) |
| DEF-07 | Unparseable Order_Date values | Medium | TC-08 | 2 records have Order_Date values that fail standard date parsing (`"Jan 5 2023"`, `"abc"`) | Fixed — coerced to datetime; unparseable values become explicit NaT |
| DEF-08 | Negative Quantity values | High | TC-11 | 2 records have negative Quantity (-2, -5) | Fixed — rows removed (treated as invalid; no business rule confirms returns) |
| DEF-09 | Negative Price value | High | TC-12 | 1 record has Price = -100 | Fixed — row removed |
| DEF-10 | Fully duplicate row | Medium | TC-13 | 1 row is an exact duplicate of another (Order_ID ORD-32755) | Fixed — removed via `drop_duplicates()` |
| DEF-11 | Inconsistent Category values (casing/naming) | Low | TC-16 | Category field contains casing variants of the same value: `"electronics"`, `"ELECTRONICS"`, `"electronic"`, `"sports"` vs `"Electronics"`, `"Sports"` | Fixed — normalized via lowercase + title-case standardization; `"electronic"` mapped to `"electronics"` as a manual business-rule decision |
| DEF-12 | Extreme outlier value in Price | Medium | TC-17 | Order ORD-72751 has Price = 10000.00 — far outside the normal range (~38–705) seen elsewhere | **Flagged only — not auto-corrected.** No evidence to confirm whether this is a data entry error or a legitimate high-value order; correcting without evidence would be unjustified |
| DEF-13 | Duplicate Order_IDs with mismatched Total (discount inconsistency) | High | TC-18 | 2 Order_ID pairs (ORD-56651, ORD-69018) had identical Quantity/Price but different Total — one row's Total was exactly 70% of Quantity × Price, suggesting a lost/misapplied discount upstream | Fixed — kept the row where Total reconciled with Quantity × Price; discarded the inconsistent duplicate |

## Severity Summary

| Severity | Count |
|---|---|
| High | 7 |
| Medium | 4 |
| Low | 2 |
| **Total** | **13** |

## Resolution Summary

| Status | Count |
|---|---|
| Fixed | 11 |
| Flagged only (not auto-corrected) | 1 (DEF-12) |
| Fixed via root-cause resolution | 1 (DEF-13, also resolves DEF-06) |
