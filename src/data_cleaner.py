import pandas as pd
import numpy as np


def analyze_dataset(df):
    """Generate a basic dataset quality report."""

    report = {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "missing_values": int(df.isnull().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "memory_usage_kb": round(
            df.memory_usage(deep=True).sum() / 1024, 2
        )
    }

    return report


def clean_dataset(df):
    """Clean missing values and duplicate records."""

    cleaned_df = df.copy()

    # Remove duplicate records
    cleaned_df = cleaned_df.drop_duplicates()

    # Fill missing numerical values with median
    for column in cleaned_df.select_dtypes(include=np.number).columns:
        cleaned_df[column] = cleaned_df[column].fillna(
            cleaned_df[column].median()
        )

    # Fill missing text values with mode
    for column in cleaned_df.select_dtypes(include="object").columns:
        if cleaned_df[column].isnull().any():
            mode_value = cleaned_df[column].mode()

            if not mode_value.empty:
                cleaned_df[column] = cleaned_df[column].fillna(
                    mode_value[0]
                )

    return cleaned_df
