"""
Tag manager class for TestZeus tag operations.
"""

from typing import Dict, Any, Optional, List
from testzeus_sdk.client import TestZeusClient
from testzeus_sdk.managers.base import BaseManager, record_to_dict
from testzeus_sdk.models.tag import Tag

class TagManager(BaseManager[Tag]):
    """
    Manager class for TestZeus tag entities.

    This class provides CRUD operations and specialized methods
    for working with tag entities.
    """

    def __init__(self, client: TestZeusClient) -> None:
        """
        Initialize a TagManager.

        Args:
            client: TestZeus client instance
        """
        super().__init__(client, "tags", Tag)

    def create(self, name:str, value:str = None) -> Tag:
        """
        Create a new tag.

        Args:
            name: Name of the Tag
            value: Value for the Tag

        Returns:
            Created tag instance
        """
        data = {
            'name': name,
            'value': value
        }
        return super().create(data)
    
    def update(self, id_or_name:str, name:str = None, value:str = None) -> Tag:
        """
        Update a existing tag.

        Args:
            name: Name of the Tag
            value: Value for the Tag

        Returns:
            Updated tag instance
        """
        data = {}
        if name:
            data['name'] = name
        if value:
            data['value'] = value

        return super().update(id_or_name, data)

    def find_or_create(self, name: str, value: Optional[str] = None) -> Tag:
        """
        Find a tag by name or create it if it doesn't exist.

        Args:
            name: Tag name
            value: Optional tag value

        Returns:
            Existing or newly created tag instance
        """
        tenant_id = self.client.get_tenant_id()
        if not tenant_id:
            raise ValueError(
                "User must be authenticated with a tenant to find or create tags"
            )

        # Try to find the tag
        try:
            filter_str = f'name = "{name}" && tenant = "{tenant_id}"'
            result = self.client.pb.collection(
                self.collection_name
            ).get_first_list_item(filter_str)
            return Tag(record_to_dict(result))
        except Exception:
            # Tag doesn't exist, create it
            tag_data = {"name": name, "tenant": tenant_id}

            if value:
                tag_data["value"] = value

            return self.create(tag_data)
