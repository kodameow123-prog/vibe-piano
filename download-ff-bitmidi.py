#!/usr/bin/env python3
"""
Download Final Fantasy MIDI files from BitMidi
"""
import urllib.request
import time
from pathlib import Path

OUTPUT_DIR = Path("/Users/kodameow/vibe-piano/midi")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Direct BitMidi upload URLs (these are the actual file URLs from bitmidi.com)
FF_MIDIS = {
    "ff6-terra-theme.mid": "https://bitmidi.com/uploads/ff6-terra.mid",
    "ff6-arias-theme.mid": "https://bitmidi.com/uploads/ff6-aria.mid",
    "ff7-aerith-theme.mid": "https://bitmidi.com/uploads/ff7-aerith.mid",
    "ff7-main-theme.mid": "https://bitmidi.com/uploads/ff7-main.mid",
    "ff7-one-winged-angel.mid": "https://bitmidi.com/uploads/ff7-one-winged.mid",
    "ff8-eyes-on-me.mid": "https://bitmidi.com/uploads/ff8-eyes.mid",
    "ff9-melodies-of-life.mid": "https://bitmidi.com/uploads/ff9-melodies.mid",
    "ff10-suteki-da-ne.mid": "https://bitmidi.com/uploads/ff10-suteki.mid",
    "ff10-to-zanarkand.mid": "https://bitmidi.com/uploads/ff10-zanarkand.mid",
    "ff12-kiss-me-good-bye.mid": "https://bitmidi.com/uploads/ff12-kiss.mid",
    "ff13-promise.mid": "https://bitmidi.com/uploads/ff13-promise.mid",
    "ff15-somnus.mid": "https://bitmidi.com/uploads/ff15-somnus.mid",
    "ff15-omnis-lacrima.mid": "https://bitmidi.com/uploads/ff15-omnis.mid",
}

def download_file(url, filepath, max_retries=2):
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=20) as response:
                data = response.read()
                if len(data) > 1000 and data[:4] in [b'MThd', b'RIFF']:
                    with open(filepath, 'wb') as f:
                        f.write(data)
                    return True, len(data)
                return False, f"Invalid MIDI ({len(data)} bytes)"
        except Exception as e:
            if attempt == max_retries - 1:
                return False, str(e)
            time.sleep(1)
    return False, "Max retries"

def main():
    print(f"Downloading {len(FF_MIDIS)} Final Fantasy MIDIs...")
    print("=" * 60)
    
    success = 0
    failed = 0
    
    for filename, url in FF_MIDIS.items():
        filepath = OUTPUT_DIR / filename
        if filepath.exists():
            print(f"✓ {filename} (exists)")
            success += 1
            continue
        
        print(f"⬇ {filename} ... ", end="", flush=True)
        ok, result = download_file(url, filepath)
        if ok:
            print(f"OK ({result:,} bytes)")
            success += 1
        else:
            print(f"Failed - {result}")
            failed += 1
            if filepath.exists():
                filepath.unlink()
        time.sleep(0.5)
    
    print("=" * 60)
    print(f"Done: {success} successful, {failed} failed")
    for f in sorted(OUTPUT_DIR.glob("ff*.mid")):
        print(f"  {f.name} ({f.stat().st_size:,} bytes)")

if __name__ == "__main__":
    main()