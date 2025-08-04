from typing import Type
import logging
from app.internals.exceptions import UnkonwnRepoType
from app.lib.data_access.json_repo import JsonRepo
from app.lib.data_access.sqllite_repo import SQLiteRepo
from app.lib.data_access.short_url_repo import ShortUrlRepo


class RepoFactory:
    repo_mapping: dict[str, Type[ShortUrlRepo]] = {
        "json": JsonRepo,
        "sqlite": SQLiteRepo,
    }

    @staticmethod
    def get_repo(repo_name) -> ShortUrlRepo:
        if RepoFactory.repo_mapping.get(repo_name):
            return RepoFactory.repo_mapping[repo_name]()
        error_logger = logging.getLogger("app_error_logger")
        error_logger.error(f"Unknown ShortUrlRepo type - {repo_name}")
        raise UnkonwnRepoType(repo_name)
