import os
from pathlib import Path

from databricks.connect import DatabricksSession
from databricks.sdk import WorkspaceClient
from dotenv import load_dotenv

load_dotenv(Path(__file__).with_name('.env'))

CATALOG = os.getenv('DATABRICKS_CATALOG', 'main')
BRONZE_SCHEMA = os.getenv('DATABRICKS_BRONZE_SCHEMA', 'bronze')
SILVER_SCHEMA = os.getenv('DATABRICKS_SILVER_SCHEMA', 'silver')
VOLUME_PATH = os.getenv(
    'DATABRICKS_VOLUME_PATH', f"/Volumes/{CATALOG}/{BRONZE_SCHEMA}/cleaned"
)
DRIVE_CONNECTION = os.getenv('DATABRICKS_DRIVE_CONNECTION', 'gdrive')


def get_spark():
    """Establish and return a Databricks Serverless Spark session."""
    return DatabricksSession.builder.serverless().getOrCreate()


def get_workspace() -> WorkspaceClient:
    """Return a Databricks WorkspaceClient."""
    load_dotenv(Path(__file__).with_name('.env'))
    return WorkspaceClient()


def drive_file_url(file_id: str) -> str:
    """Build a Google Drive file URL for the Databricks connector."""
    return f"https://drive.google.com/file/d/{file_id}/view"


def read_drive_file(spark, file_id: str, file_format: str = 'csv'):
    """Read a Google Drive file into a Spark DataFrame via the Databricks connector."""
    url = drive_file_url(file_id)
    reader = (
        spark.read
        .format(file_format)
        .option('databricks.connection', DRIVE_CONNECTION)
        .option('header', 'true')
        .option('inferSchema', 'true')
    )
    return reader.load(url)


def spark_to_pandas(spark_df):
    """Convert a Spark DataFrame to pandas."""
    return spark_df.toPandas()


def pandas_to_spark(spark, pandas_df):
    """Convert a pandas DataFrame to a Spark DataFrame."""
    return spark.createDataFrame(pandas_df)


def write_to_bronze(spark_df, table_name: str, mode: str = 'overwrite') -> str:
    """Write a Spark DataFrame to the bronze layer in Unity Catalog."""
    get_spark()
    full_table = f"{CATALOG}.{BRONZE_SCHEMA}.{table_name}"
    spark_df.write.format('delta').mode(mode).saveAsTable(full_table)
    return full_table


def write_to_silver(spark_df, table_name: str, mode: str = 'overwrite') -> str:
    """Write a Spark DataFrame to the silver (cleaned) layer in Unity Catalog."""
    get_spark()
    full_table = f"{CATALOG}.{SILVER_SCHEMA}.{table_name}"
    spark_df.write.format('delta').mode(mode).saveAsTable(full_table)
    return full_table


def upload_to_volume(
    workspace: WorkspaceClient, file_bytes: bytes, volume_path: str, filename: str
) -> str:
    """Upload raw file bytes to a Databricks Volume and return the full path."""
    volume_path = volume_path.rstrip('/')
    full_path = f"{volume_path}/{filename}"
    workspace.files.upload(full_path, file_bytes, overwrite=True)
    return full_path
