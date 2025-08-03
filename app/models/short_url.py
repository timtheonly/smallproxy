from pydantic import BaseModel


class ShortUrl(BaseModel):
    short_url_id: str
    long_url: str
