import json
import uuid
from app.main import app
from app.internals.logging.json_formatter import JSONFormatter
from fastapi.testclient import TestClient
from pytest import fixture


@fixture
def test_client():
    return TestClient(app)


class TestCorrelationId:
    def test_default_correlation_id(self, test_client, caplog):
        # caplog injects its own handler, add JSONFormatter to it
        caplog.handler.formatter = JSONFormatter()

        response = test_client.get("/")
        assert response.status_code == 200
        assert len(caplog.messages) == 1

        json_log = json.loads(
            caplog.text
        )  # using .text only works if there is only 1 log entry

        correlation_id = json_log.get("correlation_id")
        try:
            uuid.UUID(correlation_id, version=4)
        except Exception:
            raise AssertionError

    def test_passed_correlation_id(seld, test_client, caplog):
        # caplog injects its own handler, add JSONFormatter to it
        caplog.handler.formatter = JSONFormatter()
        passed_correlation_id = "blah"
        response = test_client.get(
            "/", headers={"X-Correlation-Id": passed_correlation_id}
        )
        assert response.status_code == 200
        assert len(caplog.messages) == 1

        json_log = json.loads(
            caplog.text
        )  # using .text only works if there is only 1 log entry
        correlation_id = json_log.get("correlation_id")
        assert correlation_id == passed_correlation_id
