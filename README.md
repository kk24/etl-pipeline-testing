# ETL Pipeline with Automated Testing

A simulated data migration pipeline built to demonstrate ETL best practices: extracting raw data, transforming it to meet data quality standards, loading it into a destination store, and validating every step with automated tests.

## 🎯 Project Goal

Real-world data migrations fail silently — duplicate records slip through, dates get malformed, types get mismatched. This project simulates that scenario and builds a test suite that catches these issues *before* they reach production.

## 🛠️ Tech Stack

- **Python** — core pipeline logic
- **pandas** — data extraction & transformation
- **SQLite** — simulated destination warehouse
- **pytest** — automated pipeline testing
- **Great Expectations** *(optional/upcoming)* — declarative data validation

## 📂 Project Structure

├── pipeline.py          # Extract, transform, load logic
├── test_pipeline.py      # Automated pytest test suite
├── data/                  # Sample/raw dataset
└── README.md

## 🔄 Pipeline Overview

1. **Extract** — reads raw CSV data (sourced from [Kaggle dataset name/link — TBD])
2. **Transform** — cleans the data:
   - Removes duplicate records
   - Converts and validates date formats
   - Casts numeric fields, coercing invalid entries
   - Normalizes text fields (trimming, casing)
3. **Load** — writes the cleaned dataset into a SQLite warehouse table

## ✅ Testing Strategy

The test suite validates both **pipeline logic** and **data integrity**:

- No duplicate IDs after transformation
- No null primary keys
- Correct data types on numeric/date fields
- Expected columns present in final output
- Row count sanity checks (no unexpected data loss)

Run tests locally:

```bash
pytest test_pipeline.py -v
```

## 📊 Results

> _To be filled in once the pipeline runs on the final dataset:_
> - Raw rows: `TBD`
> - Clean rows after transformation: `TBD`
> - Tests passing: `TBD / TBD`

## 🔗 Related

- Live notebook on Kaggle: [link — TBD]

## 📌 Why This Project

Built to practice and demonstrate ETL testing patterns used in real data engineering workflows — particularly around validating data migrations where silent data corruption is a common and costly failure mode.
