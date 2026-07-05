# FluxTV Android TV — Build & Install Guide

## What this APK does

Appears on your Android TV home screen as "FluxTV". When you press OK/Select on
the remote it opens fluxtv.cc directly in Chrome (the full desktop-class browser
already on your TV). Video plays natively, D-pad navigation works, no CORS issues,
no WebView limitations. Your friend installs the same APK and gets the same thing.

---

## Option A — Build it yourself (needs a PC/Mac)

### Prerequisites
- **Java JDK 17+** — https://adoptium.net (download Temurin 17 LTS)
- **Android SDK** — install Android Studio from https://developer.android.com/studio
  - In Android Studio → SDK Manager → install **Android 14 (API 34)**
  - Note your SDK path (shown in SDK Manager, usually `~/Android/Sdk`)

### Build steps

```bash
# 1. Open a terminal in this folder
cd fluxtv-launcher

# Mac/Linux — run directly:
./gradlew assembleRelease

# Windows — use the batch file:
gradlew.bat assembleRelease
```

The first run downloads Gradle (~130 MB) and the Android build tools automatically.

**Your APK will be at:**
```
app/build/outputs/apk/release/FluxTV-AndroidTV-release.apk
```

If you get an `ANDROID_HOME` error, set it first:
```bash
# Mac/Linux (add to ~/.zshrc or ~/.bashrc):
export ANDROID_HOME=~/Android/Sdk
export PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools

# Windows (in System → Environment Variables):
ANDROID_HOME = C:\Users\YourName\AppData\Local\Android\Sdk
```

---

## Option B — Install from Android Studio (easiest for testing)

1. Open Android Studio → **Open Project** → select the `fluxtv-launcher` folder
2. Plug in your Android TV box via USB (or connect via ADB over Wi-Fi — see below)
3. Press the **▶ Run** button — it builds and installs in one step

---

## Installing the APK on your TV

### Method 1 — ADB over Wi-Fi (recommended, no cables)

On your Android TV, enable ADB:
- Settings → Device Preferences → About → Build (click 7 times for Developer Options)
- Developer Options → enable **Network debugging** (or USB debugging)
- Note the IP address shown (or check Settings → Network)

On your computer:
```bash
adb connect 192.168.1.XXX:5555       # replace with your TV's IP
adb install app/build/outputs/apk/release/FluxTV-AndroidTV-release.apk
```

Done. FluxTV appears on the TV home screen immediately.

### Method 2 — USB stick (no computer needed for your friend's TV)

1. Copy `FluxTV-AndroidTV-release.apk` to a USB stick
2. Plug into Android TV box
3. Install a file manager from the Play Store (e.g. **FX File Explorer** or **X-plore**)
4. Browse to the USB stick → tap the APK → tap Install

### Method 3 — Send via Google Drive / file share

1. Upload the APK to Google Drive / Dropbox / any file host
2. On the TV, open Chrome → download the APK
3. Open the downloaded APK from the notification bar or Downloads

---

## Enabling Unknown Sources (required for sideloading)

If you get "Install blocked":
- **Android TV (stock):** Settings → Device Preferences → Security → Unknown sources → ON
- **Fire TV:** Settings → My Fire TV → Developer Options → Apps from Unknown Sources → ON
- **Nvidia Shield:** Settings → Device Preferences → Security & Restrictions → Unknown sources
- **Mi Box:** Settings → More Settings → Security → Unknown sources → ON

---

## How it works on your friend's TV

Same 3 steps:
1. Send them the APK file (Google Drive, WhatsApp, USB stick)
2. They enable Unknown Sources
3. They install via a file manager

The app will show up on their Android TV home screen with the FluxTV banner.
When they launch it, it opens fluxtv.cc in their TV's Chrome browser — full video,
full D-pad navigation, everything works because it's just the real browser.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "App not installed" | Enable Unknown Sources (see above) |
| Opens then instantly closes | Chrome isn't installed — install from Play Store |
| No Chrome on TV | The app falls back to the system browser automatically |
| App not on home screen | Reboot the TV after install |
| `ANDROID_HOME not set` | Set the env variable pointing to your Android SDK folder |
| Gradle download fails | Check your internet connection; Gradle downloads on first run |

---

## Notes

- The APK is ~2 MB (tiny — it contains no media, just a launcher)
- Works on: Android TV, Google TV, Nvidia Shield, Mi Box, Chromecast with TV,
  Amazon Fire TV (with sideloading), most Chinese Android TV boxes
- Does NOT work on: Apple TV, Roku, Samsung Tizen, LG webOS
  (those need a different app entirely)
