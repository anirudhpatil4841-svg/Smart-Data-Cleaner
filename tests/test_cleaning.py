import pandas as pd
from src.data_cleaner import clean_dataset, analyze_dataset


def test_remove_duplicates():
    data = {
        "Name": ["Rahul", "Priya", "Rahul"],
        "Age": [25, 28, 25]
    }

    df = pd.DataFrame(data)
    cleaned_df = clean_dataset(df)

    assert len(cleaned_df) == 2


def test_fill_missing_values():
    data = {
        "Name": ["Rahul", "Priya"],
        "Age": [25, None]
    }

    df = pd.DataFrame(data)
    cleaned_df = clean_dataset(df)

    assert cleaned_df["Age"].isnull().sum() == 0


def test_analyze_dataset():
    data = {
        "Name": ["Rahul", "Priya", "Rahul"],
        "Age": [25, 28, 25]
    }

    df = pd.DataFrame(data)
    report = analyze_dataset(df)

    assert report["total_rows"] == 3
    assert report["total_columns"] == 2
    assert report["duplicate_rows"] == 1
