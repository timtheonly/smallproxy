from abc import ABC, abstractmethod
from app.models.short_url import ShortUrl


class ShortUrlRepo(ABC):
    @abstractmethod
    def get(self, short_url_id: str) -> ShortUrl | None:
        pass

    @abstractmethod
    def get_all(self) -> list[ShortUrl]:
        pass

    @abstractmethod
    def set(self, short_url: ShortUrl) -> bool:
        pass

    @abstractmethod
    def delete(self, short_url_id: str) -> bool:
        pass

    @abstractmethod
    def update(self, short_url_id: str, short_url: ShortUrl) -> bool:
        pass
