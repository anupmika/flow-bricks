import io

import pandas as pd
import pytest

from cleaning import (
    clean_dataframe,
    remove_duplicates,
    remove_nulls,
    strip_column_names,
    to_csv_bytes,
    to_excel_bytes,
)


@pytest.fixture
def sample_df():
    return pd.DataFrame(
        {
            ' Name ': ['Alice', 'Bob', 'Alice', None],
            'Age': [25, 30, 25, 40],
            'City': ['NY', 'LA', 'NY', 'SF'],
        }
    )


def test_remove_nulls_any(sample_df):
    result = remove_nulls(sample_df, how='any')
    assert len(result) == 3
    assert result.isnull().sum().sum() == 0


def test_remove_nulls_all():
    df = pd.DataFrame({'a': [1, None, None], 'b': [2, None, 3]})
    result = remove_nulls(df, how='all')
    assert len(result) == 2


def test_remove_nulls_threshold():
    df = pd.DataFrame({'a': [1, None, None], 'b': [2, None, 3], 'c': [4, 5, 6]})
    result = remove_nulls(df, threshold=2)
    assert len(result) == 2


def test_remove_duplicates_default(sample_df):
    result = remove_duplicates(sample_df)
    assert len(result) == 3


def test_remove_duplicates_subset():
    df = pd.DataFrame({'a': [1, 1, 2], 'b': ['x', 'y', 'z']})
    result = remove_duplicates(df, subset=['a'])
    assert len(result) == 2


def test_remove_duplicates_keep_last():
    df = pd.DataFrame({'a': [1, 1, 2]})
    result = remove_duplicates(df, keep='last')
    assert result.iloc[0]['a'] == 1
    assert result.iloc[1]['a'] == 2


def test_strip_column_names(sample_df):
    result = strip_column_names(sample_df)
    assert list(result.columns) == ['name', 'age', 'city']


def test_strip_column_names_does_not_mutate(sample_df):
    original = list(sample_df.columns)
    strip_column_names(sample_df)
    assert list(sample_df.columns) == original


def test_clean_dataframe_default(sample_df):
    result = clean_dataframe(sample_df)
    assert list(result.columns) == ['name', 'age', 'city']
    assert len(result) == 2  # removes null row + duplicate
    assert result.index.tolist() == [0, 1]


def test_clean_dataframe_no_cleaning(sample_df):
    result = clean_dataframe(
        sample_df, remove_null_rows=False, remove_dup_rows=False, clean_columns=False
    )
    assert list(result.columns) == list(sample_df.columns)
    assert len(result) == 4


def test_clean_dataframe_null_how_all():
    df = pd.DataFrame({'a': [1, None, 3], 'b': [None, None, 4]})
    result = clean_dataframe(df, null_how='all')
    assert len(result) == 2


def test_to_csv_bytes(sample_df):
    cleaned = clean_dataframe(sample_df)
    data = to_csv_bytes(cleaned)
    assert isinstance(data, bytes)
    text = data.decode('utf-8')
    assert 'name,age,city' in text
    # roundtrip
    rt = pd.read_csv(io.BytesIO(data))
    assert rt.shape == cleaned.shape


def test_to_excel_bytes(sample_df):
    cleaned = clean_dataframe(sample_df)
    data = to_excel_bytes(cleaned)
    assert isinstance(data, bytes)
    assert len(data) > 0
    rt = pd.read_excel(io.BytesIO(data))
    assert rt.shape == cleaned.shape
