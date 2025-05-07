import os

from belink_plugin.config.config import BelinkPluginEnv
from belink_plugin.core.entities.plugin.setup import PluginConfiguration
from belink_plugin.core.utils.class_loader import load_single_subclass_from_source
from belink_plugin.core.utils.yaml_loader import load_yaml_file
from belink_plugin.interfaces.tool import ToolProvider, Tool
from belink_plugin.entities.tool import ToolProviderConfiguration, ToolConfiguration


class PluginRegistration:
    configuration: PluginConfiguration
    tools_configuration: list[ToolProviderConfiguration]
    tools_mapping: dict[
        str,
        tuple[
            ToolProviderConfiguration,
            type[ToolProvider],
            dict[str, tuple[ToolConfiguration, type[Tool]]],
        ],
    ]


    def __init__(self, config: BelinkPluginEnv) -> None:
        self.tools_configuration = []
        self.tools_mapping = {}

        # load plugin configuration
        self._load_plugin_configuration()
        # load plugin class
        self._resolve_plugin_cls()

    def _load_plugin_configuration(self):
        """
        load basic plugin configuration from manifest.yaml
        """
        try:
            file = load_yaml_file("manifest.yaml")
            self.configuration = PluginConfiguration(**file)

            for provider in self.configuration.plugins.tools:
                fs = load_yaml_file(provider)
                tool_provider_configuration = ToolProviderConfiguration(**fs)
                self.tools_configuration.append(tool_provider_configuration)
            # for provider in self.configuration.plugins.models:
            #     fs = load_yaml_file(provider)
            #     model_provider_configuration = ModelProviderConfiguration(**fs)
            #     self.models_configuration.append(model_provider_configuration)
            # for provider in self.configuration.plugins.endpoints:
            #     fs = load_yaml_file(provider)
            #     endpoint_configuration = EndpointProviderConfiguration(**fs)
            #     self.endpoints_configuration.append(endpoint_configuration)
            # for provider in self.configuration.plugins.agent_strategies:
            #     fs = load_yaml_file(provider)
            #     agent_provider_configuration = AgentStrategyProviderConfiguration(**fs)
            #     self.agent_strategies_configuration.append(agent_provider_configuration)

        except Exception as e:
            raise ValueError(f"Error loading plugin configuration: {e!s}") from e

    def _resolve_plugin_cls(self):
        """
        register all plugin extensions
        """
        # load tool providers and tools
        self._resolve_tool_providers()

    def _resolve_tool_providers(self):
        """
        walk through all the tool providers and tools and load the classes from sources
        """
        for provider in self.tools_configuration:
            # load class
            source = provider.extra.python.source
            # remove extension
            module_source = os.path.splitext(source)[0]
            # replace / with .
            module_source = module_source.replace("/", ".")
            cls = load_single_subclass_from_source(
                module_name=module_source,
                script_path=os.path.join(os.getcwd(), source),
                parent_type=ToolProvider,
            )

            # load tools class
            tools = {}
            for tool in provider.tools:
                tool_source = tool.extra.python.source
                tool_module_source = os.path.splitext(tool_source)[0]
                tool_module_source = tool_module_source.replace("/", ".")
                tool_cls = load_single_subclass_from_source(
                    module_name=tool_module_source,
                    script_path=os.path.join(os.getcwd(), tool_source),
                    parent_type=Tool,
                )

                if tool_cls._is_get_runtime_parameters_overridden():
                    tool.has_runtime_parameters = True

                tools[tool.identity.name] = (tool, tool_cls)

            print(f"load provider {provider.identity.name} {tools}")
            self.tools_mapping[provider.identity.name] = (provider, cls, tools)

    def get_tool_provider_cls(self, provider: str):
        """
        get the tool provider class by provider name
        :param provider: provider name
        :return: tool provider class
        """
        for provider_registration in self.tools_mapping:
            if provider_registration == provider:
                return self.tools_mapping[provider_registration][1]

    def get_tool_cls(self, provider: str, tool: str):
        """
        get the tool class by provider
        :param provider: provider name
        :param tool: tool name
        :return: tool class
        """
        for provider_registration in self.tools_mapping:
            if provider_registration == provider:
                registration = self.tools_mapping[provider_registration][2].get(tool)
                if registration:
                    return registration[1]