# Quick Start Guide - ETH Key Scanner for Android

## 🚀 Easiest Way to Get the APK (3 Methods)

### Method 1: Use GitHub Actions (Recommended - No Linux Required!)

This is the **easiest way** if you don't have Linux:

1. **Create a GitHub account** (free): https://github.com

2. **Create a new repository**:
   - Click the "+" icon → "New repository"
   - Name it: `eth-key-scanner`
   - Make it private or public (your choice)
   - Click "Create repository"

3. **Upload files**:
   - Click "uploading an existing file"
   - Drag and drop these files:
     - `main.py`
     - `eth_key_scanner.py`
     - `buildozer.spec`
     - `requirements.txt`
     - `.github/workflows/build.yml` (create folders if needed)
   - Click "Commit changes"

4. **Wait for build** (20-40 minutes):
   - Go to "Actions" tab
   - Watch the build progress (green = success)
   - Once done, click on the workflow run
   - Download the APK from "Artifacts"

5. **Install on Android**:
   - Transfer APK to your phone
   - Enable "Install from unknown sources" in Settings
   - Tap APK and install

**That's it!** GitHub builds it for you in the cloud, for free!

---

### Method 2: Use Google Colab (Quick - Browser Only!)

Run this in a Google Colab notebook:

```python
# Install buildozer
!pip install buildozer cython

# Install system dependencies
!sudo apt-get update
!sudo apt-get install -y openjdk-17-jdk git zip unzip autoconf libtool

# Upload your files to Colab or clone from GitHub
# Then run:
!buildozer android debug

# Download the APK from the 'bin' folder
from google.colab import files
files.download('bin/ethkeyscanner-1.0.0-arm64-v8a-debug.apk')
```

---

### Method 3: Local Build (Linux/Mac/WSL2)

If you have Linux, Mac, or Windows with WSL2:

```bash
# Install buildozer
pip3 install buildozer cython

# Install dependencies (Ubuntu/Debian)
sudo apt install -y git zip unzip openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libssl-dev

# Build
cd eth_key_scanner_android
buildozer android debug

# APK will be in: bin/ethkeyscanner-1.0.0-arm64-v8a-debug.apk
```

---

## 📱 Using the App

### First Time Setup

1. **Install the APK**:
   - Settings → Security → Enable "Unknown sources"
   - Tap the APK file → Install

2. **Grant Permissions**:
   - Storage (for loading custom filters)
   - Internet (for balance checking)

### Basic Usage

1. **Configure Filters**:
   - Default filters are already active
   - Toggle checkboxes to enable/disable
   - Tap "Load Custom Filter" to add your own

2. **Set Parameters**:
   - Batch Size: How many keys to generate (try 10 for testing)
   - API Key: Optional Etherscan key (get free at etherscan.io)
   - Check Balances: Enable to check each address

3. **Generate Keys**:
   - Tap "Generate Keys"
   - Wait for results
   - Keys with balances will be highlighted

### Loading Custom Filters

1. Transfer your custom filter `.py` file to your phone:
   - Via USB cable to Downloads folder
   - Via email attachment
   - Via cloud storage (Drive, Dropbox)

2. In the app:
   - Tap "Load Custom Filter (.py)"
   - Navigate to your file
   - Select it
   - Filters will automatically load

3. Example files to load:
   - `custom_filters_example.py` (included)
   - Any `.py` file with PatternFilter classes

---

## 🎯 Tips for Best Results

### Performance
- Start with small batches (10-50 keys)
- More filters = slower generation
- Balance checking is rate-limited by Etherscan

### Filters
- Use NoRepeating(6) to avoid obvious patterns
- Use NoTripleTriple to avoid AAA BBB patterns
- Add custom filters for specific needs

### API Key
- Free Etherscan key: 5 calls/second
- No key: 1 call/5 seconds
- Get one at: https://etherscan.io/apis

### Storage
- App needs storage permission ONLY if loading custom filters
- Deny if you only use default filters

---

## 🔒 Security & Privacy

✅ **Safe**:
- All code is open source
- No data leaves your device (except Etherscan balance checks)
- Keys are generated locally
- No analytics or tracking

⚠️ **Important**:
- Never share private keys that control funds
- Review custom filters before loading
- This is for educational/research purposes

---

## 🐛 Troubleshooting

### App won't install
- Enable "Unknown sources" in Settings → Security
- Make sure APK is for Android 5.0+ (API 21+)
- Try uninstalling old version first

### App crashes
- Grant all requested permissions
- Check Android version (need 5.0+)
- Clear app data and restart

### File chooser not working
- Grant storage permission
- Place files in Downloads folder
- On Android 11+, use the picker interface

### Balance checking fails
- Check internet connection
- Verify API key (if using one)
- Etherscan may be rate-limiting

### Can't load custom filters
- Ensure file is a `.py` Python file
- Check file contains PatternFilter classes
- File must be accessible in phone storage

---

## 📁 App Storage

### Where things are stored:
- **Filters**: In app memory (while running)
- **Keys**: Not stored permanently (shown in results only)
- **Settings**: Saved between sessions

### To save results:
- Copy from results text area
- Screenshot the results
- Export feature (coming in future update)

---

## 🆘 Need Help?

### Build Issues
1. Check BUILD_ANDROID.md for detailed troubleshooting
2. Use GitHub Actions (easiest, no setup needed)
3. Try Google Colab method

### App Issues
1. Check permissions are granted
2. Try reinstalling
3. Use a smaller batch size
4. Disable balance checking if having network issues

### Questions?
- Check README.md for general info
- Review eth_key_scanner.py for filter examples
- Open an issue on GitHub

---

## 🎉 You're Ready!

1. Build the APK using Method 1 (GitHub Actions)
2. Install on your Android 14 device
3. Start generating keys
4. Load custom filters as needed

**Happy scanning!** 🔑🔍
