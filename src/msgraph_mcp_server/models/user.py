"""User model for Microsoft Graph users."""

from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class User:
    """User model representing a Microsoft Graph user."""
    
    id: str
    display_name: str
    mail: Optional[str] = None
    user_principal_name: Optional[str] = None
    given_name: Optional[str] = None
    surname: Optional[str] = None
    job_title: Optional[str] = None
    office_location: Optional[str] = None
    business_phones: Optional[List[str]] = None
    mobile_phone: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, any]) -> 'User':
        """Create a User instance from a dictionary.
        
        Args:
            data: Dictionary containing user data
            
        Returns:
            User instance
        """
        return cls(
            id=data.get('id'),
            display_name=data.get('displayName'),
            mail=data.get('mail'),
            user_principal_name=data.get('userPrincipalName'),
            given_name=data.get('givenName'),
            surname=data.get('surname'),
            job_title=data.get('jobTitle'),
            office_location=data.get('officeLocation'),
            business_phones=data.get('businessPhones'),
            mobile_phone=data.get('mobilePhone')
        )
    
    def to_dict(self) -> Dict[str, any]:
        """Convert User instance to dictionary.
        
        Returns:
            Dictionary containing user data
        """
        return {
            'id': self.id,
            'displayName': self.display_name,
            'mail': self.mail,
            'userPrincipalName': self.user_principal_name,
            'givenName': self.given_name,
            'surname': self.surname,
            'jobTitle': self.job_title,
            'officeLocation': self.office_location,
            'businessPhones': self.business_phones,
            'mobilePhone': self.mobile_phone
        } 