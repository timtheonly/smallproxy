import json
from functools import lru_cache
from typing import Dict
from app.lib.data_access.short_url_repo import ShortUrlRepo
from app.models.short_url import ShortUrl


class JsonRepo(ShortUrlRepo):
    @lru_cache(maxsize=20)
    def _read_from_file(self) -> Dict[str, str]:
        with open("mappings.json", "r") as f:
            return json.load(f)

    def _write_to_file(self, mappings: Dict[str, str]) -> None:
        with open("mappings.json", "w") as f:
            json.dump(mappings, f)

    def get(self, short_url_id) -> ShortUrl | None:
        mappings = self._read_from_file()
        if short_url_id in mappings:
            return ShortUrl(short_url_id=short_url_id, long_url=mappings[short_url_id])
        else:
            return None

    def set(self, short_url: ShortUrl) -> bool:
        try:
            mappings = self._read_from_file()
            mappings[short_url.short_url_id] = short_url.long_url
            self._write_to_file(mappings)
            self._read_from_file.cache_clear()
            return True
        except (IOError, AttributeError, ValueError):
            return False

    def delete(self, short_url_id: str) -> bool:
        try:
            mappings = self._read_from_file()
            del mappings[short_url_id]
            self._write_to_file(mappings)
            self._read_from_file.cache_clear()
            return True
        except (IOError, AttributeError, ValueError):
            return False

    def update(self, short_url_id: str, short_url: ShortUrl) -> bool:
        result = self.set(short_url)
        if result:
            if short_url_id != short_url.short_url_id:
                result = self.delete(short_url_id)
        return result
