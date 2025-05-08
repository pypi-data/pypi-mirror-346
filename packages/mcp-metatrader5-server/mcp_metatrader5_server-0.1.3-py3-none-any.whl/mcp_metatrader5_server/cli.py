"""
MetaTrader 5 MCP Server - Command Line Interface

This module provides a command-line interface for the MetaTrader 5 MCP server.
"""

import argparse
import logging
import os
import sys
import subprocess
from importlib.metadata import version

from mcp_metatrader5_server.main import mcp

logger = logging.getLogger("mt5-mcp-server.cli")

def get_version():
    """Get the package version."""
    try:
        return version("mcp-metatrader5-server")
    except Exception:
        return "0.1.0"  # Default version if not installed

def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="MetaTrader 5 MCP Server - A Model Context Protocol server for MetaTrader 5"
    )
    
    parser.add_argument(
        "--version", "-v", action="store_true", help="Show version and exit"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Dev command
    dev_parser = subparsers.add_parser("dev", help="Run the server in development mode")
    dev_parser.add_argument(
        "--host", type=str, default="127.0.0.1", help="Host to bind to"
    )
    dev_parser.add_argument(
        "--port", type=int, default=8000, help="Port to bind to"
    )
    
    # Install command
    install_parser = subparsers.add_parser("install", help="Install the server for Claude Desktop")
    
    args = parser.parse_args()
    
    if args.version:
        print(f"mcp-metatrader5-server version {get_version()}")
        return 0
    
    if args.command == "dev":
        # Run in development mode
        os.environ["MT5_MCP_DEV_MODE"] = "true"
        try:
            # Use uvicorn directly
            import uvicorn
            logger.info(f"Starting server at {args.host}:{args.port}")
            uvicorn.run(
                "mcp_metatrader5_server.main:mcp.app",
                host=args.host,
                port=args.port,
                reload=True
            )
            return 0
        except ImportError:
            # If uvicorn is not available, try using the command line
            cmd = [sys.executable, "-m", "uvicorn", "mcp_metatrader5_server.main:mcp.app", 
                   f"--host={args.host}", f"--port={args.port}", "--reload"]
            logger.info(f"Running command: {' '.join(cmd)}")
            return subprocess.call(cmd)
    elif args.command == "install":
        # Install for Claude Desktop
        try:
            from mcp.cli import install_mcp
            logger.info("Installing MCP server for Claude Desktop")
            install_mcp("mcp_metatrader5_server.main:mcp")
            return 0
        except ImportError:
            logger.error("Could not import mcp.cli. Please install the mcp package with pip install mcp[cli]")
            return 1
    else:
        parser.print_help()
        return 1

if __name__ == "__main__":
    sys.exit(main())
