from typing import Type
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
        return RepoFactory.repo_mapping[repo_name]()
