
# 🎼 FloorDD: GPU-Accelerated Natural Minor MIDI Generator

This project uses PyTorch (Metal backend) and MIDIUtil to generate **64-bar natural minor triad progressions** as `.mid` files. Each file is harmonically and rhythmically aligned, labeled with its **key**, **tempo**, and **chord progression**.

---

## 📦 Features

- ✅ 64 bars of whole-note triads per file
- 🎶 Chord progressions based on natural minor scale (diatonic triads)
- 🔁 Randomized root keys and progression patterns
- 🧠 Torch accelerated logic via Metal Performance Shaders (MPS)
- 🎼 Auto-labeled `.mid` files with key, tempo, and progression
- 🚀 Parallel processing using `ProcessPoolExecutor`

---

## 🧰 Requirements

- macOS with Metal support
- Python 3.9+
- Xcode Command Line Tools (for Metal backend)
- PyTorch with MPS (Metal) backend
- MIDIUtil

### Install dependencies:
```bash
pip install torch midiutil tqdm
