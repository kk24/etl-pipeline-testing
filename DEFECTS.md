# Defect Log: E-Commerce Data Migration

| Defect ID | Title | Severity | Related TC | Description | Impact |
|---|---|---|---|---|---|
| DEF-01 | Leading whitespace in column names | Low | TC-01 | `Customer_Name` and `Category` columns have a leading space in their header names | Causes KeyError if columns are referenced without exact whitespace match; silent failure risk in downstream code |
| DEF-02 | Non-numeric values in Quantity field | High | TC-03 | Quantity field contains text value `"4a"` in addition to 5 null values | Breaks numeric operations (sums, averages) on Quantity; causes calculation failures downstream |
| DEF-03 | Non-numeric and inconsistent formats in Price field | High | TC-04 | Price field contains `"abd"` (x2), `"four hundred"`, and `"300$"` (currency symbol embedded) in addition to 5 nulls | Breaks numeric casting entirely; "300$" requires special parsing, not just type coercion |
| DEF-04 | Total field does not reconcile with Quantity × Price | High | TC-05 | 14 records have null Total; traced to upstream Price/Quantity defects | Indicates Total was either not calculated or calculation failed silently at source; major data integrity risk |
| DEF-05 | Missing values in Category field | Medium | TC-06 | 8 records have null Category | Impacts any downstream reporting/filtering by category; needs explicit handling rule |
| DEF-06 | Duplicate Order_ID values | High | TC-07 | 3 Order_IDs appear more than once | Violates expected uniqueness of order identifier; risk of double-counting revenue/orders |
| DEF-07 | Unparseable Order_Date values | Medium | TC-08 | 2 records have Order_Date values that fail standard date parsing | Breaks any time-based analysis or sorting; needs investigation into actual raw format |
| DEF-08 | Negative Quantity values | High | TC-11 | 2 records have Quantity = -5 (or similar negative values) | Not a valid representation of a sale; no business rule (e.g. return flag) confirms this as intentional — treated as invalid data |
| DEF-09 | Negative Price value | High | TC-12 | 1 record has Price = -100 | No valid business scenario for negative pricing in this dataset; treated as invalid data |
| DEF-10 | Fully duplicate row | Medium | TC-13 | 1 row is an exact duplicate of another (all columns match) | Inflates record count and skews any aggregate calculations |

## Severity Summary

| Severity | Count |
|---|---|
| High | 6 |
| Medium | 3 |
| Low | 1 |
| **Total** | **10** |
