#!/usr/bin/env python3
"""Configuration setuptools de PyVot pour Python 3."""

import os
from pathlib import Path

from setuptools import setup


SOURCE_DIR = Path(__file__).resolve().parent
PY_MODULES = sorted(
    path.stem
    for path in SOURCE_DIR.glob("*.py")
    if path.stem not in {"build", "setup"}
)


def resource_files(source: Path, destination: str) -> list[tuple[str, list[str]]]:
    """Conserve l'arborescence des ressources dans ``share/pyvot``."""
    result = []
    if not source.exists():
        return result
    for directory, _, filenames in os.walk(source):
        directory_path = Path(directory)
        relative = directory_path.relative_to(source)
        target = Path("share", "pyvot", destination, relative)
        if filenames:
            result.append((str(target), [str(directory_path / name) for name in filenames]))
    return result


DATA_FILES = []
DATA_FILES += resource_files(SOURCE_DIR / "Images", "Images")
DATA_FILES += resource_files(SOURCE_DIR.parent / "Aide", "Aide")
DATA_FILES += resource_files(SOURCE_DIR.parent / "Donnees", "Donnees")


setup(
    name="pyVot",
    version="0.62",
    author="Cédrick FAURY",
    author_email="cedrick.faury@ac-clermont.fr",
    description="Construction et analyse de liaisons pivot avec roulements",
    url="https://github.com/cedrick-f/pyVot",
    license="GPL-2.0-or-later",
    python_requires=">=3.9",
    py_modules=PY_MODULES,
    package_dir={"": str(SOURCE_DIR)},
    data_files=DATA_FILES,
    install_requires=["wxPython>=4.2"],
    entry_points={"gui_scripts": ["pyvot=PyVot:main"]},
)
