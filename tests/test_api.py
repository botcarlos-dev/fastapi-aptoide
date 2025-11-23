from fastapi.testclient import TestClient
from app.main import app  

client = TestClient(app)


def test_missing_parameter():
    response = client.get("/aptoide")
    assert response.status_code == 422  # missing query param


def test_package_not_found(monkeypatch):
    # Mock Aptoide response
    async def mock_fetch(_):
        return {"datalist": {"list": []}}

    monkeypatch.setattr("app.main.fetch_from_aptoide", mock_fetch)

    response = client.get("/aptoide?package_name=invalid.package")
    assert response.status_code == 404


def test_valid_response(monkeypatch):
    # Mock valid Aptoide response
    async def mock_fetch(_):
        return {
            "datalist": {
                "list": [
                    {
                        "name": "Test App",
                        "size": 1024 * 1024 * 20,
                        "downloads": 2000000,
                        "package": "com.test.app",
                        "file": {
                            "vername": "1.0.0",
                            "added": "2025-01-01",
                            "screensize": "SMALL",
                            "cpu": "arm64-v8a",
                            "signature": {
                                "sha1": "AA:BB:CC",
                                "owner": "CN=Dev, O=Org, L=City, ST=State, C=US"
                            }
                        }
                    }
                ]
            }
        }

    monkeypatch.setattr("app.main.fetch_from_aptoide", mock_fetch)

    response = client.get("/aptoide?package_name=com.test.app")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test App"
    assert data["downloads"] == "2M"
    assert data["developer_cn"] == "Dev"

