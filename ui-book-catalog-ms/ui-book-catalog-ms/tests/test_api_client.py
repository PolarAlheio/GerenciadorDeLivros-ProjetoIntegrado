from __future__ import annotations

from typing import Any, Dict

import responses

from src.api_client import BookCatalogClient, DEFAULT_BASE_URL


def add_json_response(mock: responses.RequestsMock, method: str, path: str, status: int, body: Dict[str, Any]) -> None:
    mock.add(method, f"{DEFAULT_BASE_URL}{path}", json=body, status=status)


def test_list_books_success() -> None:
    client = BookCatalogClient()
    with responses.RequestsMock() as mock:
        add_json_response(
            mock,
            method=responses.GET,
            path="/catalog/books",
            status=200,
            body=[{"title": "A", "author": "B", "isbn": "1", "publisher": "P", "pages": 10}],
        )
        result = client.list_books()

    assert result.success is True
    assert isinstance(result.data, list)
    assert result.data[0]["isbn"] == "1"


def test_add_book_failure() -> None:
    client = BookCatalogClient()
    with responses.RequestsMock() as mock:
        mock.add(
            responses.POST,
            f"{DEFAULT_BASE_URL}/catalog/books",
            json={"detail": "Invalid data"},
            status=400,
        )
        result = client.add_book({"title": "", "author": "", "isbn": "x", "publisher": "p", "pages": 0})

    assert result.success is False
    assert result.status_code == 400
    assert "Invalid" in (result.error_message or "")


def test_extract_error_handles_non_json() -> None:
    client = BookCatalogClient()
    with responses.RequestsMock() as mock:
        mock.add(
            responses.GET,
            f"{DEFAULT_BASE_URL}/catalog/books/999",
            body="Not found",
            status=404,
        )
        result = client.get_book("999")

    assert result.success is False
    assert result.error_message == "Not found"
