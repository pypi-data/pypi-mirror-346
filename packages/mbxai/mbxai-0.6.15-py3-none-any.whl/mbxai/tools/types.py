"""
Type definitions for the tools package.
"""

from typing import Any, Callable
from pydantic import BaseModel, Field

class ToolCall(BaseModel):
    """A tool call from the model."""
    id: str
    name: str
    arguments: dict[str, Any]

class Tool(BaseModel):
    """A tool that can be used by the model."""
    name: str
    description: str
    function: Callable[..., Any]
    schema: dict[str, Any]

    def to_openai_function(self) -> dict[str, Any]:
        """Convert the tool to an OpenAI function definition."""
        # Ensure schema is in strict format
        strict_schema = self._ensure_strict_schema(self.schema)
        
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": strict_schema
            }
        }

    def _ensure_strict_schema(self, schema: dict[str, Any]) -> dict[str, Any]:
        """Ensure the schema is in strict format required by OpenAI.
        
        Args:
            schema: The input schema to validate and convert
            
        Returns:
            A schema in strict format
        """
        # If schema has a $ref, resolve it
        if "$ref" in schema:
            ref = schema["$ref"].split("/")[-1]
            schema = schema.get("$defs", {}).get(ref, {})

        # If schema has an input wrapper, unwrap it
        if "properties" in schema and "input" in schema["properties"]:
            input_schema = schema["properties"]["input"]
            if "$ref" in input_schema:
                ref = input_schema["$ref"].split("/")[-1]
                input_schema = schema.get("$defs", {}).get(ref, {})
            schema = input_schema

        # Ensure required fields are present
        if "type" not in schema:
            schema["type"] = "object"
        
        if "properties" not in schema:
            schema["properties"] = {}
            
        if "required" not in schema:
            schema["required"] = []

        # Ensure all properties have type and description
        for prop_name, prop in schema["properties"].items():
            if "type" not in prop:
                prop["type"] = "string"  # Default to string if type not specified
            if "description" not in prop:
                prop["description"] = f"The {prop_name} parameter"

        return schema 