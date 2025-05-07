"""
Type definitions for the tools package.
"""

from typing import Any, Callable
from pydantic import BaseModel, Field

def convert_to_strict_schema(schema: dict[str, Any], strict: bool = True) -> dict[str, Any]:
    """Convert a schema to strict format required by OpenAI.
    
    Args:
        schema: The input schema to validate and convert
        strict: Whether to enforce strict validation with additionalProperties: false
        
    Returns:
        A schema in strict format
    """
    if not schema:
        return {"type": "object", "properties": {}, "required": []}

    # Create a new schema object to ensure we have all required fields
    strict_schema = {
        "type": "object",
        "properties": {},
        "required": []
    }

    # Add additionalProperties: false for strict validation
    if strict:
        strict_schema["additionalProperties"] = False

    # Handle input wrapper
    if "properties" in schema and "input" in schema["properties"]:
        input_schema = schema["properties"]["input"]
        
        # If input has a $ref, resolve it
        if "$ref" in input_schema:
            ref = input_schema["$ref"].split("/")[-1]
            input_schema = schema.get("$defs", {}).get(ref, {})
        
        # Create the input property schema
        input_prop_schema = {
            "type": "object",
            "properties": {},
            "required": []
        }
        
        # Add additionalProperties: false for input schema
        if strict:
            input_prop_schema["additionalProperties"] = False
        
        # Copy over input properties
        if "properties" in input_schema:
            for prop_name, prop in input_schema["properties"].items():
                # Create a new property object with required fields
                new_prop = {
                    "type": prop.get("type", "string"),
                    "description": prop.get("description", f"The {prop_name} parameter")
                }
                
                # Copy over any additional fields that might be useful
                for key, value in prop.items():
                    if key not in new_prop:
                        new_prop[key] = value
                
                input_prop_schema["properties"][prop_name] = new_prop
        
        # Copy over required fields for input schema
        if "required" in input_schema:
            input_prop_schema["required"] = input_schema["required"]
        
        # Add the input property to the main schema
        strict_schema["properties"]["input"] = input_prop_schema
        
        # Copy over required fields for main schema
        if "required" in schema:
            strict_schema["required"] = schema["required"]

    return strict_schema

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
        strict_schema = convert_to_strict_schema(self.schema)
        
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": strict_schema
            }
        } 