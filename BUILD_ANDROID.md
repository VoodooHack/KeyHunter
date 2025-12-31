# Building ETH Key Scanner APK for Android

This guide explains how to build the ETH Key Scanner Android app.

## Files Included

- `main.py` - Main Kivy app with Android UI
- `eth_key_scanner.py` - Core scanner logic
- `buildozer.spec` - Build configuration for Android
- `requirements.txt` - Python dependencies

## Option 1: Build Locally (Linux/Mac/WSL2)

### Prerequisites

1. Install system dependencies (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
```

2. Install buildozer:
```bash
pip3 install --user buildozer
pip3 install --user cython
```

3. Install Android SDK and NDK (buildozer will do this automatically on first run)

### Build Steps

1. Place all files in a directory:
```
eth_key_scanner_android/
├── main.py
├── eth_key_scanner.py
├── buildozer.spec
└── requirements.txt
```

2. Navigate to the directory:
```bash
cd eth_key_scanner_android
```

3. Build the APK:
```bash
buildozer -v android debug
```

4. The APK will be generated at:
```
bin/ethkeyscanner-1.0.0-arm64-v8a-debug.apk
```

5. Transfer to your Android device and install

**Note:** First build will take 30-60 minutes as it downloads Android SDK/NDK and compiles dependencies.

## Option 2: Build with GitHub Actions (Cloud)

If you don't have Linux, you can use GitHub Actions to build for you:

1. Create a new GitHub repository
2. Upload all files to the repository
3. Create `.github/workflows/build.yml`:

```yaml
name: Build Android APK

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y git zip unzip openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
        pip install buildozer cython

    - name: Build APK
      run: |
        buildozer android debug

    - name: Upload APK
      uses: actions/upload-artifact@v2
      with:
        name: apk
        path: bin/*.apk
```

4. Push to GitHub and the APK will build automatically
5. Download from the Actions tab

## Option 3: Use Buildozer in Docker

```bash
docker run --rm -v "$(pwd)":/home/user/hostcwd kivy/buildozer android debug
```

## Option 4: Online Build Services

Use services like:
- **Colab** - Use Google Colab with buildozer
- **Replit** - Build in Replit environment
- **Gitpod** - Cloud IDE with buildozer support

## Quick Build Script

Create `build.sh`:
```bash
#!/bin/bash
buildozer android clean
buildozer -v android debug
adb install -r bin/*.apk  # If device connected
```

Make executable and run:
```bash
chmod +x build.sh
./build.sh
```

## Testing on Android

### Using ADB (Android Debug Bridge)

1. Enable USB Debugging on your Android device
2. Connect via USB
3. Install directly:
```bash
adb install bin/ethkeyscanner-1.0.0-arm64-v8a-debug.apk
```

### Manual Installation

1. Transfer APK to phone via:
   - USB cable
   - Email attachment
   - Cloud storage (Google Drive, Dropbox)
   - Direct download from web server

2. On Android:
   - Settings → Security → Allow installation from unknown sources
   - Open the APK file
   - Tap "Install"

## App Features

### Main Interface

- **Active Filters Section**: Shows all loaded filters with checkboxes to enable/disable
- **Load Custom Filter Button**: Opens file browser to load `.py` filter files
- **Batch Size**: Number of keys to generate (1-1000)
- **Etherscan API Key**: Optional, for balance checking
- **Check Balances**: Enable/disable balance checking
- **Generate Keys Button**: Start generation
- **Results Area**: Shows generated keys, addresses, and balances

### Loading Custom Filters

1. Tap "Load Custom Filter (.py)"
2. Browse to your filter file (e.g., `custom_filters_example.py`)
3. Select the file
4. Filters will be automatically detected and loaded
5. Enable/disable them with checkboxes

### Permissions Required

- **Internet**: For checking balances via Etherscan API
- **Storage**: For loading custom filter files

## Troubleshooting

### Build Errors

**Error: "Command failed: ./distribute.sh"**
- Solution: Clean build and retry: `buildozer android clean`

**Error: "Java version"**
- Solution: Install OpenJDK 17: `sudo apt install openjdk-17-jdk`

**Error: "NDK not found"**
- Solution: Buildozer will download automatically, wait for first build

**Error: "Cython compilation failed"**
- Solution: Update Cython: `pip install --upgrade cython`

### Runtime Issues

**App crashes on startup**
- Check logcat: `adb logcat | grep python`
- Ensure all dependencies in `requirements.txt` are included in buildozer.spec

**File chooser not working**
- Grant storage permissions in Android settings
- On Android 11+, use the Downloads folder

**Balance checking not working**
- Check internet connection
- Verify Etherscan API key
- Check logcat for network errors

## Advanced Configuration

### Change App Icon

1. Add `icon.png` (512x512 px) to directory
2. In `buildozer.spec`:
```ini
icon.filename = %(source.dir)s/icon.png
```

### Change Package Name

In `buildozer.spec`:
```ini
package.name = myethscanner
package.domain = com.mycompany
```

### Add More Permissions

In `buildozer.spec`:
```ini
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,CAMERA
```

### Target Latest Android

```ini
android.api = 34
android.minapi = 21
```

## File Size

- Final APK size: ~50-80 MB
- First build downloads: ~1-2 GB (SDK/NDK)
- Subsequent builds: Much faster (5-10 min)

## Performance

- Key generation: ~100-1000 keys/second (depends on device)
- Filter checking: Minimal overhead
- Balance checking: Limited by Etherscan API rate limits

## Security Notes

- App stores private keys in memory only
- No data is transmitted except to Etherscan for balance checks
- Grant storage permission only if loading custom filters
- Review custom filters before loading them

## Support

For build issues, check:
- Buildozer documentation: https://buildozer.readthedocs.io
- Kivy documentation: https://kivy.org/doc/stable/
- Python-for-Android: https://python-for-android.readthedocs.io

## Pre-built APK

If you just want to use the app without building:
1. Download the pre-built APK from the releases page
2. Transfer to Android device
3. Install and run

**WARNING**: Only install APKs from trusted sources!
