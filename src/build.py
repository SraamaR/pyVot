#!/usr/bin/env python3
"""Construit l'exécutable PyVot avec PyInstaller sous Python 3."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys


SOURCE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SOURCE_DIR.parent


def add_data(source: Path, destination: str) -> list[str]:
    """Retourne une option PyInstaller si la ressource existe."""
    if not source.exists():
        return []
    return ["--add-data", f"{source}{os.pathsep}{destination}"]


def main() -> int:
    command = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--onefile",
        "--name",
        "PyVot",
    ]
    command += add_data(SOURCE_DIR / "Images", "Images")
    command += add_data(PROJECT_DIR / "Aide", "Aide")
    command += add_data(PROJECT_DIR / "Donnees", "Donnees")
    command.append(str(SOURCE_DIR / "PyVot.py"))

    try:
        subprocess.run(command, cwd=SOURCE_DIR, check=True)
    except subprocess.CalledProcessError as exc:
        return exc.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
