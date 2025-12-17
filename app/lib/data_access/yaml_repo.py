import yaml
from functools import lru_cache
from typing import Dict
from app.lib.data_access.short_url_file_repo import ShortUrlFileRepo


class YamlRepo(ShortUrlFileRepo):
    @lru_cache(maxsize=20)
    def _read_from_file(self) -> Dict[str, str]:
        with open("mappings.yml", "r") as f:
            return yaml.full_load(f)

    def _write_to_file(self, mappings: Dict[str, str]) -> None:
        with open("mappings.yml", "w") as f:
            yaml.dump(mappings, f)
