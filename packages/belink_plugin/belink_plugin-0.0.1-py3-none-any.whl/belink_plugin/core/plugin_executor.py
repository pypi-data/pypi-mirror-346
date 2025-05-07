from belink_plugin.config.config import BelinkPluginEnv
from belink_plugin.core.entities.plugin.request import ToolInvokeRequest
from belink_plugin.core.plugin_registration import PluginRegistration
from belink_plugin.entities.tool import ToolRuntime


class PluginExecutor:
    def __init__(self, config: BelinkPluginEnv, registration: PluginRegistration) -> None:
        self.config = config
        self.registration = registration


    def invoke_tool(self, request: ToolInvokeRequest):
        provider_cls = self.registration.get_tool_provider_cls(request.provider)
        if provider_cls is None:
            raise ValueError(f"Provider `{request.provider}` not found")

        tool_cls = self.registration.get_tool_cls(request.provider, request.tool)
        if tool_cls is None:
            raise ValueError(f"Tool `{request.tool}` not found for provider `{request.provider}`")

        # instantiate tool
        tool = tool_cls(
            runtime=ToolRuntime(
                credentials=request.credentials,
                user_id=request.user_id,
            )
        )

        # invoke tool
        test = yield from tool.invoke(request.tool_parameters)