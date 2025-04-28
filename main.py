#!/usr/bin/env python
"""Microsoft Graph MCP Server main entry point.

This script creates and runs the Microsoft Graph MCP server.
"""

import argparse
import os
from typing import List, Optional

from src.msgraph_mcp_server.server import create_server


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Microsoft Graph MCP Server")
    
    parser.add_argument(
        "--name",
        default="Microsoft Graph MCP Server",
        help="Name of the MCP server"
    )
    
    parser.add_argument(
        "--tenant-id",
        default=os.environ.get("TENANT_ID"),
        help="Azure tenant ID (default: from TENANT_ID env var)"
    )
    
    parser.add_argument(
        "--client-id",
        default=os.environ.get("CLIENT_ID"),
        help="Azure application client ID (default: from CLIENT_ID env var)"
    )
    
    # Client Secret authentication
    parser.add_argument(
        "--client-secret",
        default=os.environ.get("CLIENT_SECRET"),
        help="Azure application client secret (default: from CLIENT_SECRET env var)"
    )
    
    # Certificate authentication
    parser.add_argument(
        "--certificate-path",
        default=os.environ.get("CERTIFICATE_PATH"),
        help="Path to certificate file (default: from CERTIFICATE_PATH env var)"
    )
    
    parser.add_argument(
        "--certificate-pwd",
        default=os.environ.get("CERTIFICATE_PWD"),
        help="Certificate password (default: from CERTIFICATE_PWD env var)"
    )
    
    parser.add_argument(
        "--scopes",
        nargs="+",
        default=["https://graph.microsoft.com/.default"],
        help="Microsoft Graph API scopes (default: https://graph.microsoft.com/.default)"
    )
    
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse"],
        default="stdio",
        help="Transport to use (default: stdio)"
    )
    
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host to bind to for SSE transport (default: 127.0.0.1)"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=5000,
        help="Port to bind to for SSE transport (default: 5000)"
    )
    
    return parser.parse_args()


def main():
    """Run the Microsoft Graph MCP server."""
    args = parse_args()
    
    # Create and run the server
    server = create_server(
        name=args.name,
        tenant_id=args.tenant_id,
        client_id=args.client_id,
        client_secret=args.client_secret,
        certificate_path=args.certificate_path,
        certificate_pwd=args.certificate_pwd,
        scopes=args.scopes
    )
    
    # Run the server with the specified transport
    server.run(
        transport=args.transport,
        host=args.host,
        port=args.port
    )


if __name__ == "__main__":
    main()
