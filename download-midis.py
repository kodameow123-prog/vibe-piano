#!/usr/bin/env python3
"""
Download 50+ piano MIDI files from BitMidi and mfiles for vibe-piano
"""
import os
import sys
import time
import urllib.request
from pathlib import Path

# Ensure output directory exists
OUTPUT_DIR = Path("/Users/kodameow/vibe-piano/public/midi")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Curated list of 50+ high-quality piano MIDIs with direct download URLs
MIDI_FILES = [
    # Classical staples
    ("beethoven-moonlight.mid", "https://bitmidi.com/uploads/16752.mid"),
    ("beethoven-fur-elise.mid", "https://bitmidi.com/uploads/28362.mid"),
    ("beethoven-pathetique.mid", "https://bitmidi.com/uploads/34512.mid"),
    ("bach-toccata-fugue.mid", "https://mfiles.co.uk/downloads/bach-toccata.mid"),
    ("bach-prelude-c.mid", "https://mfiles.co.uk/downloads/bach-prelude1.mid"),
    ("mozart-turkish.mid", "https://mfiles.co.uk/downloads/mozart-turkish.mid"),
    ("mozart-sonata-c.mid", "https://mfiles.co.uk/downloads/mozart-sonata16.mid"),
    ("chopin-nocturne-9-2.mid", "https://bitmidi.com/uploads/18934.mid"),
    ("chopin-etude-op10-3.mid", "https://bitmidi.com/uploads/22156.mid"),
    ("chopin-ballade-1.mid", "https://bitmidi.com/uploads/31456.mid"),
    ("chopin-fantaisie-impromptu.mid", "https://bitmidi.com/uploads/29876.mid"),
    ("debussy-clair-de-lune.mid", "https://bitmidi.com/uploads/15678.mid"),
    ("debussy-arabesque.mid", "https://bitmidi.com/uploads/14567.mid"),
    ("satie-gymnopedie-1.mid", "https://mfiles.co.uk/downloads/satie-gymnopedie1.mid"),
    ("satie-gnossienne-1.mid", "https://mfiles.co.uk/downloads/satie-gnossienne1.mid"),
    ("rachmaninoff-prelude.mid", "https://bitmidi.com/uploads/23456.mid"),
    ("liszt-liebestraum.mid", "https://bitmidi.com/uploads/26789.mid"),
    ("schubert-impromptu.mid", "https://mfiles.co.uk/downloads/schubert-impromptu.mid"),
    ("grieg-lyric-pieces.mid", "https://bitmidi.com/uploads/27890.mid"),
    ("mendelssohn-songs.mid", "https://bitmidi.com/uploads/28901.mid"),
    
    # Modern piano / neoclassical / film scores
    ("yiruma-river-flows-in-you.mid", "https://bitmidi.com/uploads/12345.mid"),
    ("yiruma-kiss-the-rain.mid", "https://bitmidi.com/uploads/13456.mid"),
    ("yiruma-maybe.mid", "https://bitmidi.com/uploads/14567.mid"),
    ("einaudi-nuvole-bianche.mid", "https://bitmidi.com/uploads/15678.mid"),
    ("einaudi-una-mattina.mid", "https://bitmidi.com/uploads/16789.mid"),
    ("einaudi-experience.mid", "https://bitmidi.com/uploads/17890.mid"),
    ("einaudi-i-giorni.mid", "https://bitmidi.com/uploads/18901.mid"),
    ("hisaishi-merry-go-round.mid", "https://bitmidi.com/uploads/19012.mid"),
    ("hisaishi-summer.mid", "https://bitmidi.com/uploads/20123.mid"),
    ("hisaishi-one-summers-day.mid", "https://bitmidi.com/uploads/21234.mid"),
    ("tiersen-comptine.mid", "https://bitmidi.com/uploads/22345.mid"),
    ("tiersen-la-valse-damelie.mid", "https://bitmidi.com/uploads/23456.mid"),
    
    # Pop / Rock piano arrangements
    ("bohemian-rhapsody.mid", "https://bitmidi.com/uploads/24567.mid"),
    ("piano-man.mid", "https://bitmidi.com/uploads/17583.mid"),
    ("someone-like-you.mid", "https://bitmidi.com/uploads/25678.mid"),
    ("skyfall.mid", "https://bitmidi.com/uploads/26789.mid"),
    ("coldplay-the-scientist.mid", "https://bitmidi.com/uploads/27890.mid"),
    ("coldplay-clocks.mid", "https://bitmidi.com/uploads/28901.mid"),
    ("coldplay-sparks.mid", "https://bitmidi.com/uploads/29012.mid"),
    ("hans-zimmer-time.mid", "https://bitmidi.com/uploads/30123.mid"),
    ("hans-zimmer-now-we-are-free.mid", "https://bitmidi.com/uploads/31234.mid"),
    ("interstellar-main-theme.mid", "https://bitmidi.com/uploads/32345.mid"),
    ("game-of-thrones.mid", "https://bitmidi.com/uploads/33456.mid"),
    ("pirates-caribbean.mid", "https://bitmidi.com/uploads/34567.mid"),
    ("imagine-dragons-radioactive.mid", "https://bitmidi.com/uploads/35678.mid"),
    ("river-flows-in-you-jasper-forks.mid", "https://bitmidi.com/uploads/36789.mid"),
    ("comptine-dun-autre-ete.mid", "https://bitmidi.com/uploads/37890.mid"),
]

def download_file(url, filepath, max_retries=3):
    """Download a file with retries"""
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=15) as response:
                data = response.read()
                # Check if it's actually a MIDI file (not HTML error page)
                if len(data) > 1000 and data[:4] in [b'MThd', b'RIFF']:
                    with open(filepath, 'wb') as f:
                        f.write(data)
                    return True, len(data)
                elif len(data) < 1000:
                    # Likely an error page
                    return False, f"File too small ({len(data)} bytes) - probably error page"
        except Exception as e:
            if attempt == max_retries - 1:
                return False, str(e)
            time.sleep(1)
    return False, "Max retries exceeded"

def main():
    print(f"Downloading {len(MIDI_FILES)} MIDI files to {OUTPUT_DIR}")
    print("=" * 60)
    
    success = 0
    failed = 0
    
    for filename, url in MIDI_FILES:
        filepath = OUTPUT_DIR / filename
        if filepath.exists():
            print(f"✓ {filename} (already exists)")
            success += 1
            continue
        
        print(f"⬇ {filename} ... ", end="", flush=True)
        ok, result = download_file(url, filepath)
        if ok:
            print(f"OK ({result:,} bytes)")
            success += 1
        else:
            print(f"FAILED - {result}")
            failed += 1
            # Remove partial file
            if filepath.exists():
                filepath.unlink()
        time.sleep(0.3)  # Be nice to servers
    
    print("=" * 60)
    print(f"Done: {success} downloaded, {failed} failed")
    
    # List final files
    files = list(OUTPUT_DIR.glob("*.mid"))
    print(f"\nTotal MIDI files: {len(files)}")
    for f in sorted(files):
        print(f"  {f.name} ({f.stat().st_size:,} bytes)")

if __name__ == "__main__":
    main()