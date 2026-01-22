#!/bin/bash
set -e

REPO="404Nikhil/gshell"  
VERSION="v1.0.0"               

OS="$(uname -s)"
BINARY="gsh"

echo "Detected OS: $OS"

if [ "$OS" = "Darwin" ]; then
    URL="https://github.com/$REPO/releases/download/$VERSION/gsh-darwin"
elif [ "$OS" = "Linux" ]; then
    URL="https://github.com/$REPO/releases/download/$VERSION/gsh-linux"
else
    echo "Error: This installer supports macOS and Linux. Windows users should download the .exe manually."
    exit 1
fi

echo "Downloading gsh from $URL..."

INSTALL_DIR="/usr/local/bin"

if [ -w "$INSTALL_DIR" ]; then
    curl -L -o "$INSTALL_DIR/$BINARY" "$URL"
    chmod +x "$INSTALL_DIR/$BINARY"
else
    echo "Password required to install to $INSTALL_DIR"
    sudo curl -L -o "$INSTALL_DIR/$BINARY" "$URL"
    sudo chmod +x "$INSTALL_DIR/$BINARY"
fi

echo ""
echo "✅ Installed successfully!"
echo "Run 'gsh' to get started."