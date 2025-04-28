"""Microsoft Graph MCP Server.

This module provides the main FastMCP server implementation for
interacting with Microsoft Graph services.
"""

import logging
from typing import Dict, List, Optional, Any
from fastmcp import FastMCP, Context

from auth.graph_auth import GraphAuthManager, AuthenticationError
from utils.graph_client import GraphClient
from resources import users, signin_logs, mfa

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
        results = await users.search_users(graph_client, query, limit)
        await ctx.report_progress(progress=100, total=100)
        return results
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

@mcp.tool()
async def get_user_by_id(user_id: str, ctx: Context) -> Optional[Dict[str, Any]]:
    """Get a specific user by their ID.
    
    Args:
        user_id: The unique identifier (ID) of the user.
        ctx: Context object
        
    Returns:
        A dictionary containing the user's details if found, otherwise None.
    """
    await ctx.info(f"Fetching user with ID: {user_id}...")
    
    try:
        result = await users.get_user_by_id(graph_client, user_id)
        await ctx.report_progress(progress=100, total=100)
        if not result:
            await ctx.warning(f"User with ID {user_id} not found.")
        return result
    except AuthenticationError as e:
        error_msg = f"Authentication error: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Error fetching user {user_id}: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise

@mcp.tool()
async def get_user_sign_ins(user_id: str, ctx: Context, days: int = 7) -> List[Dict[str, Any]]:
    """Get sign-in logs for a specific user within the last N days.

    Requires AuditLog.Read.All permission.
    
    Args:
        user_id: The unique identifier (ID) of the user.
        ctx: Context object
        days: The number of past days to retrieve logs for (default: 7).
        
    Returns:
        A list of dictionaries, each representing a sign-in log event.
    """
    await ctx.info(f"Fetching sign-in logs for user {user_id} for the last {days} days...")
    
    try:
        logs = await signin_logs.get_user_sign_in_logs(graph_client, user_id, days)
        await ctx.report_progress(progress=100, total=100)
        if not logs:
            await ctx.info(f"No sign-in logs found for user {user_id} in the last {days} days.")
        return logs
    except AuthenticationError as e:
        error_msg = f"Authentication error: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Error fetching sign-in logs for {user_id}: {str(e)}"
        # Check for permission errors specifically
        if "Authorization_RequestDenied" in str(e):
             error_msg += " (Ensure the application has AuditLog.Read.All permission)"
             await ctx.error(error_msg)
        else:
            await ctx.error(error_msg)
        logger.error(error_msg)
        raise

@mcp.tool()
async def get_user_mfa_status(user_id: str, ctx: Context) -> Optional[Dict[str, Any]]:
    """Get MFA status and methods for a specific user.
    
    Args:
        user_id: The unique identifier of the user.
        ctx: Context object
        
    Returns:
        A dictionary containing MFA status and methods information.
    """
    await ctx.info(f"Fetching MFA status for user {user_id}...")
    
    try:
        result = await mfa.get_mfa_status(graph_client, user_id)
        await ctx.report_progress(progress=100, total=100)
        if not result:
            await ctx.warning(f"No MFA data found for user {user_id}")
        return result
    except AuthenticationError as e:
        error_msg = f"Authentication error: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Error fetching MFA status for {user_id}: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise

@mcp.tool()
async def get_group_mfa_status(group_id: str, ctx: Context) -> List[Dict[str, Any]]:
    """Get MFA status for all members of a group.
    
    Args:
        group_id: The unique identifier of the group.
        ctx: Context object
        
    Returns:
        A list of dictionaries containing MFA status for each group member.
    """
    await ctx.info(f"Fetching MFA status for group {group_id}...")
    
    try:
        results = await mfa.get_group_mfa_status(graph_client, group_id)
        await ctx.report_progress(progress=100, total=100)
        if not results:
            await ctx.warning(f"No MFA data found for group {group_id}")
        return results
    except AuthenticationError as e:
        error_msg = f"Authentication error: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Error fetching group MFA status for {group_id}: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise

@mcp.tool()
async def get_privileged_users(ctx: Context) -> List[Dict[str, Any]]:
    """Get all users who are members of privileged directory roles."""
    await ctx.info("Fetching privileged users...")
    try:
        privileged_users = await users.get_privileged_users(graph_client)
        await ctx.report_progress(progress=100, total=100)
        return privileged_users
    except Exception as e:
        await ctx.error(f"Error fetching privileged users: {str(e)}")
        raise



# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"