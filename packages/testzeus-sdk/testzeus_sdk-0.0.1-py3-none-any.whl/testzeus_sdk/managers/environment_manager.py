"""
Environment manager class for TestZeus environment operations.
"""

from typing import Dict, Any, Optional, List, Text, Literal
from testzeus_sdk.client import TestZeusClient
from testzeus_sdk.managers.base import BaseManager
from testzeus_sdk.models.environment import Environment
from testzeus_sdk.utils.helpers import get_id_by_name
from pocketbase.client import FileUpload


class EnvironmentManager(BaseManager[Environment]):
    """
    Manager class for TestZeus environment entities.

    This class provides CRUD operations and specialized methods
    for working with environment entities.
    """

    def __init__(self, client: TestZeusClient) -> None:
        """
        Initialize an EnvironmentManager.

        Args:
            client: TestZeus client instance
        """
        super().__init__(client, "environment", Environment)

    def create(self, name:Text, status:Literal['draft', 'ready', 'deleted'] = 'draft', supporting_data_files:Text = None, data:Text = None, tags:List[Text] = None) -> Environment:
        """
        Create a new environment.

        Args:
            data: Environment data with potentially name-based references

        Returns:
            Created environment instance
        """
        data = {
            'name':name,
            'status': status,
            'data': data,
            'tags': tags
        }

        # Check for supporting_data_files and upload if present
        if supporting_data_files:
            filename = supporting_data_files
            data["supporting_data_files"] = FileUpload(filename, open(filename, 'rb'))

        return super().create(data)

    def update(self, id_or_name:Text, name:Text = None, status:Literal['draft', 'ready', 'deleted'] = None, supporting_data_files:Text = None, env_data:Text = None, tags:List[Text] = None) -> Environment:
        """
        Update an existing environment.

        Args:
            id_or_name: Environment ID or name
            data: Updated environment data with potentially name-based references

        Returns:
            Updated environment instance
        """
        data = {}
        if name:
            data['name'] = name
        if status:
            data['status'] = status
        if env_data:
            data['data'] = env_data
        if tags:
            data['tags'] = tags
        # Check for supporting_data_files and upload if present
        if supporting_data_files:
            filename = supporting_data_files
            data["supporting_data_files"] = FileUpload(filename, open(filename, 'rb'))

        return super().update(id_or_name, data)

    def add_tags(self, id_or_name: str, tags: List[str]) -> Environment:
        """
        Add tags to an environment.

        Args:
            id_or_name: Environment ID or name
            tags: List of tag names or IDs

        Returns:
            Updated environment instance
        """
        # Get the environment
        environment = self.get_one(id_or_name)

        # Process tags
        tag_ids = []
        current_tags = environment.tags or []

        # Add existing tags
        if isinstance(current_tags, list):
            tag_ids.extend(current_tags)

        # Process new tags
        for tag in tags:
            if self._is_valid_id(tag):
                if tag not in tag_ids:
                    tag_ids.append(tag)
            else:
                tag_id = get_id_by_name(self.client, "tags", tag)
                if tag_id and tag_id not in tag_ids:
                    tag_ids.append(tag_id)

        # Update the environment
        return self.update(environment.id, {"tags": tag_ids})

    def _process_references(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process name-based references to ID-based references.

        Args:
            data: Environment data with potential name-based references

        Returns:
            Processed data with ID-based references
        """
        result = data.copy()
        tenant_id = self.client.get_tenant_id()

        # Process tags references
        if "tags" in result and isinstance(result["tags"], list):
            tag_ids = []
            for tag in result["tags"]:
                if isinstance(tag, str):
                    if self._is_valid_id(tag):
                        tag_ids.append(tag)
                    else:
                        tag_id = get_id_by_name(self.client, "tags", tag, tenant_id)
                        if tag_id:
                            tag_ids.append(tag_id)
            result["tags"] = tag_ids

        return result


