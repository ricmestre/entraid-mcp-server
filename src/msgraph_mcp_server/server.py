"""Microsoft Graph MCP Server.

This module provides the main FastMCP server implementation for
interacting with Microsoft Graph services.
"""

import logging
from typing import Dict, List
from fastmcp import FastMCP, Context

from auth.graph_auth import GraphAuthManager, AuthenticationError
from utils.graph_client import GraphClient

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create an MCP server
mcp = FastMCP("EntraID MCP Server")

# Initialize Graph client
try:
    auth_manager = GraphAuthManager()
    graph_client = GraphClient(auth_manager)
    logger.info("Successfully initialized Graph client")
except AuthenticationError as e:
    logger.error(f"Failed to initialize Graph client: {str(e)}")
    raise

@mcp.tool()
async def search_users(query: str, ctx: Context, limit: int = 10) -> List[Dict[str, str]]:
    """Search for users by name or email.
    
    Args:
        query: Search query (name or email)
        ctx: Context object
        limit: Maximum number of results to return (default: 10)
    """
    await ctx.info(f"Searching for users matching '{query}'...")
    
    try:
        users = await graph_client.search_users(query, limit)
        await ctx.report_progress(progress=100, total=100)
        return users
    except AuthenticationError as e:
        error_msg = f"Authentication error: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Error searching users: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise

# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"