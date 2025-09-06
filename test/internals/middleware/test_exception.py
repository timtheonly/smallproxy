class TestExceptionMiddleware:
    def test_exception(self, test_client):
        response = test_client.get("/e")
        assert response.status_code == 500
        assert response.text == "Internal server error!!"
