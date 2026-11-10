"""Data cleaning helpers.

The general helpers (missing values, duplicates, outliers) work with any dataset.
`clean_data` holds the dataset-specific steps and is completed after the dataset decision.
"""

import pandas as pd


def missing_value_report(df):
    """Return a table with the number and percentage of missing values per column."""
    missing_count = df.isna().sum()
    report = pd.DataFrame(
        {
            "missing": missing_count,
            "missing_percent": (missing_count / len(df) * 100).round(2),
        }
    )
    return report.sort_values("missing", ascending=False)


def find_outliers_iqr(series):
    """Return True for values outside 1.5 * IQR (the same rule a box plot uses)."""
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower_limit = q1 - 1.5 * iqr
    upper_limit = q3 + 1.5 * iqr
    return (series < lower_limit) | (series > upper_limit)


def clean_column_names(df):
    """Make column names easier to use: no extra spaces, e.g. ' Sales ' -> 'Sales'."""
    df = df.copy()
    df.columns = df.columns.str.strip()
    return df


def clean_data(df):
    """Run all cleaning steps and return the cleaned DataFrame."""
    df = clean_column_names(df)
    df = df.drop_duplicates()

    # TODO (after dataset decision): add dataset-specific steps here, for example
    # - fill or drop missing values
    # - fix data types (dates, categories)
    # - create new columns (year, month, profit margin, ...)

    return df
