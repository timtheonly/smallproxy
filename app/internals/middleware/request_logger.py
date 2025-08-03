from logging import getLogger, Logger
from typing import Optional
from app.internals.middleware import Middleware
from starlette.types import Scope, Send, Receive


class RequestLogger(Middleware):
    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
        else:
            logger: Logger = getLogger("app_request_logger")

            client_info: Optional[tuple[str, int]] = scope.get("client")
            client_addr = client_info[0] if client_info else None
            log_data = {
                "client_addr": client_addr,
                "method": scope["method"],
                "path": scope["path"],
            }

            if scope["query_string"]:
                log_data["query"] = scope["query_string"]

            async def log_body():
                message = await receive()

                if message["body"]:
                    log_data["body"] = message["body"]

                return message

            async def finish_request(message):
                if message["type"] == "http.response.start":
                    log_data["status"] = message["status"]
                await send(message)

            await self.app(scope, log_body, finish_request)
            logger.info("logging request", extra=log_data)
