"""
pipeline.py

ETL pipeline for the E-Commerce Sales Dataset migration.
Each function below resolves one or more defects identified during
data profiling (see DEFECTS.md for full defect log and rationale).
"""

import pandas as pd


def extract(filepath: str) -> pd.DataFrame:
    """Load raw source data."""
    return pd.read_csv(filepath)


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """DEF-01: Strip leading/trailing whitespace from column names."""
    df = df.copy()
    df.columns = df.columns.str.strip()
    return df


def clean_quantity_and_price(df: pd.DataFrame) -> pd.DataFrame:
    """
    DEF-02: Coerce Quantity to numeric (invalid entries -> null).
    DEF-03: Strip currency symbols from Price, then coerce to numeric.
    """
    df = df.copy()
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["Price"] = df["Price"].astype(str).str.replace("$", "", regex=False)
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
    return df


def remove_invalid_negative_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    DEF-08: Remove rows with negative Quantity.
    DEF-09: Remove rows with negative Price.
    Treated as invalid data; no business rule confirms returns/refunds.
    """
    df = df.copy()
    mask = (df["Quantity"].isna() | (df["Quantity"] >= 0)) & \
           (df["Price"].isna() | (df["Price"] >= 0))
    return df[mask]


def remove_exact_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """DEF-10: Remove fully duplicate rows."""
    df = df.copy()
    return df.drop_duplicates()


def resolve_duplicate_order_ids(df: pd.DataFrame) -> pd.DataFrame:
    """
    DEF-06 / DEF-13: Resolve duplicate Order_IDs caused by a discount
    calculation applied inconsistently upstream. Keeps the row where
    Total reconciles with Quantity x Price; discards the mismatched one.
    """
    df = df.copy()
    df["_total_check"] = (df["Quantity"] * df["Price"]).round(2)
    df["_total_matches"] = df["Total"] == df["_total_check"]

    df = (
        df.sort_values("_total_matches", ascending=False)
        .drop_duplicates(subset="Order_ID", keep="first")
    )
    return df.drop(columns=["_total_check", "_total_matches"])


def clean_order_date(df: pd.DataFrame) -> pd.DataFrame:
    """DEF-07: Parse Order_Date to datetime; unparseable values -> NaT."""
    df = df.copy()
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
    return df


def clean_category(df: pd.DataFrame) -> pd.DataFrame:
    """
    DEF-11: Normalize Category casing and singular/plural variants.
    DEF-05: Fill missing Category with explicit 'Unknown' label.

    Note: 'electronic' -> 'electronics' is a manual business-rule
    decision based on evident intent, not an automated inference.
    """
    df = df.copy()
    df["Category"] = df["Category"].str.strip().str.lower()
    df["Category"] = df["Category"].replace({"electronic": "electronics"})
    df["Category"] = df["Category"].str.title()
    df["Category"] = df["Category"].fillna("Unknown")
    return df


def recalculate_total(df: pd.DataFrame) -> pd.DataFrame:
    """
    DEF-04: Recalculate Total as Quantity x Price.
    Rows where Quantity or Price is unrecoverable remain null by design
    (verified by an automated test, not treated as a bug).
    """
    df = df.copy()
    df["Total"] = (df["Quantity"] * df["Price"]).round(2)
    return df


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Run the full transformation pipeline in the correct order."""
    df = clean_column_names(df)
    df = clean_quantity_and_price(df)
    df = remove_invalid_negative_values(df)
    df = remove_exact_duplicates(df)
    df = resolve_duplicate_order_ids(df)
    df = clean_order_date(df)
    df = clean_category(df)
    df = recalculate_total(df)
    return df


def load(df: pd.DataFrame, db_path: str, table_name: str) -> None:
    """Load cleaned data into a SQLite destination table."""
    import sqlite3
    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()


if __name__ == "__main__":
    raw_df = extract("data/messy_ecommerce.csv")
    clean_df = transform(raw_df)
    load(clean_df, "warehouse.db", "sales")

    print(f"Raw rows: {len(raw_df)}")
    print(f"Cleaned rows: {len(clean_df)}")
    print(f"Rows removed: {len(raw_df) - len(clean_df)}")
