# Test Case Matrix: E-Commerce Data Migration

| TC ID | Title | Type | Precondition | Steps | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|---|---|
| TC-01 | Verify column names have no leading/trailing whitespace | Schema Validation | Raw dataset loaded | 1. Load raw CSV<br>2. Inspect column names | All column names match exactly (no leading/trailing spaces) | Leading space found in `Customer_Name`, `Category` | FAIL |
| TC-02 | Verify all expected columns are present | Schema Validation | Raw dataset loaded | 1. Load raw CSV<br>2. Compare columns to expected schema list | All 11 expected columns present | TBD | TBD |
| TC-03 | Verify Quantity field contains only numeric values | Data Type | Raw dataset loaded | 1. Load raw CSV<br>2. Attempt numeric cast on Quantity column | All values castable to numeric type | 5 nulls present; needs verification of non-numeric entries | TBD |
| TC-04 | Verify Price field contains only numeric values | Data Type | Raw dataset loaded | 1. Load raw CSV<br>2. Attempt numeric cast on Price column | All values castable to numeric type | Non-numeric value `"abd"` found (row index 1); 5 nulls present | FAIL |
| TC-05 | Verify Total = Quantity × Price for all records | Data Accuracy | Quantity and Price are numeric | 1. Compute Quantity × Price<br>2. Compare to Total column | Computed value matches Total for all rows | 14 rows have null Total; mismatch likely tied to Price defect (TC-04) | FAIL |
| TC-06 | Verify no missing values in Category | Completeness | Raw dataset loaded | 1. Load raw CSV<br>2. Count nulls in Category | 0 nulls | 8 nulls found | FAIL |
| TC-07 | Verify Order_ID values are unique | Uniqueness | Raw dataset loaded | 1. Load raw CSV<br>2. Check for duplicate Order_ID values | All Order_IDs unique | TBD | TBD |
| TC-08 | Verify Order_Date values are parseable as valid dates | Data Type | Raw dataset loaded | 1. Load raw CSV<br>2. Attempt datetime parse on Order_Date | All values parse successfully | TBD | TBD |
| TC-09 | Verify Status field uses consistent, expected values | Domain/Value Consistency | Raw dataset loaded | 1. Load raw CSV<br>2. Get unique values in Status | Only expected values present (e.g. Shipped, Delivered, Processing, Cancelled) — consistent casing | TBD | TBD |
| TC-10 | Verify Payment_Method field uses consistent, expected values | Domain/Value Consistency | Raw dataset loaded | 1. Load raw CSV<br>2. Get unique values in Payment_Method | Only expected values present, consistent casing | TBD | TBD |
| TC-11 | Verify Quantity values are positive (no zero/negative) | Boundary/Negative | Quantity is numeric | 1. Cast Quantity to numeric<br>2. Check min value | Minimum value > 0 | TBD | TBD |
| TC-12 | Verify Price values are positive (no zero/negative) | Boundary/Negative | Price is numeric | 1. Cast Price to numeric<br>2. Check min value | Minimum value > 0 | TBD | TBD |
| TC-13 | Verify no fully duplicate rows exist | Uniqueness | Raw dataset loaded | 1. Load raw CSV<br>2. Check for exact duplicate rows | 0 duplicate rows | TBD | TBD |
| TC-14 | Verify record count is preserved post-migration (minus confirmed duplicates) | Completeness | Migration executed | 1. Compare row count pre- and post-migration | Row count matches expected (raw count − duplicates removed) | TBD | TBD |
| TC-15 | Verify Category nulls are handled per defined rule (not silently passed through) | Completeness | Migration executed | 1. Run migration<br>2. Inspect Category column post-migration | No raw NaN values; nulls filled with defined placeholder (e.g. "Unknown") or explicitly flagged | TBD | TBD |
