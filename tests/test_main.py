from pathlib import Path

from intelligent_insurance_agent.main import InsuranceRAGApp


def test_ingest_and_answer_query(tmp_path: Path) -> None:
    document_path = tmp_path / "policy.txt"
    document_path.write_text("This policy covers collision and roadside assistance.", encoding="utf-8")

    app = InsuranceRAGApp()
    indexed_count = app.ingest_documents([document_path])

    assert indexed_count > 0
    response = app.answer_query("What does the policy cover?")
    assert "collision" in response.lower() or "roadside" in response.lower() or "policy" in response.lower()
