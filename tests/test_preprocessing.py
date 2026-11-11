"""Unit tests for the cleaning steps in dashboard/preprocessing.py."""

import pandas as pd

from dashboard.preprocessing import (
    add_new_columns,
    clean_column_names,
    convert_dates,
    find_outliers_iqr,
    missing_value_report,
    remove_invalid_rows,
    strip_text_values,
)


def test_find_outliers_iqr_marks_extreme_value():
    values = pd.Series([10, 11, 12, 13, 14, 100])
    outliers = find_outliers_iqr(values)
    assert outliers.tolist() == [False, False, False, False, False, True]


def test_missing_value_report_counts_missing_values():
    df = pd.DataFrame({"a": [1, None, 3, None], "b": [1, 2, 3, 4]})
    report = missing_value_report(df)
    assert report.loc["a", "missing"] == 2
    assert report.loc["a", "missing_percent"] == 50.0
    assert report.loc["b", "missing"] == 0


def test_clean_column_names_and_strip_text_values():
    df = pd.DataFrame({" Market ": [" EU", "US "]})
    cleaned = strip_text_values(clean_column_names(df))
    assert list(cleaned.columns) == ["Market"]
    assert cleaned["Market"].tolist() == ["EU", "US"]


def test_convert_dates_reads_day_month_year():
    df = pd.DataFrame({"Order Date": ["31-07-2012"], "Ship Date": ["02-08-2012"]})
    converted = convert_dates(df)
    assert converted.loc[0, "Order Date"] == pd.Timestamp("2012-07-31")
    assert converted.loc[0, "Ship Date"] == pd.Timestamp("2012-08-02")


def test_remove_invalid_rows():
    df = pd.DataFrame(
        {
            "Order Date": pd.to_datetime(["2012-01-05", "2012-01-05", "2012-01-05"]),
            "Ship Date": pd.to_datetime(["2012-01-07", "2012-01-01", "2012-01-07"]),
            "Sales": [100.0, 100.0, 0.0],
        }
    )
    # Row 2 is shipped before it was ordered, row 3 has no sales.
    assert len(remove_invalid_rows(df)) == 1


def test_add_new_columns():
    df = pd.DataFrame(
        {
            "Order Date": pd.to_datetime(["2013-03-10"]),
            "Ship Date": pd.to_datetime(["2013-03-14"]),
            "Sales": [200.0],
            "Profit": [50.0],
        }
    )
    result = add_new_columns(df)
    assert result.loc[0, "Year"] == 2013
    assert result.loc[0, "Month"] == 3
    assert result.loc[0, "Shipping Days"] == 4
    assert result.loc[0, "Profit Margin"] == 0.25
