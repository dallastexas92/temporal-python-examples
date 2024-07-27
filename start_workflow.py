# start_workflow.py
import os
from dotenv import load_dotenv
import asyncio

from temporalio.client import Client, TLSConfig
from workflow import ETLWorkflow

load_dotenv()

async def main():
    cert_path = os.getenv("TEMPORAL_TLS_CERT_PATH")
    key_path = os.getenv("TEMPORAL_TLS_KEY_PATH")
    cloud_url = os.getenv("TEMPORAL_CLOUD_URL")
    namespace = os.getenv("TEMPORAL_NAMESPACE")

    with open(cert_path, "rb") as f:
        client_cert = f.read()
    with open(key_path, "rb") as f:
        client_private_key = f.read()
    
    client = await Client.connect(
        target_host = cloud_url,
        namespace = namespace,
        tls=TLSConfig(
            client_cert=client_cert,
            client_private_key=client_private_key,
        ),
    )

    result = await client.execute_workflow(
        ETLWorkflow.run,
        id="etl-workflow-id",
        task_queue="etl-task-queue"
    )
    
    print(f"Workflow result: {result}")

if __name__ == "__main__":
    asyncio.run(main())