import os

import yaml
from typing import Any, Dict, Optional, TypeVar
from app.lib.borg import Borg

T = TypeVar("T")


class Config(Borg):
    values: Dict[Any, Any] = {}
    env: str = ""
    base_dir: str = "app/config"
    base_config_file: str = f"{base_dir}/config.yaml"
    local_base_config: str = f"{base_dir}/config_local.yaml"

    def __init__(self, reload: bool = False):
        """
        :param reload: refresh cached values, used by tests to prevent false failures.
        """
        super(Config, self).__init__()
        self.env = os.getenv("ENV", "DEV")
        if self.env:
            self.env = self.env.lower()
        if reload or not self.values:
            self._load()

    def _load(self):
        self.values = {}  # reset values for a fresh read i.e. don't use cached values
        config_files = [self.base_config_file, self.local_base_config]
        if self.env:
            config_files.append(f"{self.base_dir}/{self.env}_config.yaml")
            config_files.append(f"{self.base_dir}/{self.env}_config_local.yaml")

        for config_file in config_files:
            self.values.update(self._read_config_file(config_file))

    @staticmethod
    def _read_config_file(filename) -> Dict:
        config = {}
        if os.path.exists(filename):
            with open(filename) as config_file:
                config = yaml.full_load(config_file)
        return config

    def get_values(self) -> Optional[Dict]:
        if self.values:
            return self.values
        return None

    def get(self, config_name: str) -> Optional[Any]:
        return self.values.get(config_name)

    def get_with_default(self, config_name: str, default: T) -> T | Optional[Any]:
        if self.values:
            return self.values.get(config_name, default)
        return default
