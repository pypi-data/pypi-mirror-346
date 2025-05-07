from abc import ABC

from flask import Flask
from flask.typing import RouteCallable


class HttpServer(ABC):

    app: Flask

    def __init__(self, app: Flask) -> None:
        self.app = app

    def register_route(self, path: str, f: RouteCallable, method = 'POST'):  # noqa: A002
        print(f"testt  {method}")
        self.app.add_url_rule(path, view_func=f, methods=[method])

    def run(self):
        """
        start plugin server
        """
        self.app.run()