import os
from unittest import mock

from app.lib.config import Config


def mocked_open(filename):
    if filename == "app/config/config.yaml":
        content = """
            database_uri: 'mysql://127.13.11.1/blah'
            secret_key: 'beanz'
            token_expiry_minutes: 10
            token_algorithm: 'HS256'
        """
    elif filename == "app/config/config_local.yaml":
        content = """
            database_uri: 'mysql://database.local/blah'
            secret_key: 'beanz.local'
        """
    elif filename == "app/config/env_config.yaml":
        content = """
            database_uri: 'mysql://database.env/blah'
            secret_key: 'beanz.env'
            token_expiry_minutes: 20
        """
    elif filename == "app/config/env_config_local.yaml":
        content = """
            token_algorithm: 'sha256'
        """
    else:
        raise FileNotFoundError(filename)
    file_obj = mock.mock_open(read_data=content).return_value
    file_obj.__iter__.return_value = content.splitlines(True)
    return file_obj


@mock.patch("os.path.exists")
class TestConfig:
    def tearDown(self) -> None:
        Config(reload=True)  # reset the configs back to current env

    @mock.patch.dict(os.environ, {"ENV": ""})
    def test_base_config(self, mock_exists):
        mock_exists.return_value = True
        with mock.patch("app.lib.config.open", new=mocked_open):
            config = Config(reload=True)
            assert config.get_values() == {
                "database_uri": "mysql://database.local/blah",
                "secret_key": "beanz.local",
                "token_expiry_minutes": 10,
                "token_algorithm": "HS256",
            }

    @mock.patch.dict(os.environ, {"ENV": "env"})
    def test_env_config(self, mock_exists):
        mock_exists.return_value = True
        with mock.patch("app.lib.config.open", new=mocked_open):
            config = Config(reload=True)
            assert config.get_values() == {
                "database_uri": "mysql://database.env/blah",
                "secret_key": "beanz.env",
                "token_expiry_minutes": 20,
                "token_algorithm": "sha256",
            }

    @mock.patch.dict(os.environ, {"ENV": ""})
    def test_get(self, mock_exists):
        mock_exists.return_value = True
        with mock.patch("app.lib.config.open", new=mocked_open):
            config = Config(reload=True)
            assert config.get("token_expiry_minutes") == 10
            assert config.get("token") is None

    @mock.patch.dict(os.environ, {"ENV": ""})
    def test_get_with_default(self, mock_exists):
        mock_exists.return_value = True
        with mock.patch("app.lib.config.open", new=mocked_open):
            config = Config(reload=True)
            assert config.get_with_default("token_expiry_minutes", "POTATO") == 10
            assert config.get_with_default("token", "BEANZ") == "BEANZ"
