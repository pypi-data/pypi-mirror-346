"""
Custom OpenAPI schema generator for MCP Microservice compatible with MCP-Proxy.
"""
import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Type

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from mcp_proxy_adapter.commands.command_registry import registry
from mcp_proxy_adapter.commands.base import Command
from mcp_proxy_adapter.core.logging import logger


class CustomOpenAPIGenerator:
    """
    Custom OpenAPI schema generator for compatibility with MCP-Proxy.
    
    This generator creates an OpenAPI schema that matches the format expected by MCP-Proxy,
    enabling dynamic command loading and proper tool representation in AI models.
    """
    
    def __init__(self):
        """Initialize the generator."""
        self.base_schema_path = Path(__file__).parent / "schemas" / "openapi_schema.json"
        self.base_schema = self._load_base_schema()
        
    def _load_base_schema(self) -> Dict[str, Any]:
        """
        Load the base OpenAPI schema from file.
        
        Returns:
            Dict containing the base OpenAPI schema.
        """
        with open(self.base_schema_path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def _add_commands_to_schema(self, schema: Dict[str, Any]) -> None:
        """
        Add all registered commands to the OpenAPI schema.
        
        Args:
            schema: The OpenAPI schema to update.
        """
        # Get all commands from the registry
        commands = registry.get_all_commands()
        
        # Add command names to the CommandRequest enum
        schema["components"]["schemas"]["CommandRequest"]["properties"]["command"]["enum"] = [
            cmd for cmd in commands.keys()
        ]
        
        # Add command parameters to oneOf
        params_refs = []
        
        for name, cmd_class in commands.items():
            # Create schema for command parameters
            param_schema_name = f"{name.capitalize()}Params"
            schema["components"]["schemas"][param_schema_name] = self._create_params_schema(cmd_class)
            
            # Add to oneOf
            params_refs.append({"$ref": f"#/components/schemas/{param_schema_name}"})
        
        # Add null option for commands without parameters
        params_refs.append({"type": "null"})
        
        # Set oneOf for params
        schema["components"]["schemas"]["CommandRequest"]["properties"]["params"]["oneOf"] = params_refs
    
    def _create_params_schema(self, cmd_class: Type[Command]) -> Dict[str, Any]:
        """
        Create a schema for command parameters.
        
        Args:
            cmd_class: The command class.
            
        Returns:
            Dict containing the parameter schema.
        """
        # Get command schema
        cmd_schema = cmd_class.get_schema()
        
        # Add title and description
        cmd_schema["title"] = f"Parameters for {cmd_class.name}"
        cmd_schema["description"] = f"Parameters for the {cmd_class.name} command"
        
        return cmd_schema
        
    def generate(self) -> Dict[str, Any]:
        """
        Generate the complete OpenAPI schema compatible with MCP-Proxy.
        
        Returns:
            Dict containing the complete OpenAPI schema.
        """
        # Deep copy the base schema to avoid modifying it
        schema = deepcopy(self.base_schema)
        
        # Add commands to schema
        self._add_commands_to_schema(schema)
        
        logger.info(f"Generated OpenAPI schema with {len(registry.get_all_commands())} commands")
        
        return schema


def custom_openapi(app: FastAPI) -> Dict[str, Any]:
    """
    Create a custom OpenAPI schema for the FastAPI application.
    
    Args:
        app: The FastAPI application.
        
    Returns:
        Dict containing the custom OpenAPI schema.
    """
    generator = CustomOpenAPIGenerator()
    openapi_schema = generator.generate()
    
    # Cache the schema
    app.openapi_schema = openapi_schema
    
    return openapi_schema 