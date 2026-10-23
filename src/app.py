import io
import os

import pandas as pd
import streamlit as st

from cleaning import clean_dataframe, to_csv_bytes, to_excel_bytes
from databricks_ops import (
    get_spark,
    get_workspace,
    pandas_to_spark,
    upload_to_volume,
    write_to_bronze,
    write_to_silver,
)


def read_uploaded_file(
    file_bytes: bytes, filename: str, file_format: str
) -> pd.DataFrame:
    """Read uploaded file bytes into a pandas DataFrame."""
    buffer = io.BytesIO(file_bytes)
    if file_format == 'csv':
        return pd.read_csv(buffer)
    if file_format in ('xls', 'xlsx'):
        return pd.read_excel(buffer)
    raise ValueError(f"Unsupported file format: .{file_format}")


st.set_page_config(page_title='Medallion Data Lakehouse', layout='wide')

st.title('Medallion Data Lakehouse')
st.caption(
    'Upload local file  |  Clean  |  Save to Databricks Catalog + Volumes  |  Download'
)

# ---------------------------------------------------------------------------
# Session state defaults
# ---------------------------------------------------------------------------
for key, default in {
    'spark': None,
    'workspace': None,
    'df_raw': None,
    'df_cleaned': None,
    'file_name': 'uploaded_file',
    'file_format': 'csv',
    'cleaned_filename': 'cleaned_file.csv',
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ---------------------------------------------------------------------------
# Sidebar: Databricks config
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header('Databricks')
    catalog = st.text_input('Catalog', value=os.getenv('DATABRICKS_CATALOG', 'main'))
    bronze_schema = st.text_input(
        'Bronze schema', value=os.getenv('DATABRICKS_BRONZE_SCHEMA', 'bronze')
    )
    silver_schema = st.text_input(
        'Silver schema', value=os.getenv('DATABRICKS_SILVER_SCHEMA', 'silver')
    )
    volume_path = st.text_input(
        'Volume path',
        value=os.getenv(
            'DATABRICKS_VOLUME_PATH', f"/Volumes/{catalog}/{bronze_schema}/cleaned"
        ),
        help='Databricks Volume path to store cleaned files.',
    )

    os.environ['DATABRICKS_CATALOG'] = catalog
    os.environ['DATABRICKS_BRONZE_SCHEMA'] = bronze_schema
    os.environ['DATABRICKS_SILVER_SCHEMA'] = silver_schema
    os.environ['DATABRICKS_VOLUME_PATH'] = volume_path

    if st.button('Connect to Databricks', type='primary'):
        with st.spinner('Establishing Databricks Spark session...'):
            try:
                spark = get_spark()
                workspace = get_workspace()
                st.session_state.spark = spark
                st.session_state.workspace = workspace
                st.success('Connected to Databricks')
            except Exception as e:
                st.error(f"Connection failed: {e}")

    st.divider()
    st.header('Upload File')
    uploaded = st.file_uploader(
        'Choose a file (.csv, .xls, .xlsx)',
        type=['csv', 'xls', 'xlsx'],
        accept_multiple_files=False,
    )
    if uploaded is not None:
        file_bytes = uploaded.read()
        st.session_state.file_name = uploaded.name
        ext = uploaded.name.rsplit('.', 1)[-1].lower()
        st.session_state.file_format = ext
        st.session_state.uploaded_bytes = file_bytes
        st.success(f"Selected {uploaded.name}")

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if st.session_state.spark is None:
    st.info('Connect to Databricks from the sidebar to begin.')
    st.stop()

spark = st.session_state.spark
workspace = st.session_state.workspace

st.subheader('1. Load uploaded file')
col_load, col_sep = st.columns([1, 3])
with col_load:
    if st.button(
        'Load file', type='primary', disabled='uploaded_bytes' not in st.session_state
    ):
        with st.spinner('Reading uploaded file...'):
            try:
                df = read_uploaded_file(
                    st.session_state.uploaded_bytes,
                    st.session_state.file_name,
                    st.session_state.file_format,
                )
                st.session_state.df_raw = df
                st.success(f"Loaded {df.shape[0]} rows x {df.shape[1]} columns")
            except Exception as e:
                st.error(f"Failed to read file: {e}")

# ---------------------------------------------------------------------------
# Raw preview
# ---------------------------------------------------------------------------
if st.session_state.df_raw is not None:
    df_raw = st.session_state.df_raw
    st.subheader('2. Raw data preview')
    st.dataframe(df_raw.head(20), width='stretch')
    st.caption(f"Shape: {df_raw.shape[0]} rows x {df_raw.shape[1]} columns")

    # -----------------------------------------------------------------------
    # Cleaning options
    # -----------------------------------------------------------------------
    st.subheader('3. Cleaning options')
    c1, c2, c3 = st.columns(3)
    with c1:
        remove_nulls = st.checkbox('Remove null rows', value=True)
        null_how = st.selectbox('Null removal mode', options=['any', 'all'], index=0)
    with c2:
        remove_dups = st.checkbox('Remove duplicate rows', value=True)
    with c3:
        clean_cols = st.checkbox(
            'Clean column names (strip/lowercase/underscore)', value=True
        )

    if st.button('Run cleaning', type='primary'):
        with st.spinner('Cleaning data...'):
            df_cleaned = clean_dataframe(
                df_raw,
                remove_null_rows=remove_nulls,
                remove_dup_rows=remove_dups,
                clean_columns=clean_cols,
                null_how=null_how,
            )
            st.session_state.df_cleaned = df_cleaned
            st.success(
                f"Cleaned: {df_cleaned.shape[0]} rows x {df_cleaned.shape[1]} columns"
            )

    # -----------------------------------------------------------------------
    # Cleaned preview & outputs
    # -----------------------------------------------------------------------
    if st.session_state.df_cleaned is not None:
        df_cleaned = st.session_state.df_cleaned
        st.subheader('4. Cleaned data preview')
        st.dataframe(df_cleaned.head(20), width='stretch')
        st.caption(f"Shape: {df_cleaned.shape[0]} rows x {df_cleaned.shape[1]} columns")

        base_name = st.session_state.file_name
        st.session_state.cleaned_filename = st.text_input(
            'Cleaned file name',
            value=f"{base_name}_cleaned.{st.session_state.file_format}",
        )

        st.subheader('5. Save & Download')
        col_bronze, col_silver, col_volume, col_dl = st.columns(4)

        with col_bronze:
            if st.button('Save raw to Bronze'):
                with st.spinner('Writing raw to Databricks Bronze...'):
                    try:
                        spark_df = pandas_to_spark(spark, df_raw)
                        table = write_to_bronze(spark_df, f"raw_{base_name}")
                        st.success(f"Raw saved to {table}")
                    except Exception as e:
                        st.error(f"Bronze write failed: {e}")

        with col_silver:
            if st.button('Save cleaned to Silver'):
                with st.spinner('Writing cleaned to Databricks Silver...'):
                    try:
                        spark_df = pandas_to_spark(spark, df_cleaned)
                        table = write_to_silver(spark_df, f"cleaned_{base_name}")
                        st.success(f"Cleaned saved to {table}")
                    except Exception as e:
                        st.error(f"Silver write failed: {e}")

        with col_volume:
            if st.button('Save cleaned to Volume'):
                with st.spinner('Uploading cleaned file to Databricks Volume...'):
                    try:
                        ext = st.session_state.cleaned_filename.rsplit('.', 1)[
                            -1
                        ].lower()
                        if ext == 'csv':
                            payload = to_csv_bytes(df_cleaned)
                        else:
                            payload = to_excel_bytes(df_cleaned)
                        full_path = upload_to_volume(
                            workspace,
                            payload,
                            volume_path,
                            st.session_state.cleaned_filename,
                        )
                        st.success(f"Saved to Volume: {full_path}")
                    except Exception as e:
                        st.error(f"Volume write failed: {e}")

        with col_dl:
            ext = st.session_state.cleaned_filename.rsplit('.', 1)[-1].lower()
            if ext == 'csv':
                payload = to_csv_bytes(df_cleaned)
                mime = 'text/csv'
            else:
                payload = to_excel_bytes(df_cleaned)
                mime = (
                    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
            st.download_button(
                label='Download cleaned file',
                data=payload,
                file_name=st.session_state.cleaned_filename,
                mime=mime,
                type='primary',
            )
