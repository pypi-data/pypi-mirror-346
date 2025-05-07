from enum import Enum
from typing import Any

from pydantic import BaseModel

class PluginInvokeType(Enum):
    Tool = "tool"
    Model = "model"
    Endpoint = "endpoint"
    Agent = "agent_strategy"

class ToolActions(Enum):
    ValidateCredentials = "validate_tool_credentials"
    InvokeTool = "invoke_tool"
    GetToolRuntimeParameters = "get_tool_runtime_parameters"

class PluginAccessRequest(BaseModel):
    type: PluginInvokeType
    user_id: str

class ToolInvokeRequest(PluginAccessRequest):
    type: PluginInvokeType = PluginInvokeType.Tool
    action: ToolActions = ToolActions.InvokeTool
    provider: str
    tool: str
    credentials: dict
    tool_parameters: dict[str, Any]

    @classmethod
    def from_json(cls, data):
        return cls(
            user_id=data.get('user_id'),
            provider=data.get('provider'),
            tool=data.get('tool'),
            credentials=data.get('credentials'),
            tool_parameters=data.get('tool_parameters')
        )