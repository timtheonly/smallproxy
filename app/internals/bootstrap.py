from fastapi import FastAPI
from logging import Logger, getLogger, StreamHandler, FileHandler, INFO, ERROR

from app.internals.logging.json_formatter import JSONFormatter
from app.lib.config import Config

config = Config()


def bootstrap_routers(fast_api: FastAPI) -> FastAPI:
    from app.routers import routers

    for router in routers:
        fast_api.include_router(router)
    return fast_api


def setup_logging() -> None:
    request_logger: Logger = getLogger("app_request_logger")
    request_logger.setLevel(INFO)
    request_log_file_handler = FileHandler(f"{config.get('logbase')}/request.log")
    request_log_file_handler.setLevel(INFO)
    request_log_file_handler.setFormatter(JSONFormatter())
    request_logger.addHandler(request_log_file_handler)

    error_logger: Logger = getLogger("app_error_logger")
    error_logger.setLevel(ERROR)
    error_log_file_handler = FileHandler(f"{config.get('logbase')}/error.log")
    error_log_file_handler.setLevel(ERROR)
    error_log_file_handler.setFormatter(JSONFormatter())
    error_logger.addHandler(error_log_file_handler)

    if config.get("env") == "DEV":
        request_log_stream_handler = StreamHandler()
        request_log_stream_handler.setLevel(INFO)
        request_log_stream_handler.setFormatter(JSONFormatter(pretty=True))
        request_logger.addHandler(request_log_stream_handler)

        error_log_stream_handler = StreamHandler()
        error_log_stream_handler.setLevel(INFO)
        error_log_stream_handler.setFormatter(JSONFormatter(pretty=True))
        error_logger.addHandler(request_log_stream_handler)
