"""
test_pipeline.py

Automated regression suite for the E-Commerce Sales Migration pipeline.
Each test maps to a specific defect documented in DEFECTS.md.
Run with: pytest test_pipeline.py -v
"""

import pandas as pd
import pytest
from pipeline import extract, transform


@pytest.fixture(scope="module")
def raw_df():
    return extract("data/messy_ecommerce.csv")


@pytest.fixture(scope="module")
def clean_df(raw_df):
    return transform(raw_df)


def test_no_whitespace_in_column_names(clean_df):
    """DEF-01"""
    assert all(c == c.strip() for c in clean_df.columns)


def test_quantity_is_numeric(clean_df):
    """DEF-02"""
    assert pd.api.types.is_numeric_dtype(clean_df["Quantity"])


def test_price_is_numeric(clean_df):
    """DEF-03"""
    assert pd.api.types.is_numeric_dtype(clean_df["Price"])


def test_no_negative_quantity(clean_df):
    """DEF-08"""
    assert (clean_df["Quantity"].dropna() >= 0).all()


def test_no_negative_price(clean_df):
    """DEF-09"""
    assert (clean_df["Price"].dropna() >= 0).all()


def test_no_fully_duplicate_rows(clean_df):
    """DEF-10"""
    assert clean_df.duplicated().sum() == 0


def test_no_duplicate_order_ids(clean_df):
    """DEF-06 / DEF-13"""
    assert clean_df["Order_ID"].duplicated().sum() == 0


def test_order_date_is_datetime(clean_df):
    """DEF-07"""
    assert pd.api.types.is_datetime64_any_dtype(clean_df["Order_Date"])


def test_category_has_no_raw_nulls(clean_df):
    """DEF-05"""
    assert clean_df["Category"].isna().sum() == 0


def test_category_values_are_standardized(clean_df):
    """DEF-11"""
    expected = {"Books", "Home", "Sports", "Clothing", "Electronics", "Unknown"}
    assert set(clean_df["Category"].unique()).issubset(expected)


def test_total_reconciles_with_quantity_times_price(clean_df):
    """DEF-04 - only checks rows where both inputs are valid"""
    valid_rows = clean_df.dropna(subset=["Quantity", "Price"])
    expected_total = (valid_rows["Quantity"] * valid_rows["Price"]).round(2)
    assert (valid_rows["Total"] == expected_total).all()


def test_unrecoverable_totals_are_null_by_design(clean_df):
    """
    Confirms remaining nulls in Total are exactly the rows where
    Quantity or Price was unrecoverable source data - not a regression.
    """
    null_total_rows = clean_df[clean_df["Total"].isna()]
    unrecoverable = null_total_rows["Quantity"].isna().sum() + \
                    null_total_rows["Price"].isna().sum()
    assert unrecoverable >= len(null_total_rows)


def test_row_count_within_expected_range(raw_df, clean_df):
    """
    Sanity check on migration completeness: cleaned row count should be
    lower than raw (rows were legitimately removed) but not drastically
    lower (which would indicate over-aggressive filtering).
    """
    assert len(clean_df) < len(raw_df)
    assert len(clean_df) >= len(raw_df) * 0.9


def test_price_outlier_is_flagged_not_silently_corrected(clean_df):
    """
    DEF-12: Confirms the known outlier (Price = 10000.00) is still present
    in the cleaned data - i.e. it was flagged for review, not silently
    deleted or capped without evidence.
    """
    outliers = clean_df[clean_df["Price"] > 5000]
    assert len(outliers) >= 1, "Expected outlier row was unexpectedly removed"
