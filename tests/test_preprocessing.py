"""Unit tests for the cleaning helpers in dashboard/preprocessing.py."""

import pandas as pd

from dashboard.preprocessing import clean_data, find_outliers_iqr, missing_value_report


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


def test_clean_data_strips_column_names_and_drops_duplicates():
    df = pd.DataFrame({" Sales ": [5, 5, 7], "Region": ["A", "A", "B"]})
    cleaned = clean_data(df)
    assert list(cleaned.columns) == ["Sales", "Region"]
    assert len(cleaned) == 2
