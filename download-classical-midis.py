#!/usr/bin/env python3
"""
Download working classical MIDI from mfiles.co.uk + find HK MIDI
"""
import urllib.request
import time
from pathlib import Path

OUTPUT_DIR = Path("/Users/kodameow/vibe-piano/public/midi")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Reliable classical MIDI from mfiles.co.uk (we know these work)
CLASSICAL_MIDIS = {
    # Mozart
    "mozart-sonata-k331.mid": "https://www.mfiles.co.uk/downloads/mozart-sonata-k331-movement1.mid",
    "mozart-sonata-k545.mid": "https://www.mfiles.co.uk/downloads/sonata-in-c.mid",
    "mozart-rondo-k511.mid": "https://www.mfiles.co.uk/downloads/mozart-rondo-k511.mid",
    "mozart-alla-turca.mid": "https://www.mfiles.co.uk/downloads/alla-turca.mid",
    "mozart-piano-concerto-21.mid": "https://www.mfiles.co.uk/downloads/mozart-piano-concerto-21-2-elvira-madigan-piano-solo.mid",
    
    # Beethoven
    "beethoven-sonata-op13-pathetique.mid": "https://www.mfiles.co.uk/downloads/beethoven-piano-sonata-pathetique-2.mid",
    "beethoven-sonata-op27-moonlight.mid": "https://www.mfiles.co.uk/downloads/moonlight-movement1.mid",
    "beethoven-fur-elise.mid": "https://www.mfiles.co.uk/downloads/fur-elise.mid",
    "beethoven-minuet-g.mid": "https://www.mfiles.co.uk/downloads/beethoven-minuet-in-G.mid",
    "beethoven-ode-to-joy.mid": "https://www.mfiles.co.uk/downloads/beethoven-symphony9-4-ode-to-joy-piano-solo.mid",
    
    # Chopin
    "chopin-nocturne-op9-2.mid": "https://www.mfiles.co.uk/downloads/chopin-nocturne-op9-no2.mid",
    "chopin-etude-op10-3.mid": "https://www.mfiles.co.uk/downloads/chopin-etude-op10-no3.mid",
    "chopin-etude-op10-12.mid": "https://www.mfiles.co.uk/downloads/chopin-etude-op10-no12.mid",
    "chopin-prelude-op28-15.mid": "https://www.mfiles.co.uk/downloads/prelude15.mid",
    "chopin-waltz-op64-1.mid": "https://www.mfiles.co.uk/downloads/minute-waltz.mid",
    "chopin-waltz-op64-2.mid": "https://www.mfiles.co.uk/downloads/waltz-op64-no2.mid",
    "chopin-fantaisie-impromptu.mid": "https://www.mfiles.co.uk/downloads/chopin-fantaisie-impromptu.mid",
    
    # Debussy
    "debussy-clair-de-lune.mid": "https://www.mfiles.co.uk/downloads/debussy-clair-de-lune.mid",
    "debussy-arabesque-1.mid": "https://www.mfiles.co.uk/downloads/debussy-arabesque.mid",
    "debussy-reverie.mid": "https://www.mfiles.co.uk/downloads/debussy-reverie.mid",
    
    # Liszt
    "liszt-liebestraum-3.mid": "https://www.mfiles.co.uk/downloads/franz-liszt-liebestraum-3.mid",
    "liszt-hungarian-rhapsody-2.mid": "https://www.mfiles.co.uk/downloads/liszt-hungarian-rhapsody-2.mid",
    
    # Rachmaninoff
    "rachmaninoff-prelude-op3-2.mid": "https://www.mfiles.co.uk/downloads/rachmaninoff-prelude-op3-2.mid",
    
    # Schubert
    "schubert-impromptu-op90-3.mid": "https://www.mfiles.co.uk/downloads/Impromptu-set1-no3.mid",
    "schubert-impromptu-op90-4.mid": "https://www.mfiles.co.uk/downloads/Impromptu-set1-no4.mid",
    "schubert-moment-musical-3.mid": "https://www.mfiles.co.uk/downloads/Schubert-Moment-Musical-3.mid",
    "schubert-standchen.mid": "https://www.mfiles.co.uk/downloads/franz-schubert-standchen-serenade-piano-solo.mid",
    
    # Schumann
    "schumann-traumerei.mid": "https://www.mfiles.co.uk/downloads/schumann-traumerei.mid",
    "schumann-kinderszenen.mid": "https://www.mfiles.co.uk/downloads/schumann-kinderszenen.mid",
    
    # Brahms
    "brahms-intermezzo-op118-2.mid": "https://www.mfiles.co.uk/downloads/brahms-intermezzo-op118-no2.mid",
    "brahms-lullaby.mid": "https://www.mfiles.co.uk/downloads/brahms-lullaby-wiegenlied-piano.mid",
    
    # Grieg
    "grieg-lyric-pieces.mid": "https://www.mfiles.co.uk/downloads/grieg-lyric-pieces-op54.mid",
    
    # Bach
    "bach-prelude-c.mid": "https://www.mfiles.co.uk/downloads/bach-prelude1.mid",
    "bach-toccata-fugue.mid": "https://www.mfiles.co.uk/downloads/bach-toccata.mid",
    "bach-goldberg.mid": "https://www.mfiles.co.uk/downloads/bach-goldberg.mid",
    "bach-invention-1.mid": "https://www.mfiles.co.uk/downloads/bach-invention1.mid",
    
    # Scarlatti
    "scarlatti-sonata-k32.mid": "https://www.mfiles.co.uk/downloads/scarlatti-sonata-k32-d-minor.mid",
    "scarlatti-sonata-k159.mid": "https://www.mfiles.co.uk/downloads/scarlatti-sonata-k159-c-major.mid",
    
    # Haydn
    "haydn-sonata-hob50.mid": "https://www.mfiles.co.uk/downloads/haydn-sonata-hob50.mid",
    
    # Mendelssohn
    "mendelssohn-songs-without-words.mid": "https://www.mfiles.co.uk/downloads/mendelssohn-songs.mid",
    
    # Satie
    "satie-gymnopedie-1.mid": "https://www.mfiles.co.uk/downloads/Gymnopedie1.mid",
    "satie-gymnopedie-2.mid": "https://www.mfiles.co.uk/downloads/Gymnopedie2.mid",
    "satie-gnossienne-1.mid": "https://www.mfiles.co.uk/downloads/Gnossienne1.mid",
    
    # Ravel
    "ravel-pavane.mid": "https://www.mfiles.co.uk/downloads/ravel-pavane.mid",
    
    # Prokofiev (if available)
    # Tchaikovsky
    "tchaikovsky-seasons.mid": "https://www.mfiles.co.uk/downloads/tchaikovsky-seasons.mid",
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
    print(f"Downloading {len(CLASSICAL_MIDIS)} classical MIDIs to {OUTPUT_DIR}")
    print("=" * 60)
    
    success = 0
    failed = []
    
    for filename, url in CLASSICAL_MIDIS.items():
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
            print(f"FAILED - {result}")
            failed.append((filename, result))
            if filepath.exists():
                filepath.unlink()
        time.sleep(0.3)
    
    print("=" * 60)
    print(f"Done: {success} downloaded, {len(failed)} failed")
    for f, r in failed:
        print(f"  ✗ {f}: {r}")

if __name__ == "__main__":
    main()