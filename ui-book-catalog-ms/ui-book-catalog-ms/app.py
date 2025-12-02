"""Streamlit UI for interacting with the Book Catalog Service."""
from __future__ import annotations

from typing import Any, Dict, List

import streamlit as st
import json 

from src.api_client import BookCatalogClient, ApiResponse
from src.sample_loader import list_sample_files, load_sample_content


st.set_page_config(page_title="Book Catalog UI", layout="wide")


client = BookCatalogClient()


# ---------- Helper utilities ----------

def display_status(response: ApiResponse, success_message: str) -> None:
    """Render a concise status message based on the API response."""
    if response.success:
        st.success(success_message)
    else:
        status = response.status_code or "Connection error"
        detail = response.error_message or "Unexpected error"
        st.error(f"Request failed ({status}): {detail}")


def refresh_catalog() -> List[Dict[str, Any]]:
    """Fetch the catalog and store it in the session state."""
    response = client.list_books()
    if response.success and isinstance(response.data, list):
        st.session_state["catalog"] = response.data
        return response.data
    st.session_state["catalog"] = []
    display_status(response, "Catalog refreshed")
    return []


def get_cached_catalog() -> List[Dict[str, Any]]:
    """Return the cached catalog, refreshing from the API if absent."""
    if "catalog" not in st.session_state:
        return refresh_catalog()
    return st.session_state["catalog"]


# ---------- UI sections ----------

def books_section() -> None:
    st.header("Books")
    st.caption("Browse, create, update, or delete books in the catalog.")

    cols = st.columns([1, 3])
    with cols[0]:
        if st.button("Refresh catalog"):
            refresh_catalog()
    with cols[1]:
        st.write("")

    books = get_cached_catalog()
    if books:
        st.table(books)
    else:
        st.info("No books available. Add a book to begin.")

    st.subheader("Add new book")
    with st.form("add_book_form", clear_on_submit=True):
        title = st.text_input("Title")
        author = st.text_input("Author")
        isbn = st.text_input("ISBN")
        publisher = st.text_input("Publisher")
        pages = st.number_input("Pages", min_value=1, step=1)
        submitted = st.form_submit_button("Add book")
        if submitted:
            payload = {
                "title": title,
                "author": author,
                "isbn": isbn,
                "publisher": publisher,
                "pages": int(pages),
            }
            response = client.add_book(payload)
            display_status(response, "Book created successfully")
            if response.success:
                refresh_catalog()

    st.subheader("Update existing book")
    books = get_cached_catalog()
    isbn_options = [book["isbn"] for book in books] if books else []
    if not isbn_options:
        st.info("No books to update.")
    else:
        selected_isbn = st.selectbox("Select ISBN", isbn_options)
        selected_book = next((b for b in books if b["isbn"] == selected_isbn), None)
        with st.form("update_book_form"):
            title = st.text_input("Title", value=selected_book.get("title", ""))
            author = st.text_input("Author", value=selected_book.get("author", ""))
            publisher = st.text_input("Publisher", value=selected_book.get("publisher", ""))
            pages = st.number_input(
                "Pages", min_value=1, step=1, value=int(selected_book.get("pages", 1))
            )
            submitted = st.form_submit_button("Update book")
            if submitted:
                payload = {
                    "title": title,
                    "author": author,
                    "isbn": selected_isbn,
                    "publisher": publisher,
                    "pages": int(pages),
                }
                response = client.update_book(selected_isbn, payload)
                display_status(response, "Book updated successfully")
                if response.success:
                    refresh_catalog()

    st.subheader("Delete book")
    books = get_cached_catalog()
    isbn_options = [book["isbn"] for book in books] if books else []
    if not isbn_options:
        st.info("No books to delete.")
    else:
        selected_isbn = st.selectbox("ISBN to delete", isbn_options, key="delete_isbn")
        if st.button("Delete book"):
            response = client.delete_book(selected_isbn)
            display_status(response, "Book deleted successfully")
            if response.success:
                refresh_catalog()

def import_export_section() -> None:
    st.header("Import / Export")
    st.caption("Bulk import or export the catalog in JSON or XML.")

    # ---------- IMPORT ----------
    st.subheader("Import catalog")

    sample_files = list_sample_files()
    if sample_files:
        selected_sample = st.selectbox("Load sample file", ["(none)"] + sample_files)
    else:
        selected_sample = "(none)"

    default_content = ""

    if selected_sample != "(none)":
        raw = load_sample_content(selected_sample)
        if raw:
            # agora o textarea mostra o JSON COMPLETO
            default_content = raw

    import_content = st.text_area("Catalog content", value=default_content, height=250)

    if st.button("Import catalog"):
        try:
            parsed = json.loads(import_content)

            # extraímos o formato real do arquivo, ignorando o rádio
            fmt = parsed.get("format")
            inner_content = parsed.get("content")

            if not fmt or not inner_content:
                st.error("Invalid payload: expected keys 'format' and 'content'")
                return

            response = client.import_catalog(fmt, inner_content)

            if response.success:
                count = response.data.get("count", 0)
                st.success(f"Import completed: {count} books added")
                refresh_catalog()
            else:
                display_status(response, "Import failed")
        except Exception as e:
            st.error(f"Invalid JSON input: {e}")

    # ---------- EXPORT ----------
    st.divider()
    st.subheader("Export catalog")
    export_format = st.radio("Export format", ("json", "xml"))
    if st.button("Export catalog"):
        response = client.export_catalog(export_format)
        if response.success and isinstance(response.data, dict):
            content = response.data.get("content", "")
            st.text_area("Exported content", value=content, height=200, disabled=True)
        else:
            display_status(response, "Export failed")



def undo_section() -> None:
    st.header("Undo & Debug")
    st.caption("Inspect state restoration after undo operations.")

    columns = st.columns([1, 1])
    with columns[0]:
        if st.button("Undo last operation"):
            response = client.undo_last()
            if response.success and isinstance(response.data, dict):
                remaining = response.data.get("remaining_undos", 0)
                st.success(f"Undo completed. Remaining undos: {remaining}")
                books = response.data.get("books", [])
                st.table(books)
                st.session_state["catalog"] = books
            else:
                display_status(response, "Undo failed")

    with columns[1]:
        if st.button("Refresh catalog", key="undo_refresh"):
            refresh_catalog()

    current_books = get_cached_catalog()
    if current_books:
        st.subheader("Current catalog")
        st.table(current_books)


# ---------- Layout ----------

def main() -> None:
    st.title("Book Catalog Service UI")
    st.sidebar.title("Navigation")
    section = st.sidebar.radio("Go to", ("Books", "Import / Export", "Undo & Debug"))

    if section == "Books":
        books_section()
    elif section == "Import / Export":
        import_export_section()
    else:
        undo_section()


if __name__ == "__main__":
    main()
