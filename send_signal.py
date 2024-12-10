#Send in a signal to the workflow as a separate client
import os
from dotenv import load_dotenv
import asyncio
from temporalio.client import Client, TLSConfig

load_dotenv()

async def send_signal():
    #Load Environment Variables
    cert_path = os.getenv("TEMPORAL_TLS_CERT_PATH")
    key_path = os.getenv("TEMPORAL_TLS_KEY_PATH")
    cloud_url = os.getenv("TEMPORAL_CLOUD_URL")
    namespace = os.getenv("TEMPORAL_NAMESPACE")

    #Read certificates and key files
    with open(cert_path, "rb") as f:
        client_cert = f.read()
    with open(key_path, "rb") as f:
        client_private_key = f.read()
    
    #Connect to Temporal Cloud
    client = await Client.connect(
        target_host = cloud_url,
        namespace = namespace,
        tls=TLSConfig(
            client_cert=client_cert,
            client_private_key=client_private_key,
        ),
    )
    
    # Get a handle to the running workflow
    workflow_handle = client.get_workflow_handle("etl-workflow-id")

    #Send a signal to the running workflow
    await workflow_handle.signal("update_data", "I'm a signal!")

if __name__ == "__main__":
    asyncio.run(send_signal())