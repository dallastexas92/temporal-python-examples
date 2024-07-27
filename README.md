# Temporal Python Examples

This repository contains example workflows and activities using the Temporal Python SDK.

## Setup Instructions

### Prerequisites

- [Virtualenv](https://virtualenv.pypa.io/en/latest/installation.html)

### Setting Up the Project

1. **Clone the Repository**

    ```bash
    git clone https://github.com/dallastexas92/temporal-python-examples.git
    cd temporal-python-examples
    ```

2. **Create and Activate a Virtual Environment**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**

    ```bash
    pip install temporalio python-dotenv
    ```

4. **Set Up Environment Variables**

    Create a `.env` file in the root directory of the project and add the following variables:

    ```plaintext
    TEMPORAL_CLOUD_URL=your-temporal-cloud-url
    TEMPORAL_TLS_CERT_PATH=path-to-your-cert
    TEMPORAL_TLS_KEY_PATH=path-to-your-key
    TEMPORAL_NAMESPACE=your-namespace
    ```

    Replace the placeholders with your actual values.

5. **Run the Worker**

    ```bash
    python worker.py
    ```

6. **Run the Workflow**

    In a separate terminal, run the following command:

    ```bash
    python start_workflow.py
    ```

### Project Structure

- `activities.py`: Contains the activity definitions for the workflows.
- `workflow.py`: Contains the workflow definitions.
- `worker.py`: Sets up and runs the Temporal worker.
- `start_workflow.py`: Starts the workflow execution.
- `.env`: Contains environment variables (not included in the repository for security).

### Notes

- Ensure your Temporal Cloud URL, certificates, and keys are correctly set in the `.env` file.
- The `.gitignore` file is configured to ignore sensitive files like the virtual environment and certificates.

### License

This project is licensed under the MIT License.
