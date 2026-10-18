from os import getenv

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.sql import StatementState
from dotenv import load_dotenv


def create_catalog(client: WorkspaceClient, warehouse_id: str) -> None:
    response = client.statement_execution.execute_statement(
        warehouse_id=warehouse_id,
        statement="CREATE CATALOG IF NOT EXISTS study_agent",
        wait_timeout="50s",
    )

    if response.status is None:
        raise RuntimeError("Statement response has no status")
    if response.status.state == StatementState.SUCCEEDED:
        print("Catalog creation succeeded")
    else:
        raise RuntimeError(f"Catalog creation did not succeed: {response.status}")


def main() -> None:
    load_dotenv()

    warehouse_id = getenv("DATABRICKS_WAREHOUSE_ID")
    if warehouse_id is None:
        raise ValueError("DATABRICKS_WAREHOUSE_ID is not set")

    client = WorkspaceClient()

    create_catalog(client, warehouse_id)


if __name__ == "__main__":
    main()
