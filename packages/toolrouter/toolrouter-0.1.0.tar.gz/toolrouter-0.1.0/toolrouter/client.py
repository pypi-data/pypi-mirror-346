import requests

class ToolRouter:
    def __init__(self, client_id, api_key, base_url="https://api.toolrouter.ai/s"):
        self.client_id = client_id
        self.api_key = api_key
        self.base_url = base_url
        
    def list_tools(self, schema="openai"):
        """Get available tools from Toolrouter
        
        Args:
            schema (str): Schema format to return tools in. Default is "openai".
            
        Returns:
            list: Available tools
        """
        url = f"{self.base_url}/{self.client_id}/list_tools?schema={schema}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.get(url, headers=headers)
        return response.json().get("tools", [])
        
    def call_tool(self, tool_name, tool_input):
        """Call a tool using Toolrouter
        
        Args:
            tool_name (str): Name of the tool to call
            tool_input (dict): Input parameters for the tool
            
        Returns:
            dict: Result of the tool execution
        """
        url = f"{self.base_url}/{self.client_id}/call_tool"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "tool_name": tool_name,
            "tool_input": tool_input
        }
        response = requests.post(url, headers=headers, json=data)
        return response.json().get("result", {})

# Standalone functions that use default configuration
_default_router = None

def _get_default_router():
    global _default_router
    if _default_router is None:
        raise ValueError(
            "No default ToolRouter has been configured. "
            "Please initialize by calling either:\n"
            "1. Use the ToolRouter class directly, or\n"
            "2. Import and configure 'setup_default_router' before calling functions"
        )
    return _default_router

def setup_default_router(client_id, api_key, base_url="https://api.toolrouter.ai/s"):
    """Configure the default router with credentials.
    
    Args:
        client_id (str): Your ToolRouter client ID
        api_key (str): Your ToolRouter API key
        base_url (str, optional): Base URL for ToolRouter API. Defaults to "https://api.toolrouter.ai/s".
    """
    global _default_router
    _default_router = ToolRouter(client_id, api_key, base_url)
    return _default_router

def list_tools(schema="openai"):
    """Get available tools from Toolrouter
    
    Args:
        schema (str): Schema format to return tools in. Default is "openai".
        
    Returns:
        list: Available tools
    """
    router = _get_default_router()
    return router.list_tools(schema)

def call_tool(tool_name, tool_input):
    """Call a tool using Toolrouter
    
    Args:
        tool_name (str): Name of the tool to call
        tool_input (dict): Input parameters for the tool
        
    Returns:
        dict: Result of the tool execution
    """
    router = _get_default_router()
    return router.call_tool(tool_name, tool_input) 