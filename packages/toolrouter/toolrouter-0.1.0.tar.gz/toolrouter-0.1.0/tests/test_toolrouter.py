import unittest
from unittest.mock import patch, MagicMock

from toolrouter import ToolRouter, setup_default_router, list_tools, call_tool


class TestToolRouter(unittest.TestCase):
    def test_init(self):
        router = ToolRouter(client_id="test-id", api_key="test-key")
        self.assertEqual(router.client_id, "test-id")
        self.assertEqual(router.api_key, "test-key")
        self.assertEqual(router.base_url, "https://api.toolrouter.ai/s")

        router = ToolRouter(client_id="test-id", api_key="test-key", base_url="https://custom.api")
        self.assertEqual(router.base_url, "https://custom.api")

    @patch("toolrouter.client.requests.get")
    def test_list_tools(self, mock_get):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"tools": [{"name": "test_tool"}]}
        mock_get.return_value = mock_response

        # Test method
        router = ToolRouter(client_id="test-id", api_key="test-key")
        tools = router.list_tools()

        # Verify results
        self.assertEqual(tools, [{"name": "test_tool"}])
        mock_get.assert_called_once_with(
            "https://api.toolrouter.ai/s/test-id/list_tools?schema=openai", 
            headers={"Authorization": "Bearer test-key"}
        )

    @patch("toolrouter.client.requests.post")
    def test_call_tool(self, mock_post):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"result": {"output": "success"}}
        mock_post.return_value = mock_response

        # Test method
        router = ToolRouter(client_id="test-id", api_key="test-key")
        result = router.call_tool("test_tool", {"param": "value"})

        # Verify results
        self.assertEqual(result, {"output": "success"})
        mock_post.assert_called_once_with(
            "https://api.toolrouter.ai/s/test-id/call_tool",
            headers={
                "Authorization": "Bearer test-key",
                "Content-Type": "application/json"
            },
            json={
                "tool_name": "test_tool",
                "tool_input": {"param": "value"}
            }
        )

    @patch("toolrouter.client.ToolRouter")
    def test_standalone_functions(self, mock_toolrouter_class):
        # Setup mock instance
        mock_router = MagicMock()
        mock_toolrouter_class.return_value = mock_router
        mock_router.list_tools.return_value = [{"name": "standalone_test"}]
        mock_router.call_tool.return_value = {"output": "standalone_success"}

        # Setup and test
        router = setup_default_router(client_id="test-id", api_key="test-key")
        tools = list_tools()
        result = call_tool("test_tool", {"param": "value"})

        # Verify
        mock_toolrouter_class.assert_called_once_with("test-id", "test-key", "https://api.toolrouter.ai/s")
        mock_router.list_tools.assert_called_once_with("openai")
        mock_router.call_tool.assert_called_once_with("test_tool", {"param": "value"})
        self.assertEqual(tools, [{"name": "standalone_test"}])
        self.assertEqual(result, {"output": "standalone_success"})


if __name__ == "__main__":
    unittest.main() 