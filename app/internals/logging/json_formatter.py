import json
import pytz
from logging import Formatter, LogRecord, ERROR
from app.internals.context import ctx_correlation_id
from datetime import datetime


class JSONFormatter(Formatter):
    pretty: bool
    known_fields: list[str] = [
        "args",
        "asctime",
        "created",
        "exc_info",
        "exc_text",
        "filename",
        "funcName",
        "levelname",
        "levelno",
        "lineno",
        "message",
        "msg",
        "module",
        "msecs",
        "name",
        "pathname",
        "process",
        "processName",
        "relativeCreated",
        "stack_info",
        "thread",
        "threadName",
        "taskName",
    ]

    def __init__(self, pretty: bool = False):
        self.pretty = pretty

    def format(self, record: LogRecord) -> str:
        correlation_id = ctx_correlation_id.get()
        log_dict = {
            "message": record.msg,
            "level": record.levelname,
            "correlation_id": correlation_id,
            "timestamp": str(datetime.now(pytz.UTC)),
        }

        if record.levelname == ERROR and record.exc_info:
            log_dict["exc_info"] = record.exc_info
            log_dict["filename"] = record.filename
            log_dict["lineno"] = record.lineno

        extra_data = {}
        for k, v in record.__dict__.items():
            if k not in self.known_fields:
                try:
                    extra_data[k] = v.decode()
                except Exception:
                    extra_data[k] = v

        log_dict.update(extra_data)

        json_args = {}
        if self.pretty:
            json_args = {"sort_keys": True, "indent": 4}

        return json.dumps(log_dict, **json_args)  # type: ignore[arg-type]
