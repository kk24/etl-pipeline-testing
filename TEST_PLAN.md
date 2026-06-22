# Test Plan: E-Commerce Data Migration Validation

## 1. Objective

Validate the migration of raw e-commerce sales data from a source system (CSV export) 
to a target system (cleaned data warehouse table), ensuring data completeness, accuracy, 
and integrity are preserved throughout the migration process.

## 2. Scope

### In Scope
- Schema validation (column structure, naming, data types)
- Data completeness checks (null/missing value detection)
- Data accuracy checks (computed field validation — e.g. Total = Quantity × Price)
- Data type validation (numeric fields containing non-numeric values)
- Uniqueness and referential integrity (duplicate record detection)
- Categorical/domain value consistency (Status, Payment_Method)
- Negative and boundary value testing (zero/negative quantities or prices)

### Out of Scope
- Performance/load testing of the migration process
- Security/access control testing
- UI-level testing (no front-end involved)
- Source system data collection process (assumed as given input)

## 3. Test Environment

| Component | Detail |
|---|---|
| Source data | `messy-e-commerce-sales-dataset` (Kaggle, raw CSV, 103 records) |
| Target system | SQLite database (simulated data warehouse) |
| Migration script | `pipeline.py` (Python/pandas ETL script) |
| Test framework | pytest |
| Test execution | Local / Kaggle Notebook |

## 4. Test Strategy

Testing will be conducted in two layers:

1. **Manual exploratory testing** — profiling the raw dataset to identify defects 
   before any transformation occurs (documented in `DEFECTS.md`)
2. **Automated regression testing** — pytest suite executed against the migrated 
   (post-transform) dataset to verify each identified defect was resolved and no 
   new issues were introduced (`test_pipeline.py`)

Each test case will be traceable: a defect found in manual profiling maps to one or 
more automated test cases that guard against its regression.

## 5. Test Types & Coverage

| Test Type | Description | Target Fields |
|---|---|---|
| Schema Validation | Verify column names, structure, expected types | All columns |
| Completeness | Detect nulls/missing values pre- and post-migration | Quantity, Price, Category, Total |
| Accuracy | Verify computed/derived fields are correct | Total (vs Quantity × Price) |
| Data Type | Verify fields contain expected data type after migration | Quantity, Price, Order_Date |
| Uniqueness | Verify no duplicate primary identifiers | Order_ID |
| Domain/Value Consistency | Verify categorical fields use consistent values | Status, Payment_Method |
| Boundary/Negative | Verify no invalid numeric values (negative/zero where not expected) | Quantity, Price |

## 6. Entry Criteria
- Raw dataset available and accessible
- Migration script (`pipeline.py`) implemented

## 7. Exit Criteria
- All test cases in `TEST_CASES.md` executed
- All identified defects logged in `DEFECTS.md` with severity
- Automated regression suite passes 100% against migrated data
- Test summary report completed

## 8. Deliverables
- `TEST_PLAN.md` (this document)
- `TEST_CASES.md` — test case matrix
- `DEFECTS.md` — defect log from raw data profiling
- `test_pipeline.py` — automated regression suite
- `TEST_SUMMARY.md` — final results report

## 9. Tools Used
- Python, pandas (data profiling & transformation)
- pytest (test automation)
- SQLite (target system simulation)
- Kaggle Notebooks (execution environment)
