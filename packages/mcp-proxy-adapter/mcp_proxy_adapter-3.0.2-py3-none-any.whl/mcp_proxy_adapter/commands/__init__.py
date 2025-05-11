"""
Package with command implementation.
"""

from mcp_proxy_adapter.commands.base import Command
from mcp_proxy_adapter.commands.result import CommandResult, SuccessResult, ErrorResult
from mcp_proxy_adapter.commands.command_registry import registry, CommandRegistry

# Automatically discover and register commands
registry.discover_commands()

__all__ = [
    "Command",
    "CommandResult",
    "SuccessResult", 
    "ErrorResult",
    "registry",
    "CommandRegistry"
]
