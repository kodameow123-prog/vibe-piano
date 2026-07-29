#!/usr/bin/env python3
"""
Download Final Fantasy MIDI files from various sources
"""
import os
import sys
import time
import urllib.request
from pathlib import Path

OUTPUT_DIR = Path("/Users/kodameow/vibe-piano/midi")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# FF MIDI URLs from various sources (we'll try multiple)
FF_MIDIS = {
    "ff6-terra-theme.mid": [
        "https://www.mfiles.co.uk/downloads/ff6-terra.mid",
        "https://bitmidi.com/uploads/terra-theme.mid",
    ],
    "ff6-arias-theme.mid": [
        "https://www.mfiles.co.uk/downloads/ff6-aria.mid",
    ],
    "ff7-aerith-theme.mid": [
        "https://www.mfiles.co.uk/downloads/ff7-aerith.mid",
        "https://bitmidi.com/uploads/aerith.mid",
    ],
    "ff7-main-theme.mid": [
        "https://www.mfiles.co.uk/downloads/ff7-main.mid",
    ],
    "ff7-one-winged-angel.mid": [
        "https://www.mfiles.co.uk/downloads/ff7-one-winged.mid",
    ],
    "ff8-eyes-on-me.mid": [
        "https://www.mfiles.co.uk/downloads/ff8-eyes.mid",
    ],
    "ff9-melodies-of-life.mid": [
        "https://www.mfiles.co.uk/downloads/ff9-melodies.mid",
    ],
    "ff10-suteki-da-ne.mid": [
        "https://www.mfiles.co.uk/downloads/ff10-suteki.mid",
    ],
    "ff10-to-zanarkand.mid": [
        "https://www.mfiles.co.uk/downloads/ff10-zanarkand.mid",
    ],
    "ff12-kiss-me-good-bye.mid": [
        "https://www.mfiles.co.uk/downloads/ff12-kiss.mid",
    ],
    "ff13-promise.mid": [
        "https://www.mfiles.co.uk/downloads/ff13-promise.mid",
    ],
    "ff15-somnus.mid": [
        "https://www.mfiles.co.uk/downloads/ff15-somnus.mid",
    ],
    "ff15-omnis-lacrima.mid": [
        "https://www.mfiles.co.uk/downloads/ff15-omnis.mid",
    ],
}

def download_file(url, filepath, max_retries=3):
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=15) as response:
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
    print(f"Downloading {len(FF_MIDIS)} Final Fantasy MIDIs to {OUTPUT_DIR}")
    print("=" * 60)
    
    success = 0
    failed = 0
    
    for filename, urls in FF_MIDIS.items():
        filepath = OUTPUT_DIR / filename
        if filepath.exists():
            print(f"✓ {filename} (exists)")
            success += 1
            continue
        
        downloaded = False
        for url in urls:
            print(f"⬇ {filename} from {url.split('/')[-2] if '/' in url else url[:40]}... ", end="", flush=True)
            ok, result = download_file(url, filepath)
            if ok:
                print(f"OK ({result:,} bytes)")
                success += 1
                downloaded = True
                break
            else:
                print(f"Failed - {result}")
        
        if not downloaded:
            failed += 1
            if filepath.exists():
                filepath.unlink()
        time.sleep(0.3)
    
    print("=" * 60)
    print(f"Done: {success} successful, {failed} failed")
    files = list(OUTPUT_DIR.glob("ff*.mid"))
    for f in sorted(files):
        print(f"  {f.name} ({f.stat().st_size:,} bytes)")

if __name__ == "__main__":
    main()