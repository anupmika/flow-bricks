import os
from unittest.mock import MagicMock, patch

from databricks_ops import (
    CATALOG,
    BRONZE_SCHEMA,
    SILVER_SCHEMA,
    VOLUME_PATH,
    DRIVE_CONNECTION,
    drive_file_url,
    get_spark,
    get_workspace,
    read_drive_file,
    spark_to_pandas,
    pandas_to_spark,
    write_to_bronze,
    write_to_silver,
    upload_to_volume,
)


def test_constants_defaults():
    # just ensure defined
    assert isinstance(CATALOG, str)
    assert isinstance(BRONZE_SCHEMA, str)
    assert isinstance(SILVER_SCHEMA, str)
    assert isinstance(VOLUME_PATH, str)
    assert isinstance(DRIVE_CONNECTION, str)


def test_drive_file_url():
    url = drive_file_url('abc123')
    assert url == 'https://drive.google.com/file/d/abc123/view'


def test_get_spark():
    with patch('databricks_ops.DatabricksSession') as m:
        m.builder.serverless.return_value.getOrCreate.return_value = 'spark'
        assert get_spark() == 'spark'


def test_get_workspace():
    with patch('databricks_ops.WorkspaceClient') as m:
        m.return_value = 'ws'
        assert get_workspace() == 'ws'


def test_read_drive_file():
    spark = MagicMock()
    reader = MagicMock()
    spark.read.format.return_value = reader
    reader.option.return_value = reader
    reader.load.return_value = 'df'
    result = read_drive_file(spark, 'fid', 'csv')
    assert result == 'df'
    spark.read.format.assert_called_with('csv')
    reader.load.assert_called_with('https://drive.google.com/file/d/fid/view')


def test_spark_to_pandas():
    spark_df = MagicMock()
    spark_df.toPandas.return_value = 'pdf'
    assert spark_to_pandas(spark_df) == 'pdf'


def test_pandas_to_spark():
    spark = MagicMock()
    spark.createDataFrame.return_value = 'sdf'
    assert pandas_to_spark(spark, 'pdf') == 'sdf'


def test_write_to_bronze():
    spark_df = MagicMock()
    with patch('databricks_ops.get_spark') as gs:
        result = write_to_bronze(spark_df, 't', 'overwrite')
        assert result == f"{CATALOG}.{BRONZE_SCHEMA}.t"
        spark_df.write.format.return_value.mode.return_value.saveAsTable.assert_called()


def test_write_to_silver():
    spark_df = MagicMock()
    with patch('databricks_ops.get_spark') as gs:
        result = write_to_silver(spark_df, 't', 'overwrite')
        assert result == f"{CATALOG}.{SILVER_SCHEMA}.t"


def test_upload_to_volume():
    class Files:
        def __init__(self):
            self.calls = []

        def upload(self, path, data, overwrite=True):
            self.calls.append((path, data, overwrite))

    class WS:
        def __init__(self):
            self.files = Files()

    ws = WS()
    result = upload_to_volume(ws, b'hello', '/Volumes/main/bronze/cleaned/', 'file.csv')
    assert result == '/Volumes/main/bronze/cleaned/file.csv'
    assert ws.files.calls[0] == ('/Volumes/main/bronze/cleaned/file.csv', b'hello', True)


def test_upload_strips_slash():
    class Files:
        def upload(self, path, data, overwrite=True):
            self.path = path

    class WS:
        files = Files()

    ws = WS()
    result = upload_to_volume(ws, b'x', '/vol/path/', 'a.csv')
    assert result == '/vol/path/a.csv'
