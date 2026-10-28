import io

import pandas as pd
import pytest

from app import read_uploaded_file


def test_read_csv():
    df = pd.DataFrame({'a': [1, 2], 'b': ['x', 'y']})
    buf = io.BytesIO()
    df.to_csv(buf, index=False)
    result = read_uploaded_file(buf.getvalue(), 'test.csv', 'csv')
    assert result.shape == (2, 2)
    assert list(result.columns) == ['a', 'b']


def test_read_xlsx():
    df = pd.DataFrame({'a': [1, 2], 'b': ['x', 'y']})
    buf = io.BytesIO()
    df.to_excel(buf, index=False)
    result = read_uploaded_file(buf.getvalue(), 'test.xlsx', 'xlsx')
    assert result.shape == (2, 2)


def test_read_xls():
    df = pd.DataFrame({'a': [1, 2]})
    buf = io.BytesIO()
    df.to_excel(buf, index=False, engine='openpyxl')
    # rename extension handling: function checks xls/xlsx both read_excel
    result = read_uploaded_file(buf.getvalue(), 'test.xls', 'xls')
    assert result.shape == (2, 1)


def test_read_unsupported():
    with pytest.raises(ValueError):
        read_uploaded_file(b'data', 'test.txt', 'txt')
