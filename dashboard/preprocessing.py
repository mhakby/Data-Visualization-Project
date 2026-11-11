"""Data cleaning for the Global Superstore dataset.

`clean_data` runs all steps in order. Each step is a small function,
so it is easy to test and to explain in the report.
"""

import pandas as pd

# --- General helpers --------------------------------------------------------


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


# --- Cleaning steps ---------------------------------------------------------


def clean_column_names(df):
    """Remove extra spaces from column names, e.g. ' Sales ' -> 'Sales'."""
    df = df.copy()
    df.columns = df.columns.str.strip()
    return df


def strip_text_values(df):
    """Remove extra spaces at the start and end of text values."""
    df = df.copy()
    for column in df.columns:
        if pd.api.types.is_string_dtype(df[column]):
            df[column] = df[column].str.strip()
    return df


def drop_unused_columns(df):
    """Drop columns we do not use.

    - Row ID: only a row number, it carries no information.
    - Postal Code: about 80% missing, because only US orders have one.
    """
    return df.drop(columns=["Row ID", "Postal Code"])


def convert_dates(df):
    """Convert date text like '31-07-2012' (day-month-year) to datetime."""
    df = df.copy()
    df["Order Date"] = pd.to_datetime(df["Order Date"], format="%d-%m-%Y")
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], format="%d-%m-%Y")
    return df


def remove_invalid_rows(df):
    """Remove rows that cannot be correct: shipped before ordered, or zero/negative sales."""
    shipped_before_ordered = df["Ship Date"] < df["Order Date"]
    no_sales = df["Sales"] <= 0
    return df[~shipped_before_ordered & ~no_sales]


def add_new_columns(df):
    """Add columns that several charts need."""
    df = df.copy()
    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.month
    df["Shipping Days"] = (df["Ship Date"] - df["Order Date"]).dt.days
    df["Profit Margin"] = (df["Profit"] / df["Sales"]).round(4)
    return df


def clean_data(df):
    """Run all cleaning steps and return the cleaned DataFrame."""
    df = clean_column_names(df)
    df = strip_text_values(df)
    df = df.drop_duplicates()
    df = drop_unused_columns(df)
    df = convert_dates(df)
    df = remove_invalid_rows(df)
    df = add_new_columns(df)

    # Outliers are NOT removed: large orders and big losses are real sales, not errors.
    # The sidebar has a checkbox to hide Sales outliers when needed.

    return df.reset_index(drop=True)
