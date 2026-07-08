from fastapi.testclient import TestClient

from intelligent_insurance_agent import api as api_module


client = TestClient(api_module.app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_endpoint():
    response = client.post("/chat", json={"message": "I need a quote"})
    assert response.status_code == 200
    assert "quote" in response.json()["reply"].lower()


def test_upload_and_documents_endpoints(tmp_path, monkeypatch):
    monkeypatch.setattr(api_module, "UPLOAD_DIR", tmp_path)
    tmp_path.mkdir(parents=True, exist_ok=True)

    upload_response = client.post(
        "/upload",
        files={"file": ("policy.pdf", b"dummy pdf content", "application/pdf")},
    )
    assert upload_response.status_code == 200

    documents_response = client.get("/documents")
    assert documents_response.status_code == 200
    data = documents_response.json()
    assert len(data) == 1
    assert data[0]["filename"] == "policy.pdf"
