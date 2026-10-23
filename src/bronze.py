import os

from databricks.connect import DatabricksSession
from dotenv import load_dotenv

if __name__ == "__main__":
    # 1. Force load the environment variables from your local .env file
    load_dotenv()
    GDRIVE_FILE_ID = os.getenv("GDRIVE_FILE_ID")
    if not GDRIVE_FILE_ID:
        raise RuntimeError("`GDRIVE_FILE_ID` environment variable is not set")

    print("🚀 Connecting to remote Databricks Serverless Compute Engine...")

    try:
        # 2. Establish a connection flagging Serverless context
        spark = DatabricksSession.builder.serverless().getOrCreate()
        print("✅ Serverless connection successfully established!")
    except Exception as e:
        raise RuntimeError(
            f"Failed to establish Databricks Connect Spark Session: {e}"
        ) from e

    # 3. Google Drive / Ingestion Configuration
    # FIX: Databricks expects the explicit /view suffix to correctly locate the domain host bounds
    GDRIVE_URL = f"https://drive.google.com/file/d/{GDRIVE_FILE_ID}/view"
    UC_CONNECTION_NAME = "gdrive"

    print(f"📥 Extracting data from Google Drive ID: {GDRIVE_FILE_ID}")
    print(f"🔗 Target Path: {GDRIVE_URL}")

    # 4. Extract data using Lakeflow Connect configurations
    df = (
        spark.read
        .format("csv")
        .option("databricks.connection", UC_CONNECTION_NAME)
        .option("header", "true")
        .option("inferSchema", "true")
        .load(GDRIVE_URL)
    )

    # 5. Display structure on local terminal for testing purposes
    print("📋 Connection Handshake validated! Sample data preview:")
    df.show(3)

    # # 6. Save to your Lakehouse Architecture Table
    TARGET_DELTA_TABLE = "main.bronze.google_drive_raw"
    print(f"💾 Committing structured data onto Delta Table: {TARGET_DELTA_TABLE}...")

    df.write.format("delta").mode("overwrite").saveAsTable(TARGET_DELTA_TABLE)

    print("✅ Bronze layer ingestion completed successfully!")
