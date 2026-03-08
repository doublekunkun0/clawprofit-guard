"""Runtime fingerprint helpers for local demo reload and desync detection."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Iterable


ROOT_DIR = Path(__file__).resolve().parents[2]
BACKEND_ROOT = ROOT_DIR / "src" / "claw_profit_guard"
DEMO_ROOT = ROOT_DIR / "web" / "demo"


def _iter_files(paths: Iterable[Path], suffixes: set[str] | None = None) -> Iterable[Path]:
    for path in paths:
        if path.is_file():
            if suffixes is None or path.suffix in suffixes:
                yield path
            continue
        if not path.exists():
            continue
        for child in sorted(path.rglob("*")):
            if child.is_file() and (suffixes is None or child.suffix in suffixes):
                yield child


def _fingerprint(paths: Iterable[Path], suffixes: set[str] | None = None) -> str:
    digest = hashlib.sha256()
    for path in _iter_files(paths, suffixes=suffixes):
        relative = path.relative_to(ROOT_DIR).as_posix().encode("utf-8")
        digest.update(relative)
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def compute_backend_fingerprint() -> str:
    return _fingerprint((ROOT_DIR / "run.py", BACKEND_ROOT), suffixes={".py"})


def compute_demo_asset_fingerprint() -> str:
    return _fingerprint((DEMO_ROOT,), suffixes={".html", ".css", ".js"})


def short_fingerprint(value: str, length: int = 12) -> str:
    return value[:length]
