# Enscli File Embedder - Azure Function

This project is an Azure Function application with a predefined structure. It includes a virtual environment, necessary configuration files, and a test suite.

## Prerequisites

- Python 3.11.x
- pip (Python package installer)
- Virtualenv (optional, but recommended)

## Instructions

1. **Clone the repository**:
    ```sh
    git clone <repository_url>
    cd <project_root>
    ```

2. **Install Azure Functions Core Tools**:
    - **Install Node.js**: Download and install Node.js from [nodejs.org](https://nodejs.org/).
    - **Install Azure Functions Core Tools**:
        ```sh
        npm install -g azure-functions-core-tools@4 --unsafe-perm true
        ```

3. **Set up the virtual environment**:
    ```sh
    python -m venv .venv
    ```

4. **Activate the virtual environment**:
    - On Windows:
        ```sh
        .venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```sh
        source .venv/bin/activate
        ```

5. **Install the required packages**:
    ```sh
    pip install -r requirements.txt
    ```

6. **Install new package**:
    ```sh
    pip install <package_name>
    pip freeze > requirements.txt
    ```

7. **Uninstall the new package**:
    ```sh
    pip install <package_name>
    pip freeze > requirements.txt
    ```

## Running the Project

To run the Azure Function locally, use the following command:
```sh
func start --python
```

## Testing

To run the tests:
```sh
pytest
```
