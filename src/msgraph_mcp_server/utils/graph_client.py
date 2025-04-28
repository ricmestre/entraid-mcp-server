"""Microsoft Graph client utility.

This module provides a utility class for making requests to the Microsoft Graph API.
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional, Union

from msgraph import GraphServiceClient
from msgraph.generated.models.user import User as MSGraphUser
from msgraph.generated.users.users_request_builder import UsersRequestBuilder

from auth.graph_auth import GraphAuthManager
from models.user import User


class GraphClient:
    """Client utility for making requests to Microsoft Graph API."""
    
    def __init__(self, auth_manager: GraphAuthManager):
        """Initialize the GraphClient.
        
        Args:
            auth_manager: GraphAuthManager instance for authentication
        """
        self.auth_manager = auth_manager
        self._client = None
        self.logger = logging.getLogger(__name__)
    
    def _get_client(self) -> GraphServiceClient:
        """Get or create a Graph client.
        
        Returns:
            Initialized GraphServiceClient
        """
        if self._client is None:
            self._client = self.auth_manager.get_graph_client()
        return self._client
    
    async def get_me(self) -> User:
        """Get the current user's profile.
        
        Returns:
            User object representing the current user
        """
        try:
            client = self._get_client()
            ms_user = await client.me.get()
            
            # Convert MS Graph User to our User model
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
            
            return User.from_dict(user_data)
            
        except Exception as e:
            self.logger.error(f"Error fetching current user: {str(e)}")
            raise
    
    async def search_users(self, query: str, limit: int = 10) -> List[Dict[str, str]]:
        """Search for users by name or email.
        
        Args:
            query: Search query (name or email)
            limit: Maximum number of results to return
            
        Returns:
            List of user dictionaries with all User model fields
        """
        try:
            client = self._get_client()
            
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
            
            # Format the response with all User model fields
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
            self.logger.error(f"Error searching users: {str(e)}")
            raise
    
    async def send_email(self, email_data: Dict[str, Any]) -> None:
        """Send an email.
        
        Args:
            email_data: Email data in Microsoft Graph format
            
        Returns:
            None
        """
        try:
            client = self._get_client()
            
            # Prepare the message request
            message = email_data.get("message", {})
            
            # Send the email using the Graph client
            client.me.send_mail.post(
                body={
                    "message": {
                        "subject": message.get("subject"),
                        "body": message.get("body"),
                        "toRecipients": message.get("toRecipients"),
                        "ccRecipients": message.get("ccRecipients"),
                        "bccRecipients": message.get("bccRecipients")
                    }
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error sending email: {str(e)}")
            raise
    
    async def get_user(self, user_id: str) -> User:
        """Get a user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            User object
        """
        try:
            client = self._get_client()
            ms_user = client.users.by_user_id(user_id).get()
            
            # Convert MS Graph User to our User model
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
            
            return User.from_dict(user_data)
            
        except Exception as e:
            self.logger.error(f"Error fetching user {user_id}: {str(e)}")
            raise 