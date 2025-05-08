"""
Manager for users collection.
"""

from typing import Dict, List, Any, Optional, Union
from testzeus_sdk.models.users import Users
from testzeus_sdk.client import TestZeusClient
from .base import BaseManager


class UsersManager(BaseManager):
    """
    Manager for Users resources
    """
    
    def __init__(self, client: TestZeusClient) -> None:
        """
        Initialize the Users manager
        
        Args:
            client: TestZeus client instance
        """
        super().__init__(client, "users", Users)

    def _process_references(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process name-based references to ID-based references
        
        Args:
            data: Entity data with potential name-based references
            
        Returns:
            Processed data with ID-based references
        """
        from testzeus_sdk.utils.helpers import convert_name_refs_to_ids
        
        # Define which fields are relations and what collections they reference
        ref_fields = {
            "tenant": "pbc_138639755",
        }
        
        return convert_name_refs_to_ids(self.client, data, ref_fields)
