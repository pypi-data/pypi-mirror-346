"""
TestRun manager class for TestZeus test run operations.
"""

from typing import Dict, Any, Optional, List, Union
from testzeus_sdk.client import TestZeusClient
from testzeus_sdk.managers.base import BaseManager
from testzeus_sdk.models.test_run import TestRun
from testzeus_sdk.utils.helpers import get_id_by_name, expand_test_run_tree


class TestRunManager(BaseManager[TestRun]):
    """
    Manager class for TestZeus test run entities.

    This class provides CRUD operations and specialized methods
    for working with test run entities.
    """

    def __init__(self, client: TestZeusClient) -> None:
        """
        Initialize a TestRunManager.

        Args:
            client: TestZeus client instance
        """
        super().__init__(client, "test_runs", TestRun)

    async def create_and_start(self, name:str, test:str) -> TestRun:
        """
        Create and start a test run.

        Args:
            data: Either test run data dictionary or test ID/name

        Returns:
            Created and started test run instance
        """
        
        from testzeus_sdk.managers.test_manager import TestManager

        test_manager = TestManager(self.client)
        test = await test_manager.get_one(test)
        run_data = {
            "name": name,
            "status": "pending",
            "test": test.id,
        }
        return await self.create(run_data)

    async def cancel(self, id_or_name: str) -> TestRun:
        """
        Cancel a test run.

        Args:
            id_or_name: Test run ID or name

        Returns:
            Updated test run instance
        """
        # Get the test run
        test_run = await self.get_one(id_or_name)

        # Check if it's in a cancellable state
        if test_run.status not in ["pending", "running"]:
            raise ValueError(
                f"Test run must be in 'pending' or 'running' status to cancel, but is in '{test_run.status}'"
            )

        # Update to cancelled status
        return await self.update(test_run.id, {"status": "cancelled"})

    async def get_expanded(self, id_or_name: str) -> Dict[str, Any]:
        """
        Get a test run with all expanded details including outputs, steps, and attachments.

        Args:
            id_or_name: Test run ID or name

        Returns:
            Complete test run tree with all details
        """
        # Get the ID if a name was provided
        test_run_id = await self._get_id_from_name_or_id(id_or_name)
        return await expand_test_run_tree(self.client, test_run_id)
    
    async def download_all_attachments(self, id_or_name: str, output_dir: str = ".") -> None:
        """
        Download all attachments for a test run.

        Args:
            id_or_name: Test run ID or name
            output_dir: Directory to save attachments
        """
        
        expanded_test_run = await self.get_expanded(id_or_name)
        attachments = expanded_test_run['test_run_dash_outputs_attachments']
        for attachment in attachments:
            await self.client.test_run_dash_outputs_attachments.download_attachment(attachment['id'], output_dir)
        

    def _process_references(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process name-based references to ID-based references.

        Args:
            data: Test run data with potential name-based references

        Returns:
            Processed data with ID-based references
        """
        result = data.copy()
        tenant_id = self.client.get_tenant_id()

        # Process test reference
        if (
            "test" in result
            and isinstance(result["test"], str)
            and not self._is_valid_id(result["test"])
        ):
            test_id = get_id_by_name(self.client, "tests", result["test"], tenant_id)
            if test_id:
                result["test"] = test_id

        # Process environment reference
        if (
            "environment" in result
            and isinstance(result["environment"], str)
            and not self._is_valid_id(result["environment"])
        ):
            env_id = get_id_by_name(
                self.client, "environment", result["environment"], tenant_id
            )
            if env_id:
                result["environment"] = env_id

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
