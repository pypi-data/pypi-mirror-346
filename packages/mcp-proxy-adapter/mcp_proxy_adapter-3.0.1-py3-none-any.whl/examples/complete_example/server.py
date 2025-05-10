"""
Complete MCP Microservice example.

This example demonstrates a complete microservice application with Docker support,
environment-specific configuration, and multiple commands.
"""

import os
import sys
import argparse
from typing import Dict, Any
from pathlib import Path

import mcp_proxy_adapter as mcp
from mcp_proxy_adapter import MicroService
from mcp_proxy_adapter.commands.command_registry import registry
from mcp_proxy_adapter.core.logging import logger
from mcp_proxy_adapter.config import config

# Add commands directory to path for local imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def parse_args():
    """
    Parse command line arguments.
    
    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(description="MCP Microservice Example")
    parser.add_argument(
        "--config", 
        default="configs/config.dev.yaml",
        help="Path to configuration file"
    )
    return parser.parse_args()


def ensure_directories(config_path: str):
    """
    Create necessary directories based on configuration.
    
    Args:
        config_path: Path to configuration file
    """
    # Extract base directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create logs directory
    os.makedirs(os.path.join(base_dir, "logs"), exist_ok=True)
    
    # Create cache directory
    os.makedirs(os.path.join(base_dir, "cache"), exist_ok=True)
    
    # Create data directory
    os.makedirs(os.path.join(base_dir, "data"), exist_ok=True)


def setup_application(config_file=None):
    """
    Setup and configure the microservice application.
    
    Args:
        config_file: Path to configuration file (optional)
        
    Returns:
        Configured microservice object
    """
    # Parse command line arguments if config_file not provided
    if config_file is None:
        args = parse_args()
        config_file = args.config
    
    # Get absolute path to config file
    current_dir = Path(__file__).parent.absolute()
    config_path = current_dir / config_file
    
    # Fall back to config.json if specified file doesn't exist
    if not config_path.exists():
        config_path = current_dir / "config.json"
    
    # Create necessary directories
    ensure_directories(str(config_path))
    
    # Load configuration if exists
    if config_path.exists():
        config.load_from_file(str(config_path))
        logger.info(f"Loaded configuration from {config_path}")
    else:
        logger.warning(f"Configuration file {config_path} not found, using defaults")
    
    # Create microservice
    service = MicroService(
        title="Complete MCP Microservice Example",
        description="Full-featured microservice with Docker support",
        version="1.0.0",
        config_path=str(config_path) if config_path.exists() else None
    )
    
    # Safely register commands from package
    try:
        # Clear any existing registrations to prevent conflicts
        package_path = "commands"
        
        # Get currently registered commands
        commands = registry.get_all_commands()
        for cmd_name in list(commands.keys()):
            try:
                registry.unregister(cmd_name)
            except Exception as e:
                logger.debug(f"Error unregistering command {cmd_name}: {e}")
        
        # Discover and register commands
        service.discover_commands(package_path)
        logger.info(f"Discovered and registered commands from package: {package_path}")
    except Exception as e:
        logger.error(f"Error discovering commands: {e}")
    
    return service


def main():
    """Run microservice with command discovery."""
    # Setup application
    service = setup_application()
    
    # Check if port is overridden by environment variable (for testing)
    if "TEST_SERVER_PORT" in os.environ:
        port = int(os.environ["TEST_SERVER_PORT"])
        service.port = port
        logger.info(f"Using test port from environment: {port}")
    
    # Run server with parameters from configuration
    service.run()


if __name__ == "__main__":
    main() 