import pytest
from fastapi import FastAPI, Request, Response, Depends
from fastapi.testclient import TestClient
from semverfastapi.dependencies import check_api_version
from semverfastapi.decorators import available

class DescribeCheckApiVersion:
    @pytest.fixture
    def app(self):
        app = FastAPI()

        @app.middleware("http")
        async def set_api_version(request: Request, call_next):
            version = request.headers.get("X-API-Version")
            if version:
                 request.state.api_version = version
            response = await call_next(request)
            return response

        return app

    def it_redirects_when_header_is_missing(self, app):
        @app.get("/test", dependencies=[Depends(check_api_version)])
        @available(introduced="1.0")
        def test_endpoint():
            return {"message": "ok"}

        client = TestClient(app)

        # No version header -> 307 Redirect to v1.0
        response = client.get("/test", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["Location"] == "/v1.0/test"

    def it_requests_upgrade_for_older_versions(self, app):
        @app.get("/test", dependencies=[Depends(check_api_version)])
        @available(introduced="2.0")
        def test_endpoint():
            return {"message": "ok"}

        client = TestClient(app)

        # Request v1.0 but introduced in v2.0 -> 426
        response = client.get("/test", headers={"X-API-Version": "1.0"})
        assert response.status_code == 426
        assert response.headers["Upgrade"] == "2.0"

    def it_returns_gone_for_removed_versions(self, app):
        @app.get("/test", dependencies=[Depends(check_api_version)])
        @available(introduced="1.0", removed="2.0")
        def test_endpoint():
            return {"message": "ok"}

        client = TestClient(app)

        # Request v2.0 but removed in v2.0 -> 410
        response = client.get("/test", headers={"X-API-Version": "2.0"})
        assert response.status_code == 410

    def it_warns_deprecated_versions(self, app):
        @app.get("/test", dependencies=[Depends(check_api_version)])
        @available(introduced="1.0", deprecated="1.5")
        def test_endpoint():
            return {"message": "ok"}

        client = TestClient(app)

        # Request v1.5 -> Warning header
        response = client.get("/test", headers={"X-API-Version": "1.5"})
        assert response.status_code == 200
        assert "Warning" in response.headers
        assert response.headers["Warning"] == "Deprecated API"
