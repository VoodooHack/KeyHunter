#!/bin/bash
# Simple build script for ETH Key Scanner APK

set -e

echo "======================================"
echo "ETH Key Scanner - APK Builder"
echo "======================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo -e "${RED}Error: This script must run on Linux${NC}"
    echo "Consider using:"
    echo "  - WSL2 on Windows"
    echo "  - GitHub Actions (see QUICKSTART.md)"
    echo "  - Google Colab"
    exit 1
fi

# Check if buildozer is installed
if ! command -v buildozer &> /dev/null; then
    echo -e "${YELLOW}Buildozer not found. Installing...${NC}"
    pip3 install --user buildozer cython
    export PATH=$PATH:~/.local/bin
fi

# Check for required system packages
echo "Checking system dependencies..."
REQUIRED_PACKAGES="git zip unzip openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libssl-dev"

for pkg in $REQUIRED_PACKAGES; do
    if ! dpkg -l | grep -q "^ii  $pkg"; then
        echo -e "${YELLOW}Missing package: $pkg${NC}"
        echo "Installing system dependencies..."
        sudo apt-get update
        sudo apt-get install -y git zip unzip openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
        break
    fi
done

# Clean previous builds
echo ""
echo "Cleaning previous builds..."
if [ -d ".buildozer" ]; then
    buildozer android clean
fi

# Build APK
echo ""
echo -e "${GREEN}Starting APK build...${NC}"
echo "This may take 30-60 minutes on first build..."
echo ""

buildozer -v android debug

# Check if build succeeded
if [ -f "bin/"*.apk ]; then
    echo ""
    echo -e "${GREEN}======================================"
    echo "✓ Build Successful!"
    echo "======================================${NC}"
    echo ""
    echo "APK Location:"
    ls -lh bin/*.apk
    echo ""
    echo "To install on connected device:"
    echo "  adb install -r bin/*.apk"
    echo ""
    echo "Or transfer the APK to your phone manually."
    echo ""
else
    echo -e "${RED}Build failed! Check the logs above.${NC}"
    exit 1
fi
