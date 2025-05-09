# Future AGI MCP Server

The `futureagi-mcp-server` is a server implementation designed to integrate with the Future AGI SDK using the Model Context Protocol (MCP). It provides a standardized and efficient interface for performing advanced LLM operations, including evaluations, dataset management, and content protection.

### Setup and Running

1. **Clone the Repository**:

   ```
   git clone https://github.com/future-agi/futureagi-mcp-server.git
   cd futureagi-mcp-server
   ```
2. **Install Dependencies**

   ```
   brew install uv
   uv sync
   ```
3. **Environment Variables**: Before running the server, ensure the following environment variables are set

   ```
   export FI_API_KEY = "your_api_key"
   export FI_SECRET_KEY = "your_secret_key"
   ```

**Running the Server**: Launch the server using the main entry point:

```bash
python main.py  #for running locally
```

Or, more typically, have your client application launch this command as a subprocess.

## Integration with Clients

The server communicates using the Model Context Protocol (MCP) over standard input/output (`stdio`) channels

To Configure with MCP Clients like VS Code and Claude

```
{
  "mcpServers": {
    "FutureAGI-MCP": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/futureagi-mcp-server",
        "run",
        "main.py"
      ],
      "env": {
        "FI_SECRET_KEY": "your_api_key",
        "FI_API_KEY": "your_secret_key",
        "FI_BASE_URL": "https://api.futureagi.com",
        "PYTHONPATH": "/path/to/futureagi-mcp-server"
      }
    }
  }
}
```

## Available Tools in the Server

The server exposes several functionalities via MCP tools:


 **Evaluations** : List, create, configure, and run evaluations

* **`all_evaluators`** : Retrieve all available evaluators, their functions, and configurations.
* **`get_evals_list_for_create_eval`** : Fetch evaluation templates (preset or user-defined) for creating new evaluations.
* **`get_eval_structure`** : Get detailed structure and required fields for a specific evaluation template.
* **`create_eval`** : Create a new evaluation configuration using a template and custom settings.
* **`evaluate`** : Run evaluations on a list of inputs against specified evaluation templates.

 **Datasets** : Upload datasets and manage dataset configurations

* **`upload_dataset`** : Upload a dataset from a local file to the Future AGI platform and retrieve its configuration.
* **`download_dataset_and_find_insights`** : downloads a dataset and returns the insights

 **Protection Rules** : Apply protection rules like toxicity detection, prompt injection prevention, and privacy safeguarding

* **`protect`** : Evaluate input strings against protection rules and return status, reasons, and rule summaries.
