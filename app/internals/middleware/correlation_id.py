import uuid

from starlette.datastructures import MutableHeaders
from starlette.types import Scope, Send, Receive
from app.internals.context import ctx_correlation_id
from app.internals.middleware import Middleware


class CorrelationId(Middleware):
    header_name: str = "X-Correlation-Id"

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http":
            headers = MutableHeaders(scope=scope)
            correlation_id = headers.get(self.header_name.lower())

            if not correlation_id:
                correlation_id = str(uuid.uuid4())
            tkn = ctx_correlation_id.set(correlation_id)

            async def finish_request(message):
                if message["type"] == "http.response.start":
                    response_headers = MutableHeaders(scope=message)
                    response_headers.append(self.header_name.lower(), correlation_id)
                await send(message)

            await self.app(scope, receive, finish_request)
            ctx_correlation_id.reset(tkn)
