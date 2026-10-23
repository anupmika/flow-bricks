import pandas as pd


def remove_nulls(
    df: pd.DataFrame, how: str = "any", threshold: int | None = None
) -> pd.DataFrame:
    """Remove rows with null values.

    how: 'any' drops rows with any null; 'all' drops rows where all values are null.
    threshold: minimum number of non-null values required to keep a row.
    """
    if threshold is not None:
        return df.dropna(thresh=threshold)
    return df.dropna(how=how)


def remove_duplicates(
    df: pd.DataFrame, subset: list | None = None, keep: str = "first"
) -> pd.DataFrame:
    """Remove duplicate rows."""
    return df.drop_duplicates(subset=subset, keep=keep)


def strip_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Strip whitespace and lowercase column names."""
    df = df.copy()
    df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
    return df


def clean_dataframe(
    df: pd.DataFrame,
    remove_null_rows: bool = True,
    remove_dup_rows: bool = True,
    clean_columns: bool = True,
    null_how: str = "any",
) -> pd.DataFrame:
    """Apply a standard cleaning pipeline to a DataFrame."""
    if clean_columns:
        df = strip_column_names(df)
    if remove_null_rows:
        df = remove_nulls(df, how=null_how)
    if remove_dup_rows:
        df = remove_duplicates(df)
    return df.reset_index(drop=True)


def to_csv_bytes(df: pd.DataFrame) -> bytes:
    """Serialize DataFrame to CSV bytes."""
    return df.to_csv(index=False).encode("utf-8")


def to_excel_bytes(df: pd.DataFrame) -> bytes:
    """Serialize DataFrame to Excel bytes."""
    import io

    buffer = io.BytesIO()
    df.to_excel(buffer, index=False, engine="openpyxl")
    buffer.seek(0)
    return buffer.read()
