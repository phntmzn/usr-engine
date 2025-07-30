import os
import random
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
OUTPUT_DIR = Path.home() / "Desktop" / "ascii_music_midi"
POOL_SIZE = max(4, cpu_count())

# === CONSTANTS ===
BEATS_PER_MINUTE = TEMPO
DURATION_MINUTES = 2
TOTAL_BEATS = BEATS_PER_MINUTE * DURATION_MINUTES
BEATS_PER_BAR = 4
BARS = TOTAL_BEATS // BEATS_PER_BAR

def chord_pattern(index: int) -> Path:
    chromatic_scale = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    note_to_semitone = {note: i for i, note in enumerate(chromatic_scale)}
    semitone_to_note = {i: note for i, note in enumerate(chromatic_scale)}

    locrian_intervals = [0, 1, 3, 5, 6, 8, 10]
    locrian_chord_types = [
        "Diminished", "Minor", "Major", "Minor", "Major", "Major", "Minor"
    ]

    root_note = random.choice(chromatic_scale)
    root_semitone = note_to_semitone[root_note]
    locrian_scale = [semitone_to_note[(root_semitone + i) % 12] for i in locrian_intervals]

    metal_locrian_progressions = [
        [0, 6, 5, 4], [0, 3, 1, 4], [0, 6, 0], [0, 1, 3, 5]
    ]
    progression_degrees = random.choice(metal_locrian_progressions)

    duration = time_value_durations["eighth_note"]
    steps_per_bar = 4
    total_steps = BARS * steps_per_bar

    midi = MIDIFile(1)
    midi.addTempo(0, 0, TEMPO)

    for step in range(total_steps):
        time = step * duration
        bar_index = step // steps_per_bar
        prog_idx = bar_index % len(progression_degrees)
        scale_degree = progression_degrees[prog_idx]
        root_scale_note = locrian_scale[scale_degree]
        chord_type = locrian_chord_types[scale_degree]
        intervals = chords[chord_type]
        root_note_number = notes[root_scale_note]
        interval = intervals[step % len(intervals)]
        note = root_note_number + interval + 3  # octave up
        midi.addNote(0, 0, note, time, duration, 100)

    midi_path = OUTPUT_DIR / f"{index:05}.mid"
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