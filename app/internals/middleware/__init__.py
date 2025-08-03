from starlette.types import ASGIApp


class Middleware:
    app: ASGIApp

    def __init__(self, app: ASGIApp):
        self.app = app
