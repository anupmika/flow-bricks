from databricks.sdk import WorkspaceClient
from dotenv import load_dotenv


class DatabricksWorkspace:
    @staticmethod
    def get_workspace() -> WorkspaceClient:
        """Loads environment variables and returns a Databricks Workspace Client."""
        try:
            # Load the .env file right before initializing the client
            load_dotenv()
            return WorkspaceClient()

        except Exception as e:
            raise RuntimeError(
                f"Failed to initialize Databricks WorkspaceClient: {e}"
            ) from e
