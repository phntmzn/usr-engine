import os
import random
import torch
if torch.backends.mps.is_available():
    torch.set_default_device("mps")
    torch.set_default_dtype(torch.float32)
print("✅ Using Metal GPU (MPS)" if torch.backends.mps.is_available() else "⚠️ MPS not available")
from pathlib import Path
from tempfile import NamedTemporaryFile
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count

from tqdm import tqdm
from midiutil import MIDIFile

from b import notes, chords, time_value_durations

# === CONFIGURATION ===
TOTAL_FILES = 200
TEMPO = 157
OUTPUT_DIR = Path.home() / "Desktop" / "FLOORDD"
POOL_SIZE = max(4, cpu_count())

# === CONSTANTS ===
BEATS_PER_MINUTE = TEMPO
BEATS_PER_BAR = 4
BARS = 64
TOTAL_BEATS = BEATS_PER_BAR * BARS

class NaturalMinorScale:
    def __init__(self, root_index: int):
        chromatic_scale = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        note_to_semitone = {note: i for i, note in enumerate(chromatic_scale)}
        semitone_to_note = {i: note for i, note in enumerate(chromatic_scale)}
        minor_intervals = [0, 2, 3, 5, 7, 8, 10]
        self.chord_types = ["Minor", "Diminished", "Major", "Minor", "Minor", "Major", "Major"]
        root_note = chromatic_scale[root_index]
        root_semitone = note_to_semitone[root_note]
        self.scale = [semitone_to_note[(root_semitone + i) % 12] for i in minor_intervals]

def chord_pattern(index: int) -> Path:
    chromatic_scale = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    note_to_semitone = {note: i for i, note in enumerate(chromatic_scale)}
    semitone_to_note = {i: note for i, note in enumerate(chromatic_scale)}

    root_indices = torch.randint(0, len(chromatic_scale), (TOTAL_FILES,))
    root_index = root_indices[index].item()
    locrian_scale_obj = NaturalMinorScale(root_index)
    locrian_scale = locrian_scale_obj.scale
    locrian_chord_types = locrian_scale_obj.chord_types

    root_note = locrian_scale[0]
    print(f"🎼 Key: {root_note} Natural Minor")
    metal_locrian_progressions = [
        [0, 6, 5, 4], [0, 3, 1, 4], [0, 6, 0], [0, 1, 3, 5]
    ]
    idx = torch.randint(0, len(metal_locrian_progressions), (1,)).item()
    progression_degrees = metal_locrian_progressions[idx]
    print(f"📈 Progression (degrees): {progression_degrees}")
    chord_names = [f"{locrian_scale[d]} {locrian_chord_types[d]}" for d in progression_degrees]
    print(f"🎵 Chord Progression: {', '.join(chord_names)}")

    duration = time_value_durations["whole_note"]
    steps_per_bar = 1
    total_steps = BARS * steps_per_bar

    step_tensor = torch.arange(total_steps)
    bar_index_tensor = step_tensor // steps_per_bar
    prog_idx_tensor = bar_index_tensor % len(progression_degrees)
    scale_degrees = torch.tensor([progression_degrees[i] for i in prog_idx_tensor.tolist()])

    midi = MIDIFile(1)
    midi.addTempo(0, 0, TEMPO)

    midi.addText(0, 0, f"Key: {root_note} Natural Minor")
    midi.addText(0, 1, f"Progression (degrees): {progression_degrees}")
    midi.addText(0, 2, f"Chord Progression: {', '.join(chord_names)}")

    for step, scale_degree in enumerate(scale_degrees.tolist()):
        time = round(step * duration, 3)
        root_scale_note = locrian_scale[scale_degree]
        chord_type = locrian_chord_types[scale_degree]
        intervals = chords[chord_type]
        root_note_number = notes[root_scale_note]
        for interval in intervals:
            note = root_note_number + interval + 3  # octave up
            midi.addNote(0, 0, note, time, duration, 100)

    # Create descriptive filename
    chord_symbols = "-".join(name.replace(" ", "") for name in chord_names)
    key_signature = f"{root_note}m"
    midi_filename = f"Chords_{chord_symbols}_{TEMPO}bpm_{key_signature}.mid"
    midi_path = OUTPUT_DIR / midi_filename
    with open(midi_path, "wb") as f:
        midi.writeFile(f)

    return midi_path

def render_one(index: int):
    try:
        path = chord_pattern(index)
        print(f"🎼 Saved: {path.name}")
    except Exception as e:
        print(f"❌ Error generating {index:05}: {e}")

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"🎹 Generating {TOTAL_FILES} MIDI files...")
    with ProcessPoolExecutor(max_workers=POOL_SIZE) as executor:
        futures = [executor.submit(render_one, i) for i in range(TOTAL_FILES)]
        for f in tqdm(as_completed(futures), total=TOTAL_FILES):
            try:
                f.result()
            except Exception as e:
                print(f"❌ Task failed: {e}")

if __name__ == "__main__":
    main()
