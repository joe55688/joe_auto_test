#!/bin/bash
# Windows 11 Build Script for Joe Auto Test
# Run with: bash build.sh

set -e

echo ""
echo "========================================"
echo "Joe Auto Test - Windows 11 Build Script"
echo "========================================"
echo ""

# Check Python installation
if ! command -v python &> /dev/null; then
    echo "[-] Python not found in PATH"
    echo "[*] Please install Python 3.8+ from https://www.python.org"
    exit 1
fi

python --version
echo ""

# Install build requirements
echo "[*] Installing build requirements..."
pip install -r requirements-build.txt
echo "[+] Build requirements installed"
echo ""

# Clean previous builds
echo "[*] Cleaning previous builds..."
rm -rf build dist JoeAutoTest.spec 2>/dev/null || true
echo "[+] Cleaned"
echo ""

# Build executable
echo "[*] Building Windows 11 executable..."
echo "[*] This may take a few minutes..."
echo ""

python build.py

if [ -f "dist/JoeAutoTest.exe" ]; then
    echo ""
    echo "[+] Build completed successfully!"
    echo ""
    echo "[+] Output: dist/JoeAutoTest.exe"
    
    size=$(du -h dist/JoeAutoTest.exe | cut -f1)
    echo "[+] File size: $size"
    echo ""
    echo "[+] You can now run the executable:"
    echo "    - dist/JoeAutoTest.exe"
    echo ""
else
    echo ""
    echo "[-] Build failed - JoeAutoTest.exe not found"
    exit 1
fi

echo "[+] Done!"
