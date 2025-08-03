import logging
import traceback
from app.internals.middleware import Middleware
from starlette.types import Scope, Send, Receive
from fastapi.responses import PlainTextResponse


class ExceptionMiddleware(Middleware):
    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        try:
            await self.app(scope, receive, send)
        except Exception as exc:
            logger = logging.getLogger("app_error_logger")
            logger.error(
                f"Unhandled exception - {type(exc).__name__}",
                extra={"traceback": traceback.format_exc()},
            )
            response = PlainTextResponse("Internal server error!!", status_code=500)
            await response(scope, receive, send)
            return
