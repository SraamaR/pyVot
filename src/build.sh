#!/bin/bash

# build.sh - Script de compilation Linux pour PyVot avec PyInstaller

# Configuration
MAIN_SCRIPT="PyVot.py"
ICON_DIR="Images"
ICON_NAME="logo32b.ico"  # inutile sous Linux mais conservé
DIST_DIR="dist"
BUILD_DIR="build"
SPEC_FILE="PyVot.spec"

echo "Compilation de $MAIN_SCRIPT en exécutable Linux..."

# Vérification de PyInstaller
if ! command -v pyinstaller &> /dev/null; then
    echo "PyInstaller n'est pas installé. Installe-le avec : pip install pyinstaller"
    exit 1
fi

# Nettoyage des anciens fichiers de build
rm -rf "$DIST_DIR" "$BUILD_DIR" "$SPEC_FILE"

# Lancer PyInstaller avec options
pyinstaller --noconfirm --clean \
  --onefile \
  --add-data "$ICON_DIR:$ICON_DIR" \
  "$MAIN_SCRIPT"

# Vérification
if [ -f "$DIST_DIR/PyVot" ]; then
    echo "Compilation réussie : $DIST_DIR/PyVot"
else
    echo "Échec de la compilation"
    exit 1
fi
