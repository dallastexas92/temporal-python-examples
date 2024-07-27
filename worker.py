# worker.py
import os
from dotenv import load_dotenv
import asyncio
from temporalio.worker import Worker
from temporalio.client import Client, TLSConfig
from workflow import ETLWorkflow
from activities import extract_data, transform_data, load_data

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

    worker = Worker(
        client,
        task_queue="etl-task-queue",
        workflows=[ETLWorkflow],
        activities=[extract_data, transform_data, load_data],
    )

    print("Worker started")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())