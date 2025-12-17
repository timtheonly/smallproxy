from pydantic import BaseModel, AfterValidator
from typing import Annotated
import validators


def is_valid_url(value: str) -> str:
    result = validators.url(value)
    if not result:
        raise ValueError(f"Invalid url value {result}")
    return value


def is_valid_short_id(value: str) -> str:
    if not value.isalnum() or len(value) < 3:
        raise ValueError(
            "Short url id must be greater than 3 characters and alphanumeric"
        )
    return value


class ShortUrl(BaseModel):
    short_url_id: Annotated[str, AfterValidator(is_valid_short_id)]
    long_url: Annotated[str, AfterValidator(is_valid_url)]
