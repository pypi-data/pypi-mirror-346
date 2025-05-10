"""
Module for registering and managing commands.
"""

import importlib
import inspect
import os
import pkgutil
from typing import Any, Dict, List, Optional, Type, TypeVar, cast

from mcp_proxy_adapter.commands.base import Command
from mcp_proxy_adapter.core.errors import NotFoundError
from mcp_proxy_adapter.core.logging import logger

T = TypeVar("T", bound=Command)


class CommandRegistry:
    """
    Registry for registering and finding commands.
    """
    
    def __init__(self):
        """
        Initialize command registry.
        """
        self._commands: Dict[str, Type[Command]] = {}
    
    def register(self, command_class: Type[Command]) -> None:
        """
        Registers command class in the registry.

        Args:
            command_class: Command class to register.

        Raises:
            ValueError: If command with the same name is already registered.
        """
        if not hasattr(command_class, "name") or not command_class.name:
            # Use class name if name attribute is not set
            command_name = command_class.__name__.lower()
            if command_name.endswith("command"):
                command_name = command_name[:-7]  # Remove "command" suffix
        else:
            command_name = command_class.name
            
        if command_name in self._commands:
            logger.debug(f"Command '{command_name}' is already registered, skipping")
            raise ValueError(f"Command '{command_name}' is already registered")
            
        logger.debug(f"Registering command: {command_name}")
        self._commands[command_name] = command_class
    
    def unregister(self, command_name: str) -> None:
        """
        Removes command from registry.

        Args:
            command_name: Command name to remove.

        Raises:
            NotFoundError: If command is not found.
        """
        if command_name not in self._commands:
            raise NotFoundError(f"Command '{command_name}' not found")
            
        logger.debug(f"Unregistering command: {command_name}")
        del self._commands[command_name]
    
    def command_exists(self, command_name: str) -> bool:
        """
        Checks if command exists in registry.

        Args:
            command_name: Command name to check.

        Returns:
            True if command exists, False otherwise.
        """
        return command_name in self._commands
    
    def get_command(self, command_name: str) -> Type[Command]:
        """
        Gets command class by name.

        Args:
            command_name: Command name.

        Returns:
            Command class.

        Raises:
            NotFoundError: If command is not found.
        """
        if command_name not in self._commands:
            raise NotFoundError(f"Command '{command_name}' not found")
            
        return self._commands[command_name]
    
    def get_all_commands(self) -> Dict[str, Type[Command]]:
        """
        Returns all registered commands.

        Returns:
            Dictionary with command names and their classes.
        """
        return dict(self._commands)
    
    def get_command_info(self, command_name: str) -> Dict[str, Any]:
        """
        Gets information about a command.

        Args:
            command_name: Command name.

        Returns:
            Dictionary with command information.

        Raises:
            NotFoundError: If command is not found.
        """
        command_class = self.get_command(command_name)
        
        return {
            "name": command_name,
            "description": command_class.__doc__ or "",
            "params": command_class.get_param_info(),
            "schema": command_class.get_schema(),
            "result_schema": command_class.get_result_schema()
        }
    
    def get_command_metadata(self, command_name: str) -> Dict[str, Any]:
        """
        Get complete metadata for a command.
        
        Args:
            command_name: Command name
            
        Returns:
            Dict with command metadata
            
        Raises:
            NotFoundError: If command is not found
        """
        command_class = self.get_command(command_name)
        return command_class.get_metadata()
    
    def get_all_metadata(self) -> Dict[str, Dict[str, Any]]:
        """
        Get metadata for all registered commands.
        
        Returns:
            Dict with command names as keys and metadata as values
        """
        metadata = {}
        for name, command_class in self._commands.items():
            metadata[name] = command_class.get_metadata()
        return metadata
    
    def get_all_commands_info(self) -> Dict[str, Dict[str, Any]]:
        """
        Gets information about all registered commands.

        Returns:
            Dictionary with information about all commands.
        """
        commands_info = {}
        for name in self._commands:
            commands_info[name] = self.get_command_info(name)
        return commands_info
    
    def discover_commands(self, package_path: str = "mcp_proxy_adapter.commands") -> None:
        """
        Automatically discovers and registers commands in the specified package.

        Args:
            package_path: Path to package with commands.
        """
        logger.info(f"Discovering commands in package: {package_path}")
        
        try:
            package = importlib.import_module(package_path)
            package_dir = os.path.dirname(package.__file__ or "")
            
            for _, module_name, is_pkg in pkgutil.iter_modules([package_dir]):
                if is_pkg:
                    # Recursively traverse subpackages
                    self.discover_commands(f"{package_path}.{module_name}")
                elif module_name.endswith("_command"):
                    # Import only command modules
                    module_path = f"{package_path}.{module_name}"
                    logger.debug(f"Found command module: {module_path}")
                    
                    try:
                        module = importlib.import_module(module_path)
                        
                        # Find all command classes in the module
                        for name, obj in inspect.getmembers(module):
                            if (inspect.isclass(obj) and 
                                issubclass(obj, Command) and 
                                obj != Command and
                                not inspect.isabstract(obj)):
                                
                                # Get command name before registration
                                command_name = obj.name if hasattr(obj, "name") and obj.name else obj.__name__.lower()
                                if command_name.endswith("command"):
                                    command_name = command_name[:-7]  # Remove "command" suffix
                                
                                # Register the command only if it doesn't exist
                                if not self.command_exists(command_name):
                                    self.register(cast(Type[Command], obj))
                                else:
                                    logger.debug(f"Command '{command_name}' is already registered, skipping")
                    except ValueError as e:
                        # Skip already registered commands
                        logger.debug(f"Skipping command registration: {str(e)}")
                    except Exception as e:
                        logger.error(f"Error loading command module {module_path}: {e}")
        except Exception as e:
            logger.error(f"Error discovering commands: {e}")
            
    def clear(self) -> None:
        """
        Clears command registry.
        """
        logger.debug("Clearing command registry")
        self._commands.clear()


# Global command registry instance
registry = CommandRegistry()
