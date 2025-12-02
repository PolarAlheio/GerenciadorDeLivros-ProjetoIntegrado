# Book Catalog UI

A concise Streamlit front-end for the existing **Book Catalog Service** (FastAPI). The UI focuses on clarity and academic demonstration rather than production complexity.

## Features
- Browse, add, update, and delete books.
- Bulk import/export in JSON or XML with bundled sample payloads.
- Undo support to inspect restored catalog states.
- Graceful error handling for connectivity and API errors.

## Requirements
- Python 3.13+
- Dependencies listed in `requirements.txt` (install via `pip install -r requirements.txt`).
- Running backend at `http://127.0.0.1:8000` (override with `BOOK_CATALOG_API_URL`).

## Running the app
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Running tests
```bash
pip install -r requirements.txt
pytest
```
