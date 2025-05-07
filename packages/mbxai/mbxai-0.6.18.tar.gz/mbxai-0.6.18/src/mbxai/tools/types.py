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

        # Create a new schema object to ensure we have all required fields
        strict_schema = {
            "type": "object",
            "properties": {},
            "required": []
        }

        # Copy over properties, ensuring each has type and description
        if "properties" in schema:
            for prop_name, prop in schema["properties"].items():
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

        # Copy over required fields
        if "required" in schema:
            strict_schema["required"] = schema["required"]

        # Ensure all required fields are actually in properties
        strict_schema["required"] = [
            req for req in strict_schema["required"]
            if req in strict_schema["properties"]
        ]

        # Add any additional fields from the original schema
        for key, value in schema.items():
            if key not in strict_schema:
                strict_schema[key] = value

        return strict_schema 