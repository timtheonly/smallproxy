import pytest
from app.internals.exceptions import UnkonwnRepoType
from app.lib.factory.repo_factory import RepoFactory
from app.lib.data_access.json_repo import JsonRepo
from app.lib.data_access.sqllite_repo import SQLiteRepo


class TestRepoFactory:
    def test_known_repo_types(self):
        repo = RepoFactory.get_repo("json")
        assert isinstance(repo, JsonRepo)

        repo = RepoFactory.get_repo("sqlite")
        assert isinstance(repo, SQLiteRepo)

    def test_unkown_repo_type(self):
        with pytest.raises(UnkonwnRepoType):
            RepoFactory.get_repo("bananna")
