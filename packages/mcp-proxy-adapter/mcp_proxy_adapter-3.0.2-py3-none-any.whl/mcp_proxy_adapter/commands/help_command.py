"""
Module with help command implementation.
"""

from typing import Dict, Any, Optional

from mcp_proxy_adapter.commands.base import Command
from mcp_proxy_adapter.commands.result import CommandResult
from mcp_proxy_adapter.commands.command_registry import registry
from mcp_proxy_adapter.core.errors import NotFoundError


class HelpResult(CommandResult):
    """
    Result of the help command execution.
    """
    
    def __init__(self, commands_info: Optional[Dict[str, Any]] = None, command_info: Optional[Dict[str, Any]] = None):
        """
        Initialize help command result.
        
        Args:
            commands_info: Information about all commands (for request without parameters)
            command_info: Information about a specific command (for request with cmdname parameter)
        """
        self.commands_info = commands_info
        self.command_info = command_info
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert result to dictionary.
        
        Returns:
            Dict[str, Any]: Result as dictionary
        """
        if self.command_info:
            return {
                "cmdname": self.command_info["name"],
                "info": {
                    "description": self.command_info["description"],
                    "summary": self.command_info["summary"],
                    "params": self.command_info["params"],
                    "examples": self.command_info["examples"]
                }
            }
        
        # For list of all commands, return as is (already formatted)
        result = self.commands_info.copy()
        
        # Add total count and note about usage
        result["total"] = len(result["commands"])
        result["note"] = "To get detailed information about a specific command, call help with parameter: POST /cmd {\"command\": \"help\", \"params\": {\"cmdname\": \"<command_name>\"}}. Only 'cmdname' parameter is supported."
        
        return result
    
    @classmethod
    def get_schema(cls) -> Dict[str, Any]:
        """
        Get JSON schema for result validation.
        
        Returns:
            Dict[str, Any]: JSON schema
        """
        return {
            "type": "object",
            "oneOf": [
                {
                    "properties": {
                        "commands": {
                            "type": "object",
                            "additionalProperties": {
                                "type": "object",
                                "properties": {
                                    "description": {"type": "string"}
                                }
                            }
                        },
                        "tool_info": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "description": {"type": "string"},
                                "version": {"type": "string"}
                            }
                        },
                        "help_usage": {
                            "type": "object"
                        },
                        "total": {"type": "integer"},
                        "note": {"type": "string"}
                    },
                    "required": ["commands"]
                },
                {
                    "properties": {
                        "cmdname": {"type": "string"},
                        "info": {
                            "type": "object",
                            "properties": {
                                "description": {"type": "string"},
                                "summary": {"type": "string"},
                                "params": {"type": "object"},
                                "examples": {"type": "array"}
                            }
                        }
                    },
                    "required": ["cmdname", "info"]
                }
            ]
        }


class HelpCommand(Command):
    """
    Command for getting help information about available commands.
    """
    
    name = "help"
    result_class = HelpResult
    
    async def execute(self, cmdname: Optional[str] = None) -> HelpResult:
        """
        Execute help command.
        
        Args:
            cmdname: Name of the command to get information about (optional)
            
        Returns:
            HelpResult: Help command result
            
        Raises:
            NotFoundError: If specified command not found
        """
        # If cmdname is provided, return information about specific command
        if cmdname:
            try:
                # Get command metadata from registry
                command_metadata = registry.get_command_metadata(cmdname)
                return HelpResult(command_info=command_metadata)
            except NotFoundError:
                # If command not found, raise error
                raise NotFoundError(f"Command '{cmdname}' not found")
        
        # Otherwise, return information about all available commands
        # and tool metadata
        
        # Get metadata for all commands
        all_metadata = registry.get_all_metadata()
        
        # Prepare response format with tool metadata
        result = {
            "tool_info": {
                "name": "MCP-Proxy API Service",
                "description": "JSON-RPC API for microservice command execution",
                "version": "1.0.0"
            },
            "help_usage": {
                "description": "Get information about commands",
                "examples": [
                    {"command": "help", "description": "List of all available commands"},
                    {"command": "help", "params": {"cmdname": "command_name"}, "description": "Get detailed information about a specific command"}
                ]
            },
            "commands": {}
        }
        
        # Add brief information about commands
        for name, metadata in all_metadata.items():
            result["commands"][name] = {
                "summary": metadata["summary"],
                "params_count": len(metadata["params"])
            }
        
        return HelpResult(commands_info=result)
    
    @classmethod
    def get_schema(cls) -> Dict[str, Any]:
        """
        Get JSON schema for command parameters validation.
        
        Returns:
            Dict[str, Any]: JSON schema
        """
        return {
            "type": "object",
            "properties": {
                "cmdname": {
                    "type": "string",
                    "description": "Name of command to get information about"
                }
            },
            "additionalProperties": False
        } 