from app.lib.config import Config
from app.lib.factory.repo_factory import RepoFactory

config = Config()


def get_repo():
    return RepoFactory.get_repo(config.get("repo_type"))
