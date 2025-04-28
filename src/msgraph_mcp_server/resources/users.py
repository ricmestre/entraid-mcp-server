"""User resource module for Microsoft Graph.

This module provides access to Microsoft Graph user resources.
"""

import logging
from typing import Dict, List, Optional, Any

from msgraph.generated.users.users_request_builder import UsersRequestBuilder
from kiota_abstractions.base_request_configuration import RequestConfiguration

from utils.graph_client import GraphClient

logger = logging.getLogger(__name__)

async def search_users(graph_client: GraphClient, query: str, limit: int = 10) -> List[Dict[str, str]]:
    """Search for users by name or email.
    
    Args:
        graph_client: GraphClient instance
        query: Search query (name or email)
        limit: Maximum number of results to return
        
    Returns:
        List of user dictionaries with user details
    """
    try:
        client = graph_client.get_client()
        
        # Create query parameters for the search
        query_params = UsersRequestBuilder.UsersRequestBuilderGetQueryParameters(
            search=[
                f'("displayName:{query}" OR "mail:{query}" OR "userPrincipalName:{query}" OR "givenName:{query}" OR "surName:{query}" OR "otherMails:{query}")'
            ],
            top=limit
        )
        
        # Create request configuration
        request_configuration = UsersRequestBuilder.UsersRequestBuilderGetRequestConfiguration(
            query_parameters=query_params
        )
        request_configuration.headers.add("ConsistencyLevel", "eventual")
        
        # Execute the search
        response = await client.users.get(request_configuration=request_configuration)
        
        # Format the response with all user fields
        formatted_users = []
        if response and response.value:
            for user in response.value:
                user_data = {
                    'id': user.id,
                    'displayName': user.display_name,
                    'mail': user.mail,
                    'userPrincipalName': user.user_principal_name,
                    'givenName': user.given_name,
                    'surname': user.surname,
                    'jobTitle': user.job_title,
                    'officeLocation': user.office_location,
                    'businessPhones': user.business_phones,
                    'mobilePhone': user.mobile_phone
                }
                formatted_users.append(user_data)
        
        return formatted_users
        
    except Exception as e:
        logger.error(f"Error searching users: {str(e)}")
        raise

async def get_user_by_id(graph_client: GraphClient, user_id: str) -> Optional[Dict[str, Any]]:
    """Get a user by their ID.
    
    Args:
        graph_client: GraphClient instance
        user_id: The unique identifier of the user.
        
    Returns:
        A dictionary containing the user's details if found, otherwise None.
    """
    try:
        client = graph_client.get_client()
        ms_user = await client.users.by_user_id(user_id).get()
        
        if ms_user:
            # Convert MS Graph User to our dictionary format
            user_data = {
                'id': ms_user.id,
                'displayName': ms_user.display_name,
                'mail': ms_user.mail,
                'userPrincipalName': ms_user.user_principal_name,
                'givenName': ms_user.given_name,
                'surname': ms_user.surname,
                'jobTitle': ms_user.job_title,
                'officeLocation': ms_user.office_location,
                'businessPhones': ms_user.business_phones,
                'mobilePhone': ms_user.mobile_phone
            }
            return user_data
        else:
            logger.warning(f"User with ID {user_id} not found.")
            return None
            
    except Exception as e:
        logger.error(f"Error fetching user with ID {user_id}: {str(e)}")
        raise

async def get_me(graph_client: GraphClient) -> Optional[Dict[str, Any]]:
    """Get the current user's profile.
    
    Args:
        graph_client: GraphClient instance
    
    Returns:
        Dictionary containing the current user's details
    """
    try:
        client = graph_client.get_client()
        ms_user = await client.me.get()
        
        # Convert MS Graph User to dictionary
        user_data = {
            'id': ms_user.id,
            'displayName': ms_user.display_name,
            'mail': ms_user.mail,
            'userPrincipalName': ms_user.user_principal_name,
            'givenName': ms_user.given_name,
            'surname': ms_user.surname,
            'jobTitle': ms_user.job_title,
            'officeLocation': ms_user.office_location,
            'businessPhones': ms_user.business_phones,
            'mobilePhone': ms_user.mobile_phone
        }
        
        return user_data
        
    except Exception as e:
        logger.error(f"Error fetching current user: {str(e)}")
        raise 