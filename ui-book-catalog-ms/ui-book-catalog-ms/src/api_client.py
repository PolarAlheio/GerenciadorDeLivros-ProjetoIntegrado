"""HTTP client for the Book Catalog Service."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional
import os

import requests


DEFAULT_BASE_URL = "http://127.0.0.1:8000"


@dataclass
class ApiResponse:
    """Represents a standardized response from the catalog API."""

    success: bool
    data: Optional[Any] = None
    status_code: Optional[int] = None
    error_message: Optional[str] = None


class BookCatalogClient:
    """Client for interacting with the Book Catalog Service HTTP API."""

    def __init__(self, base_url: Optional[str] = None) -> None:
        env_url = os.getenv("BOOK_CATALOG_API_URL")
        self.base_url = base_url or env_url or DEFAULT_BASE_URL

    def list_books(self) -> ApiResponse:
        """Return all books currently in the catalog."""
        return self._request("GET", "/catalog/books")

    def get_book(self, isbn: str) -> ApiResponse:
        """Return a specific book by ISBN."""
        return self._request("GET", f"/catalog/books/{isbn}")

    def add_book(self, book: Dict[str, Any]) -> ApiResponse:
        """Add a new book to the catalog."""
        return self._request("POST", "/catalog/books", json=book)

    def update_book(self, isbn: str, book: Dict[str, Any]) -> ApiResponse:
        """Update an existing book identified by ISBN."""
        return self._request("PUT", f"/catalog/books/{isbn}", json=book)

    def delete_book(self, isbn: str) -> ApiResponse:
        """Delete a book from the catalog by ISBN."""
        return self._request("DELETE", f"/catalog/books/{isbn}")

    def import_catalog(self, format_: str, content: str) -> ApiResponse:
        """Import a catalog payload in JSON or XML format."""
        payload = {"format": format_, "content": content}
        return self._request("POST", "/catalog/import", json=payload)

    def export_catalog(self, format_: str) -> ApiResponse:
        """Export the current catalog in the requested format."""
        payload = {"format": format_}
        return self._request("POST", "/catalog/export", json=payload)

    def undo_last(self) -> ApiResponse:
        """Undo the last catalog mutation and return the updated state."""
        return self._request("POST", "/catalog/undo")

    def _request(self, method: str, path: str, **kwargs: Any) -> ApiResponse:
        url = f"{self.base_url}{path}"
        try:
            response = requests.request(method, url, timeout=10, **kwargs)
            if response.ok:
                data = response.json() if response.content else None
                return ApiResponse(success=True, data=data, status_code=response.status_code)

            return ApiResponse(
                success=False,
                data=None,
                status_code=response.status_code,
                error_message=self._extract_error(response),
            )
        except requests.RequestException as exc:  # pragma: no cover - network errors
            return ApiResponse(success=False, data=None, status_code=None, error_message=str(exc))

    @staticmethod
    def _extract_error(response: requests.Response) -> str:
        """Extract a short error message from a non-2xx response."""
        try:
            payload = response.json()
            if isinstance(payload, dict) and payload.get("detail"):
                return str(payload.get("detail"))
        except ValueError:
            pass
        return response.text or f"HTTP {response.status_code}"
