from __future__ import annotations
import json
from src.sample_loader import list_sample_files, load_sample_content, SAMPLE_DIR
from typing import Any, Dict
from src.api_client import BookCatalogClient, ApiResponse


def test_list_sample_files_returns_json_files() -> None:
    files = list_sample_files()
    assert files
    assert all(name.endswith(".json") for name in files)


def test_load_sample_content_reads_file() -> None:
    files = list_sample_files()
    first_file = files[0]
    content = load_sample_content(first_file)
    assert content
    assert SAMPLE_DIR.name in str(SAMPLE_DIR)



def test_dummy_import_2_has_expected_structure() -> None:
    content = load_sample_content("dummy_import_2.json")

    # Se o loader retorna string, faz json.loads
    data = json.loads(content) if isinstance(content, str) else content

    assert data["format"] == "json"
    inner = json.loads(data["content"])
    assert "catalog" in inner
    assert isinstance(inner["catalog"], list)
    assert len(inner["catalog"]) >= 1
    

def test_import_catalog_sends_raw_content(monkeypatch) -> None:
    captured: Dict[str, Any] = {}

    def fake_request(self, method: str, path: str, **kwargs: Any) -> ApiResponse:
        captured["method"] = method
        captured["path"] = path
        captured["json"] = kwargs.get("json")
        return ApiResponse(True, {"count": 2}, 200, None)

    monkeypatch.setattr(BookCatalogClient, "_request", fake_request)

    client = BookCatalogClient(base_url="http://testserver")

    content = (
        "{\"catalog\": [{\"title\": \"Imported A\", \"author\": \"Anon\", "
        "\"isbn\": \"5555555555555\", \"publisher\": \"Global\", \"pages\": 100 },"
        "{\"title\": \"Imported B\", \"author\": \"Anon\", "
        "\"isbn\": \"6666666666666\", \"publisher\": \"Global\", \"pages\": 200 }]}"
    )

    resp = client.import_catalog(format_="json", content=content)

    assert captured["method"] == "POST"
    assert captured["path"] == "/catalog/import"
    assert captured["json"]["format"] == "json"
    assert captured["json"]["content"] == content  # <- ponto central
    # se quiser, checa só algo leve da resposta:
    assert resp.data == {"count": 2}
