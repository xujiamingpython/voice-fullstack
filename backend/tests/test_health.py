"""健康检查接口测试。"""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    resp = client.get("/api/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert "deps" in body


def test_root_not_found():
    resp = client.get("/")
    assert resp.status_code == 404
