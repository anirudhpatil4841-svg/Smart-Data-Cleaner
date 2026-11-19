import pandas as pd


def test_remove_duplicates():
    data = {
        "Name": ["Rahul", "Priya", "Rahul"],
        "Age": [25, 28, 25]
    }

    df = pd.DataFrame(data)
    cleaned_df = df.drop_duplicates()

    assert len(cleaned_df) == 2


def test_missing_values():
    data = {
        "Name": ["Rahul", "Priya"],
        "Age": [25, None]
    }

    df = pd.DataFrame(data)

    assert df.isnull().sum().sum() == 1
