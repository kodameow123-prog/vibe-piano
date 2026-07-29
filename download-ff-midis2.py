#!/usr/bin/env python3
"""
Download Final Fantasy piano MIDI files from BitMidi
"""
import os
import sys
import time
import urllib.request
from pathlib import Path

OUTPUT_DIR = Path("/Users/kodameow/vibe-piano/public/midi")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# BitMidi direct download URLs (from web_extract)
FF_MIDI_FILES = [
    ("ff7-aerith-theme.mid", "https://bitmidi.com/uploads/46467.mid"),
    ("ff7-main-theme.mid", "https://bitmidi.com/uploads/46440.mid"),
    ("ff7-tifa-theme.mid", "https://bitmidi.com/uploads/46469.mid"),  # From related
    ("ff7-one-winged-angel.mid", "https://bitmidi.com/uploads/46450.mid"),
    ("ff10-to-zanarkand.mid", "https://bitmidi.com/uploads/46502.mid"),
    ("ff10-suteki-da-ne.mid", "https://bitmidi.com/uploads/46500.mid"),
    ("ff15-somnus.mid", "https://bitmidi.com/uploads/46518.mid"),
    ("ff-prelude.mid", "https://bitmidi.com/uploads/46309.mid"),
    ("ff9-melodies-of-life.mid", "https://bitmidi.com/uploads/46381.mid"),
    ("aerith.mid", "https://bitmidi.com/uploads/46465.mid"),  # From aerith.mid page
]

# Need to find the terra and aria themes
# Let's search for them

def download_file(url, filepath, max_retries=3):
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=15) as response:
                data = response.read()
                if len(data) > 1000 and (data[:4] in [b'MThd', b'RIFF']):
                    with open(filepath, 'wb') as f:
                        f.write(data)
                    return True, len(data)
                else:
                    return False, f"Invalid MIDI ({len(data)} bytes)"
        except Exception as e:
            if attempt == max_retries - 1:
                return False, str(e)
            time.sleep(1)
    return False, "Max retries"

def main():
    print(f"Downloading {len(FF_MIDI_FILES)} Final Fantasy MIDI files...")
    success = 0
    failed = []
    
    for filename, url in FF_MIDI_FILES:
        filepath = OUTPUT_DIR / filename
        if filepath.exists():
            print(f"✓ {filename} (already exists, {filepath.stat().st_size:,} bytes)")
            success += 1
            continue
        
        print(f"⬇ {filename} ... ", end="", flush=True)
        ok, result = download_file(url, filepath)
        if ok:
            print(f"OK ({result:,} bytes)")
            success += 1
        else:
            print(f"FAILED - {result}")
            failed.append((filename, result))
            if filepath.exists():
                filepath.unlink()
        time.sleep(0.5)
    
    # Also check for terra and aria
    print(f"\nDone: {success} downloaded, {len(failed)} failed")
    for f in sorted(OUTPUT_DIR.glob("*.mid")):
        print(f"  {f.name} ({f.stat().st_size:,} bytes)")

if __name__ == "__main__":
    main()