from contextvars import ContextVar
from typing import Optional

ctx_correlation_id: ContextVar[Optional[str]] = ContextVar(
    "correlation_id", default=None
)
