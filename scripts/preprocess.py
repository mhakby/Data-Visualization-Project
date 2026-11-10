"""Clean the raw dataset and save the result for the app.

Run from the project root folder:
    python -m scripts.preprocess
"""

import pandas as pd

from dashboard import config
from dashboard.preprocessing import clean_data, missing_value_report


def main():
    if not config.RAW_DATA_FILE.exists():
        print(f"Raw data file not found: {config.RAW_DATA_FILE}")
        print("Download the dataset and put it in the data/raw/ folder first.")
        return

    raw_df = pd.read_csv(config.RAW_DATA_FILE)
    print(f"Raw data: {raw_df.shape[0]:,} rows, {raw_df.shape[1]} columns")
    print("\nMissing values before cleaning:")
    print(missing_value_report(raw_df).head(10))

    clean_df = clean_data(raw_df)
    print(f"\nClean data: {clean_df.shape[0]:,} rows, {clean_df.shape[1]} columns")

    config.PROCESSED_DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    clean_df.to_csv(config.PROCESSED_DATA_FILE, index=False)
    print(f"Saved to {config.PROCESSED_DATA_FILE}")


if __name__ == "__main__":
    main()
