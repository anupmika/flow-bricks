import os
from databricks.connect import DatabricksSession
from databricks.sdk import WorkspaceClient
from dotenv import load_dotenv


class DatabricksWorkspace:
    @staticmethod
    def get_workspace() -> WorkspaceClient:
        """Loads environment variables and returns a Databricks Workspace Client."""
        load_dotenv()
        try:
            return WorkspaceClient()
        except Exception as e:
            raise RuntimeError(
                f"Failed to initialize Databricks WorkspaceClient: {e}"
            ) from e


if __name__ == "__main__":
    # 1. Force load the environment variables from your local .env file
    load_dotenv()

    print("🚀 Connecting to remote Databricks Serverless Compute Engine...")
    try:
        spark = DatabricksSession.builder.serverless().getOrCreate()
        print("✅ Serverless connection successfully established!")
    except Exception as e:
        raise RuntimeError(
            f"Failed to establish Databricks Connect Spark Session: {e}"
        ) from e

    # 2. Google Drive Folder & Unity Catalog Connections Configuration
    GDRIVE_FOLDER_ID = "1-R7LbjZWdqYeBqfX3GE8-bVfHEvW9cHh"
    GDRIVE_FOLDER_URL = f"https://drive.google.com/drive/folders/{GDRIVE_FOLDER_ID}"
    UC_CONNECTION_NAME = "gdrive"

    # Meta-log directory structures for processing streams
    BASE_CHECKPOINT_DIR = "dbfs:/pipelines/checkpoints/medallion_lakehouse"
    SCHEMA_LOCATION_PATH = f"{BASE_CHECKPOINT_DIR}/gdrive_bronze_schema"
    CHECKPOINT_PATH = f"{BASE_CHECKPOINT_DIR}/gdrive_bronze_checkpoint"

    print(f"📥 Initializing Auto Loader on GDrive folder: {GDRIVE_FOLDER_URL}")

    # 3. Define the Incremental Streaming Reader (Auto Loader)
    df_stream = (
        spark.readStream
        .format("cloudFiles")
        .option("cloudFiles.format", "csv")
        .option("databricks.connection", UC_CONNECTION_NAME)
        .option("header", "true")
        .option("inferSchema", "true")
        # Added to store the schema and support evolution dynamically
        .option("cloudFiles.schemaLocation", SCHEMA_LOCATION_PATH)
        .option("pathGlobFilter", "*.csv")
        .option("recursiveFileLookup", "true")
        .load(GDRIVE_FOLDER_URL)
    )

    # 4. Target destination settings
    TARGET_DELTA_TABLE = "main.bronze.google_drive_raw"
    print(f"💾 Initializing streaming write into Table: {TARGET_DELTA_TABLE}...")

    # 5. Write the stream incrementally into your Delta Lakehouse
    streaming_query = (
        df_stream.writeStream
        .format("delta")
        .option("checkpointLocation", CHECKPOINT_PATH)
        .outputMode("append")
        .toTable(TARGET_DELTA_TABLE)
    )

    print(
        "⚡ Stream is active! Drop any new CSV file into your GDrive folder to watch it ingest live."
    )
    streaming_query.awaitTermination()
