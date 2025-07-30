# 🎼 floordd — Natural Minor MIDI Engine with LaunchAgent Support

**floordd** is a high-performance, Metal-accelerated MIDI engine that generates harmonically rich, quantized chord progressions using natural minor triads. It runs via command-line or background service using `launchd`, and produces 64-bar `.mid` files labeled with key and chord structure.

---

## ⚡ Features

- 🎼 Writes **64-bar natural minor triads** as whole notes
- 📝 MIDI files are labeled by **key**, **tempo**, and **progression**
- ⚙️ Supports **LaunchAgent** and `.pkg` installation via `postinstall`

---

## 🧰 Requirements

- macOS with **Metal support**
- Python 3.9+
- Metal toolchain (`xcrun`, `metal`, `metallib`) available via Xcode Command Line Tools
- PyTorch with MPS (Metal Performance Shaders) backend
- macOS LaunchAgents or LaunchDaemons for background execution
- Optional: `clang` and `pkgbuild` for `.dylib` and installer generation

### Python dependencies:

```bash
pip install torch midiutil tqdm
```
