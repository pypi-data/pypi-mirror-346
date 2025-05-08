"""
Main client class for TestZeus SDK.
"""

import os
import json
import aiohttp
import asyncio
from typing import Dict, Any, Optional, List, Union
from pocketbase import PocketBase


class TestZeusClient:
    """
    Client for interacting with TestZeus API.

    This client wraps the PocketBase client and provides access to all TestZeus
    functionality through specialized managers for each entity type.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
    ):
        """
        Initialize the TestZeus client

        Args:
            base_url: TestZeus API base URL
            email: User email for authentication
            password: User password for authentication
        """
        default_url = "https://pb.prod.testzeus.app"
        self.base_url = base_url or os.environ.get("TESTZEUS_BASE_URL", default_url)
        if self.base_url:
            self.base_url = self.base_url.rstrip("/")
        self.email = email or os.environ.get("TESTZEUS_EMAIL")
        self.password = password or os.environ.get("TESTZEUS_PASSWORD")

        # Initialize the PocketBase client
        self.pb = PocketBase(self.base_url)

        # Auth token and session
        self.token = None
        self.session = None
        self._authenticated = False

        # Import here to avoid circular imports
        from testzeus_sdk.managers.test_manager import TestManager
        from testzeus_sdk.managers.test_run_manager import TestRunManager
        from testzeus_sdk.managers.test_data_manager import TestDataManager
        from testzeus_sdk.managers.environment_manager import EnvironmentManager
        from testzeus_sdk.managers.tag_manager import TagManager

        # Import new managers
        from testzeus_sdk.managers.agent_configs_manager import AgentConfigsManager
        from testzeus_sdk.managers.test_device_manager import TestDeviceManager
        from testzeus_sdk.managers.test_designs_manager import TestDesignsManager
        from testzeus_sdk.managers.test_run_dashs_manager import TestRunDashsManager
        from testzeus_sdk.managers.test_run_dash_outputs_manager import (
            TestRunDashOutputsManager,
        )
        from testzeus_sdk.managers.test_run_dash_output_steps_manager import (
            TestRunDashOutputStepsManager,
        )
        from testzeus_sdk.managers.tenant_consumption_manager import (
            TenantConsumptionManager,
        )
        from testzeus_sdk.managers.tenant_consumption_logs_manager import (
            TenantConsumptionLogsManager,
        )
        from testzeus_sdk.managers.test_run_dash_outputs_attachments_manager import (
            TestRunDashOutputsAttachmentsManager
        )

        # Initialize managers
        self.tests = TestManager(self)
        self.test_runs = TestRunManager(self)
        self.test_data = TestDataManager(self)
        self.environments = EnvironmentManager(self)
        self.tags = TagManager(self)

        # Initialize new managers
        self.agent_configs = AgentConfigsManager(self)
        self.test_devices = TestDeviceManager(self)
        self.test_designs = TestDesignsManager(self)
        self.test_run_dashs = TestRunDashsManager(self)
        self.test_run_dash_outputs = TestRunDashOutputsManager(self)
        self.test_run_dash_output_steps = TestRunDashOutputStepsManager(self)
        self.tenant_consumption = TenantConsumptionManager(self)
        self.tenant_consumption_logs = TenantConsumptionLogsManager(self)
        self.test_run_dash_outputs_attachments = TestRunDashOutputsAttachmentsManager(self)

    async def __aenter__(self) -> "TestZeusClient":
        """Context manager entry point"""
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[Exception],
        exc_tb: Optional[asyncio.Task],
    ) -> None:
        """Context manager exit point"""
        if self.session and not self.session.closed:
            await self.session.close()
            self.session = None

    async def ensure_authenticated(self) -> None:
        """
        Ensure the client is authenticated before making API calls
        """
        if self._authenticated:
            # Make sure PocketBase client has the token
            if self.token and not self.pb.auth_store.token:
                self.pb.auth_store.save(self.token, None)
            return

        if self.session is None:
            self.session = aiohttp.ClientSession()

        if self.email and self.password:
            # Username/password authentication
            await self.authenticate(self.email, self.password)
        else:
            raise ValueError(
                "Authentication credentials not provided. "
                "Set email/password via constructor or environment variables."
            )

    async def authenticate(self, email: str, password: str) -> str:
        """
        Authenticate with email and password

        Args:
            email: User email
            password: User password

        Returns:
            Authentication token
        """
        if self.session is None:
            self.session = aiohttp.ClientSession()

        # First authenticate with PocketBase client
        try:
            auth_data = self.pb.collection("users").auth_with_password(email, password)
            self.token = auth_data.token
            self._authenticated = True
            return self.token
        except Exception as e:
            # Fallback to our own authentication if PocketBase client fails
            auth_url = f"{self.base_url}/api/collections/users/auth-with-password"
            auth_data = {
                "identity": email,
                "password": password,
            }

            async with self.session.post(auth_url, json=auth_data) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise ValueError(f"Authentication failed: {error_text}")

                data = await response.json()
                self.token = data.get("token")

                if not self.token:
                    raise ValueError("Authentication succeeded but no token was returned")

                self._authenticated = True
                return self.token

    def _get_headers(self) -> Dict[str, str]:
        """
        Get headers for API requests

        Returns:
            Dictionary of HTTP headers
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        if self.token:
            # Token auth from login
            headers["Authorization"] = f"Bearer {self.token}"

        return headers

    async def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
    ) -> Any:
        """
        Make an API request

        Args:
            method: HTTP method (GET, POST, PATCH, DELETE)
            endpoint: API endpoint (starting with /)
            params: Query parameters
            json_data: JSON body for POST/PATCH requests
            data: Form data for POST requests

        Returns:
            API response as dictionary
        """
        await self.ensure_authenticated()

        if self.session is None:
            self.session = aiohttp.ClientSession()

        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers()

        async with self.session.request(
            method=method,
            url=url,
            params=params,
            json=json_data,
            data=data,
            headers=headers,
        ) as response:
            response_text = await response.text()

            if not response_text:
                # Handle empty responses
                if 200 <= response.status < 300:
                    return {}
                else:
                    raise ValueError(
                        f"Request failed with status {response.status}: Empty response"
                    )

            try:
                import json as json_module

                response_json = json_module.loads(response_text)
            except ValueError:
                if 200 <= response.status < 300:
                    # Success with non-JSON response
                    return {"data": response_text}
                else:
                    # Error with non-JSON response
                    raise ValueError(
                        f"Request failed with status {response.status}: {response_text}"
                    )

            # Check for error response
            if not (200 <= response.status < 300):
                error_message = (
                    response_json.get("message", response_json)
                    if isinstance(response_json, dict)
                    else response_text
                )
                raise ValueError(
                    f"Request failed with status {response.status}: {error_message}"
                )

            return response_json

    def is_authenticated(self) -> bool:
        """
        Check if the client is authenticated

        Returns:
            True if authenticated
        """
        return self._authenticated and self.token is not None

    def logout(self) -> None:
        """
        Logout and clear authentication state
        """
        self.token = None
        self._authenticated = False

    def get_tenant_id(self) -> str:
        """
        Get the current tenant ID

        Returns:
            Tenant ID or empty string if not authenticated or not implemented
        """
        return self.pb.auth_store.model.tenant
    
    def get_user_id(self) -> str:
        """
        Get the current User ID

        Returns:
            User ID or empty string if not authenticated or not implemented
        """
        return self.pb.auth_store.model.id
        
    def get_file_token(self) -> str:
        """
        Get the current file token
        """
        return self.pb.get_file_token()
