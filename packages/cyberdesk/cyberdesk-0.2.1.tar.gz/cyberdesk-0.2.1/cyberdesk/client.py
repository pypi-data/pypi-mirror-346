"""
Cyberdesk Python SDK wrapper client.
"""

from openapi_client.api_reference_client.client import Client
from openapi_client.api_reference_client.api.desktop import (
    get_v1_desktop_id,
    post_v1_desktop,
    post_v1_desktop_id_stop,
    post_v1_desktop_id_computer_action,
    post_v1_desktop_id_bash_action,
)
from openapi_client.api_reference_client.models import (
    PostV1DesktopBody,
    PostV1DesktopIdBashActionBody,
    PostV1DesktopIdComputerActionClickMouseAction,
    PostV1DesktopIdComputerActionDragMouseAction,
    PostV1DesktopIdComputerActionGetCursorPositionAction,
    PostV1DesktopIdComputerActionMoveMouseAction,
    PostV1DesktopIdComputerActionPressKeysAction,
    PostV1DesktopIdComputerActionScreenshotAction,
    PostV1DesktopIdComputerActionScrollAction,
    PostV1DesktopIdComputerActionTypeTextAction,
    PostV1DesktopIdComputerActionWaitAction,
)

class CyberdeskClient:
    """
    Wrapper client for the Cyberdesk API.
    Provides both synchronous and asynchronous methods.
    """
    def __init__(self, api_key: str, base_url: str = "https://api.cyberdesk.io"):
        self.api_key = api_key
        self.client = Client(base_url=base_url, headers={"x-api-key": api_key})

    def get_desktop(self, id: str):
        """Synchronous: Get details of a specific desktop instance."""
        return get_v1_desktop_id.sync(id=id, client=self.client, x_api_key=self.api_key)

    async def async_get_desktop(self, id: str):
        """Async: Get details of a specific desktop instance. Use with 'await'."""
        return await get_v1_desktop_id.asyncio(id=id, client=self.client, x_api_key=self.api_key)

    def launch_desktop(self, timeout_ms: int = None):
        """Synchronous: Create a new virtual desktop instance."""
        body = PostV1DesktopBody(timeout_ms=timeout_ms) if timeout_ms is not None else PostV1DesktopBody()
        return post_v1_desktop.sync(client=self.client, body=body, x_api_key=self.api_key)

    async def async_launch_desktop(self, timeout_ms: int = None):
        """Async: Create a new virtual desktop instance. Use with 'await'."""
        body = PostV1DesktopBody(timeout_ms=timeout_ms) if timeout_ms is not None else PostV1DesktopBody()
        return await post_v1_desktop.asyncio(client=self.client, body=body, x_api_key=self.api_key)

    def terminate_desktop(self, id: str):
        """Synchronous: Stop a running desktop instance."""
        return post_v1_desktop_id_stop.sync(id=id, client=self.client, x_api_key=self.api_key)

    async def async_terminate_desktop(self, id: str):
        """Async: Stop a running desktop instance. Use with 'await'."""
        return await post_v1_desktop_id_stop.asyncio(id=id, client=self.client, x_api_key=self.api_key)

    def execute_computer_action(self, id: str, action: dict):
        """Synchronous: Perform an action on the desktop (mouse, keyboard, etc)."""
        action_type = action.get("type")
        model_cls = {
            "click_mouse": PostV1DesktopIdComputerActionClickMouseAction,
            "scroll": PostV1DesktopIdComputerActionScrollAction,
            "move_mouse": PostV1DesktopIdComputerActionMoveMouseAction,
            "drag_mouse": PostV1DesktopIdComputerActionDragMouseAction,
            "type": PostV1DesktopIdComputerActionTypeTextAction,
            "press_keys": PostV1DesktopIdComputerActionPressKeysAction,
            "wait": PostV1DesktopIdComputerActionWaitAction,
            "screenshot": PostV1DesktopIdComputerActionScreenshotAction,
            "get_cursor_position": PostV1DesktopIdComputerActionGetCursorPositionAction,
        }.get(action_type)
        if model_cls is None:
            raise ValueError(f"Unknown computer action type: {action_type}")
        model = model_cls.from_dict(action)
        return post_v1_desktop_id_computer_action.sync(id=id, client=self.client, body=model, x_api_key=self.api_key)

    async def async_execute_computer_action(self, id: str, action: dict):
        """Async: Perform an action on the desktop (mouse, keyboard, etc). Use with 'await'."""
        action_type = action.get("type")
        model_cls = {
            "click_mouse": PostV1DesktopIdComputerActionClickMouseAction,
            "scroll": PostV1DesktopIdComputerActionScrollAction,
            "move_mouse": PostV1DesktopIdComputerActionMoveMouseAction,
            "drag_mouse": PostV1DesktopIdComputerActionDragMouseAction,
            "type": PostV1DesktopIdComputerActionTypeTextAction,
            "press_keys": PostV1DesktopIdComputerActionPressKeysAction,
            "wait": PostV1DesktopIdComputerActionWaitAction,
            "screenshot": PostV1DesktopIdComputerActionScreenshotAction,
            "get_cursor_position": PostV1DesktopIdComputerActionGetCursorPositionAction,
        }.get(action_type)
        if model_cls is None:
            raise ValueError(f"Unknown computer action type: {action_type}")
        model = model_cls.from_dict(action)
        return await post_v1_desktop_id_computer_action.asyncio(id=id, client=self.client, body=model, x_api_key=self.api_key)

    def execute_bash_action(self, id: str, command: str):
        """Synchronous: Execute a bash command on the desktop."""
        body = PostV1DesktopIdBashActionBody(command=command)
        return post_v1_desktop_id_bash_action.sync(id=id, client=self.client, body=body, x_api_key=self.api_key)

    async def async_execute_bash_action(self, id: str, command: str):
        """Async: Execute a bash command on the desktop. Use with 'await'."""
        body = PostV1DesktopIdBashActionBody(command=command)
        return await post_v1_desktop_id_bash_action.asyncio(id=id, client=self.client, body=body, x_api_key=self.api_key) 