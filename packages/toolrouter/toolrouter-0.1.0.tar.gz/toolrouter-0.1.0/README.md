# ToolRouter Python SDK

A Python client for the [ToolRouter](https://toolrouter.ai) API.

## Installation

```bash
pip install toolrouter
```

## Usage

### Option 1: Using the ToolRouter class

```python
from toolrouter import ToolRouter

# Initialize the client
router = ToolRouter(
    client_id="your-client-id",
    api_key="your-api-key",
    # Optional: base_url="https://api.toolrouter.ai/s"  # Default value shown
)

# List available tools
tools = router.list_tools(schema="openai")  # schema is optional, defaults to "openai"

# Call a tool
result = router.call_tool(
    tool_name="example_tool",
    tool_input={
        "param1": "value1",
        "param2": "value2"
    }
)
```

### Option 2: Using standalone functions

```python
from toolrouter import setup_default_router, list_tools, call_tool

# Setup the default router (do this once at the start of your application)
setup_default_router(
    client_id="your-client-id",
    api_key="your-api-key",
    # Optional: base_url="https://api.toolrouter.ai/s"  # Default value shown
)

# List available tools
tools = list_tools(schema="openai")  # schema is optional, defaults to "openai"

# Call a tool
result = call_tool(
    tool_name="example_tool",
    tool_input={
        "param1": "value1",
        "param2": "value2"
    }
)
```

## Development

### Setting up for development

```bash
# Clone the repository
git clone https://github.com/toolrouter/toolrouter-python.git
cd toolrouter-python

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

### Publishing to PyPI

```bash
# Build the package
python -m pip install --upgrade build
python -m build

# Upload to PyPI
python -m pip install --upgrade twine
python -m twine upload dist/*
```

## License

MIT 