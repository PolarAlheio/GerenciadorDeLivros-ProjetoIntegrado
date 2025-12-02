"""Utilities for reading bundled sample catalog files."""
from __future__ import annotations

from pathlib import Path
from typing import List, Optional

SAMPLE_DIR = Path(__file__).resolve().parent.parent / "books_json_sample"


def list_sample_files() -> List[str]:
    """Return a list of available sample file names."""
    if not SAMPLE_DIR.exists():
        return []
    return sorted(file.name for file in SAMPLE_DIR.glob("*.json"))


def load_sample_content(filename: str) -> Optional[str]:
    """Return the raw text content of the chosen sample file."""
    file_path = SAMPLE_DIR / filename
    if not file_path.exists():
        return None
    return file_path.read_text(encoding="utf-8")
