import logging

from flask import Flask, request, Response
from pydantic import BaseModel

from belink_plugin.core.entities.plugin.request import ToolInvokeRequest

from belink_plugin.config.config import BelinkPluginEnv
from belink_plugin.config.logger_format import plugin_logger_handler
from belink_plugin.core.plugin_executor import PluginExecutor
from belink_plugin.core.plugin_registration import PluginRegistration
from belink_plugin.core.server.http_server import HttpServer

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(plugin_logger_handler)


class Plugin(HttpServer):
    def __init__(self, config: BelinkPluginEnv) -> None:
        self.app = Flask(__name__)
        # load plugin configuration
        self.registration = PluginRegistration(config)

        # initialize plugin executor
        self.plugin_executer = PluginExecutor(config, self.registration)

        self._register_request_routes()

    def request_test(self):
        data = request.get_json()

        if not data:
            return "No data provided", 500

        try:
            args = ToolInvokeRequest.from_json(data)
            result = next(self.plugin_executer.invoke_tool(args))
            if isinstance(result, BaseModel):
                res = result.model_dump_json()
                return Response(res, mimetype='application/json')

            return "response can not be json", 500
        except Exception as e:
            return f"request data error {e}", 500



    def _register_request_routes(self):
        """
        Register routes
        """
        self.register_route(
            '/invoke_tool',
            self.request_test
            # ,
        )