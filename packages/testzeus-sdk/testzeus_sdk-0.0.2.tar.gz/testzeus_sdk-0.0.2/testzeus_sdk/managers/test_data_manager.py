"""
TestData manager class for TestZeus test data operations.
"""

from typing import Dict, Any, Optional, List
from testzeus_sdk.client import TestZeusClient
from testzeus_sdk.managers.base import BaseManager
from testzeus_sdk.models.test_data import TestData
from testzeus_sdk.utils.helpers import get_id_by_name


class TestDataManager(BaseManager[TestData]):
    """
    Manager class for TestZeus test data entities.

    This class provides CRUD operations and specialized methods
    for working with test data entities.
    """

    def __init__(self, client: TestZeusClient) -> None:
        """
        Initialize a TestDataManager.

        Args:
            client: TestZeus client instance
        """
        super().__init__(client, "test_data", TestData)

    def create(self, data: Dict[str, Any]) -> TestData:
        """
        Create a new test data entity.

        Args:
            data: Test data with potentially name-based references

        Returns:
            Created test data instance
        """
        # Set default status if not provided
        if "status" not in data:
            data["status"] = "draft"

        # Set default type if not provided
        if "type" not in data:
            data["type"] = "test"

        return super().create(data)

    def _process_references(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process name-based references to ID-based references.

        Args:
            data: Test data with potential name-based references

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
