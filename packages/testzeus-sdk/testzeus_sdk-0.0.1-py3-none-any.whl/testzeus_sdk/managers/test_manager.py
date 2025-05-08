"""
Test manager class for TestZeus test operations.
"""

from typing import Dict, Any, Optional, List, Literal
from testzeus_sdk.client import TestZeusClient
from testzeus_sdk.managers.base import BaseManager
from testzeus_sdk.models.test import Test
from testzeus_sdk.utils.helpers import get_id_by_name
from typing import TypedDict, List, Optional, NotRequired

class TestManager(BaseManager[Test]):
    """
    Manager class for TestZeus test entities.

    This class provides CRUD operations and specialized methods
    for working with test entities.
    """

    def __init__(self, client: TestZeusClient) -> None:
        """
        Initialize a TestManager.

        Args:
            client: TestZeus client instance
        """
        super().__init__(client, "tests", Test)

    def create(self, name:str, test_feature:str, status:Literal['draft', 'ready', 'deleted'] = 'draft', test_data : List[str] = None, tags:List[str] = None, environment:str = None) -> Test:
        """
        Create a new Test entity.

        This method creates a new test record using the provided data.
        If the 'status' field is not specified, it defaults to 'draft'.

        Args:
            name* (str): Name of the test. **Required and Unique**
            test_feature* (str): Associated test feature. **Required.**
            status (str, optional): Status ('draft' by default).
            test_data (List[str]): Test data IDs.
            tags (List[str]): Tag IDs.
            environment (str): Environment ID.

        Returns:
            Test: The created Test instance.
        """
        data = {
            'name': name,
            'status': status,
            'test_feature': test_feature,
            'test_data': test_data,
            'tags': tags,
            'environment': environment,
        }

        return super().create(data)
    
    def update(self, id_or_name:str, name:str = None, test_feature:str = None, status:Literal['draft', 'ready', 'deleted'] = None , test_data : List[str] = None, tags:List[str] = None, environment:str = None) -> Test:
        """
        Update an existing Test entity.

        This method update an existing test record using the provided data.

        Args:
            name* (str): Name of the test. **Required and Unique**
            test_feature* (str): Associated test feature. **Required.**
            status (str, optional): Status.
            test_data (List[str]): Test data IDs.
            tags (List[str]): Tag IDs.
            environment (str): Environment ID.

        Returns:
            Test: The updated Test instance.
        """
        data = {
        key: value for key, value in {
            "name": name,
            "test_feature": test_feature,
            "status": status,
            "test_data": test_data,
            "tags": tags,
            "environment": environment,
        }.items() if value is not None
    }

        return super().update(id_or_name, data)

    async def run_test(
        self,
        id_or_name: str,
        environment: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Create and start a test run for a test.

        Args:
            id_or_name: Test ID or name
            environment: Environment name or ID (optional)
            tags: List of tag names or IDs (optional)

        Returns:
            Created test run data
        """
        # Get the test
        test = await self.get_one(id_or_name)

        # Import here to avoid circular imports
        from testzeus_sdk.managers.test_run_manager import TestRunManager

        test_run_manager = TestRunManager(self.client)

        # Create run data
        run_data = {
            "name": f"Run of {test.name}",
            "status": "pending",
            "test": test.id,
            "test_run": test.id,  # Add this field to fix the validation error
        }

        # Add environment if provided
        if environment:
            if self._is_valid_id(environment):
                run_data["environment"] = environment
            else:
                env_id = get_id_by_name(self.client, "environment", environment)
                if env_id:
                    run_data["environment"] = env_id

        # Add tags if provided
        if tags:
            tag_ids = []
            for tag in tags:
                if self._is_valid_id(tag):
                    tag_ids.append(tag)
                else:
                    tag_id = get_id_by_name(self.client, "tags", tag)
                    if tag_id:
                        tag_ids.append(tag_id)

            if tag_ids:
                run_data["tags"] = tag_ids

        # Create the test run
        return await test_run_manager.create_and_start(run_data)

    def add_tags(self, id_or_name: str, tags: List[str]) -> Test:
        """
        Add tags to a test.

        Args:
            id_or_name: Test ID or name
            tags: List of tag names or IDs

        Returns:
            Updated test instance
        """
        # Get the test
        test = self.get_one(id_or_name)

        # Process tags
        tag_ids = []
        current_tags = test.tags or []

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

        # Update the test
        return self.update(test.id, {"tags": tag_ids})

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

        # Process config reference
        if (
            "config" in result
            and isinstance(result["config"], str)
            and not self._is_valid_id(result["config"])
        ):
            config_id = get_id_by_name(
                self.client, "agent_configs", result["config"], tenant_id
            )
            if config_id:
                result["config"] = config_id

        # Process test_design reference
        if (
            "test_design" in result
            and isinstance(result["test_design"], str)
            and not self._is_valid_id(result["test_design"])
        ):
            design_id = get_id_by_name(
                self.client, "test_designs", result["test_design"], tenant_id
            )
            if design_id:
                result["test_design"] = design_id

        # Process test_data references
        if "test_data" in result and isinstance(result["test_data"], list):
            data_ids = []
            for data_item in result["test_data"]:
                if isinstance(data_item, str):
                    if self._is_valid_id(data_item):
                        data_ids.append(data_item)
                    else:
                        data_id = get_id_by_name(
                            self.client, "test_data", data_item, tenant_id
                        )
                        if data_id:
                            data_ids.append(data_id)
            result["test_data"] = data_ids

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
