"""MCP client implementation."""

from typing import Any, TypeVar, Callable
import httpx
import logging
import asyncio
import json
from pydantic import BaseModel, Field

from ..tools import ToolClient, Tool
from ..openrouter import OpenRouterClient

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class MCPTool(Tool):
    """MCP tool definition."""
    internal_url: str | None = Field(default=None, description="The internal URL to invoke the tool")
    service: str = Field(description="The service that provides the tool")
    strict: bool = Field(default=True, description="Whether the tool response is strictly validated")
    input_schema: dict[str, Any] = Field(description="The input schema for the tool")
    function: Callable[..., Any] | None = Field(default=None, description="The function that implements the tool")

    def to_openai_function(self) -> dict[str, Any]:
        """Convert the tool to an OpenAI function definition."""
        # Log the original schema
        logger.info(f"Original schema for {self.name}: {json.dumps(self.input_schema, indent=2)}")
        
        # Convert the schema to strict format
        strict_schema = self._convert_to_openai_schema(self.input_schema)
        
        # Log the converted schema
        logger.info(f"Converted schema for {self.name}: {json.dumps(strict_schema, indent=2)}")
        
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": strict_schema
            }
        }

    def _convert_to_openai_schema(self, mcp_schema: dict[str, Any]) -> dict[str, Any]:
        """Convert MCP schema to OpenAI schema format."""
        if not mcp_schema:
            return {"type": "object", "properties": {}, "required": []}

        logger.info(f"Starting schema conversion for {self.name}")
        logger.info(f"Initial schema: {json.dumps(mcp_schema, indent=2)}")

        # If schema has a $ref, resolve it
        if "$ref" in mcp_schema:
            ref = mcp_schema["$ref"].split("/")[-1]
            mcp_schema = mcp_schema.get("$defs", {}).get(ref, {})
            logger.info(f"Resolved $ref to: {json.dumps(mcp_schema, indent=2)}")

        # If schema has an input wrapper, unwrap it
        if "properties" in mcp_schema and "input" in mcp_schema["properties"]:
            input_schema = mcp_schema["properties"]["input"]
            if "$ref" in input_schema:
                ref = input_schema["$ref"].split("/")[-1]
                input_schema = mcp_schema.get("$defs", {}).get(ref, {})
            mcp_schema = input_schema
            logger.info(f"Unwrapped input schema: {json.dumps(mcp_schema, indent=2)}")

        # Create a new schema object to ensure we have all required fields
        strict_schema = {
            "type": "object",
            "properties": {},
            "required": []
        }

        # Copy over properties, ensuring each has type and description
        if "properties" in mcp_schema:
            for prop_name, prop in mcp_schema["properties"].items():
                # Create a new property object with required fields
                new_prop = {
                    "type": prop.get("type", "string"),
                    "description": prop.get("description", f"The {prop_name} parameter")
                }
                
                # Copy over any additional fields that might be useful
                for key, value in prop.items():
                    if key not in new_prop:
                        new_prop[key] = value
                
                strict_schema["properties"][prop_name] = new_prop
                logger.info(f"Added property {prop_name}: {json.dumps(new_prop, indent=2)}")

        # Copy over required fields
        if "required" in mcp_schema:
            strict_schema["required"] = mcp_schema["required"]
            logger.info(f"Added required fields: {strict_schema['required']}")

        # Ensure all required fields are actually in properties
        strict_schema["required"] = [
            req for req in strict_schema["required"]
            if req in strict_schema["properties"]
        ]
        logger.info(f"Final required fields: {strict_schema['required']}")

        logger.info(f"Final strict schema: {json.dumps(strict_schema, indent=2)}")
        return strict_schema


class MCPClient(ToolClient):
    """MCP client that extends ToolClient to support MCP tool servers."""

    def __init__(self, openrouter_client: OpenRouterClient):
        """Initialize the MCP client."""
        super().__init__(openrouter_client)
        self._mcp_servers: dict[str, str] = {}
        self._http_client = httpx.AsyncClient()

    async def __aenter__(self):
        """Enter the async context."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit the async context."""
        await self._http_client.aclose()

    def _create_tool_function(self, tool: MCPTool) -> Callable[..., Any]:
        """Create a function that invokes an MCP tool."""
        async def tool_function(**kwargs: Any) -> Any:
            # If kwargs has input wrapper, unwrap it
            if "input" in kwargs:
                kwargs = kwargs["input"]

            # Get the URL to use for the tool
            url = tool.internal_url
            if url is None:
                # Use the MCP server URL as fallback
                server_url = self._mcp_servers.get(tool.service)
                if server_url is None:
                    raise ValueError(f"No MCP server found for service {tool.service}")
                url = f"{server_url}/tools/{tool.name}/invoke"

            # Make the HTTP request to the tool's URL
            response = await self._http_client.post(
                url,
                json={"input": kwargs} if tool.strict else kwargs,
                timeout=300.0  # 5 minutes timeout
            )
            
            # Log response details for debugging
            logger.info(f"Tool {tool.name} response status: {response.status_code}")
            logger.info(f"Tool {tool.name} response headers: {response.headers}")
            
            try:
                result = response.json()
                logger.info(f"Tool {tool.name} response parsed successfully")
                return result
            except Exception as e:
                logger.error(f"Failed to parse tool {tool.name} response: {str(e)}")
                logger.error(f"Response content: {response.text[:1000]}...")  # Log first 1000 chars
                raise
        
        return tool_function

    async def register_mcp_server(self, name: str, base_url: str) -> None:
        """Register an MCP server and load its tools."""
        self._mcp_servers[name] = base_url.rstrip("/")
        
        # Fetch tools from the server
        response = await self._http_client.get(f"{base_url}/tools")
        response_data = response.json()
        
        # Extract tools array from response
        tools_data = response_data.get("tools", [])
        logger.info(f"Received {len(tools_data)} tools from server {name}")
        
        # Register each tool
        for idx, tool_data in enumerate(tools_data):
            logger.info(f"Processing tool {idx}: {json.dumps(tool_data, indent=2)}")
            
            # Ensure tool_data is a dictionary
            if not isinstance(tool_data, dict):
                logger.error(f"Invalid tool data type: {type(tool_data)}. Expected dict, got {tool_data}")
                continue
                
            try:
                # Create MCPTool instance with proper dictionary unpacking
                tool = MCPTool(**tool_data)
                
                # Create the tool function
                tool_function = self._create_tool_function(tool)
                
                # Set the function after creation
                tool.function = tool_function
                
                # Register the tool with ToolClient
                self._tools[tool.name] = tool
                logger.info(f"Successfully registered tool: {tool.name}")
            except Exception as e:
                logger.error(f"Failed to register tool: {str(e)}")
                logger.error(f"Tool data that caused the error: {json.dumps(tool_data, indent=2)}") 