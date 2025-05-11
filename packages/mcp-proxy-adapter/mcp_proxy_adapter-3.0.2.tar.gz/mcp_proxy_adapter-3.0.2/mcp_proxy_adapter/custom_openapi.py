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
    
    EN:
    This generator creates an OpenAPI schema that matches the format expected by MCP-Proxy,
    enabling dynamic command loading and proper tool representation in AI models.
    Allows overriding title, description, and version for schema customization.

    RU:
    Кастомный генератор схемы OpenAPI для совместимости с MCP-Proxy.
    Позволяет создавать схему OpenAPI в формате, ожидаемом MCP-Proxy,
    с возможностью динамической подгрузки команд и корректного отображения инструментов для AI-моделей.
    Поддерживает переопределение title, description и version для кастомизации схемы.
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
        
    def generate(self, title: Optional[str] = None, description: Optional[str] = None, version: Optional[str] = None) -> Dict[str, Any]:
        """
        EN:
        Generate the complete OpenAPI schema compatible with MCP-Proxy.
        Optionally override title, description, and version.

        RU:
        Генерирует полную схему OpenAPI, совместимую с MCP-Proxy.
        Позволяет опционально переопределить title, description и version.
        
        Args:
            title: Custom title for the schema / Кастомный заголовок схемы
            description: Custom description for the schema / Кастомное описание схемы
            version: Custom version for the schema / Кастомная версия схемы
        
        Returns:
            Dict containing the complete OpenAPI schema / Словарь с полной схемой OpenAPI
        """
        # Deep copy the base schema to avoid modifying it
        schema = deepcopy(self.base_schema)

        # Optionally override info fields
        if title:
            schema["info"]["title"] = title
        if description:
            schema["info"]["description"] = description
        if version:
            schema["info"]["version"] = version

        # Add commands to schema
        self._add_commands_to_schema(schema)

        logger.info(f"Generated OpenAPI schema with {len(registry.get_all_commands())} commands")

        return schema


def custom_openapi(app: FastAPI) -> Dict[str, Any]:
    """
    EN:
    Create a custom OpenAPI schema for the FastAPI application.
    Passes app's title, description, and version to the generator.

    RU:
    Создаёт кастомную OpenAPI-схему для FastAPI-приложения.
    Передаёт параметры title, description и version из приложения в генератор схемы.
    
    Args:
        app: The FastAPI application / FastAPI-приложение
        
    Returns:
        Dict containing the custom OpenAPI schema / Словарь с кастомной OpenAPI-схемой
    """
    generator = CustomOpenAPIGenerator()
    openapi_schema = generator.generate(
        title=getattr(app, 'title', None),
        description=getattr(app, 'description', None),
        version=getattr(app, 'version', None)
    )

    # Cache the schema
    app.openapi_schema = openapi_schema

    return openapi_schema 