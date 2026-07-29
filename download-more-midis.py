#!/usr/bin/env python3
"""
Download more classical piano MIDI + Hong Kong/C-pop MIDI
"""
import os
import sys
import time
import urllib.request
from pathlib import Path

OUTPUT_DIR = Path("/Users/kodameow/vibe-piano/public/midi")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Classical piano MIDIs from reliable sources
CLASSICAL_MIDIS = {
    # From piano-midi.de (Bernd Krüger's excellent collection)
    "mozart-sonata-k331.mid": "http://www.piano-midi.de/mozart/mozart_sonata_k331_1.mid",
    "mozart-sonata-k545.mid": "http://www.piano-midi.de/mozart/mozart_sonata_k545_1.mid",
    "mozart-rondo-k511.mid": "http://www.piano-midi.de/mozart/mozart_rondo_k511.mid",
    "beethoven-sonata-op13-pathetique.mid": "http://www.piano-midi.de/beeth/beeth_pats_1.mid",
    "beethoven-sonata-op27-moonlight.mid": "http://www.piano-midi.de/beeth/beeth_moon_1.mid",
    "beethoven-sonata-op57-appassionata.mid": "http://www.piano-midi.de/beeth/beeth_app_1.mid",
    "beethoven-fur-elise.mid": "http://www.piano-midi.de/beeth/beeth_furelise.mid",
    "chopin-nocturne-op9-2.mid": "http://www.piano-midi.de/chopin/chop_noct_op9_2.mid",
    "chopin-nocturne-op27-2.mid": "http://www.piano-midi.de/chopin/chop_noct_op27_2.mid",
    "chopin-etude-op10-3.mid": "http://www.piano-midi.de/chopin/chop_et_op10_3.mid",
    "chopin-etude-op10-12.mid": "http://www.piano-midi.de/chopin/chop_et_op10_12.mid",
    "chopin-etude-op25-1.mid": "http://www.piano-midi.de/chopin/chop_et_op25_1.mid",
    "chopin-ballade-1.mid": "http://www.piano-midi.de/chopin/chop_bal_1.mid",
    "chopin-fantaisie-impromptu.mid": "http://www.piano-midi.de/chopin/chop_fant_imp.mid",
    "chopin-prelude-op28-15.mid": "http://www.piano-midi.de/chopin/chop_prel_op28_15.mid",
    "chopin-waltz-op64-1.mid": "http://www.piano-midi.de/chopin/chop_waltz_op64_1.mid",
    "chopin-waltz-op64-2.mid": "http://www.piano-midi.de/chopin/chop_waltz_op64_2.mid",
    "debussy-clair-de-lune.mid": "http://www.piano-midi.de/debuss/deb_clair_de_lune.mid",
    "debussy-arabesque-1.mid": "http://www.piano-midi.de/debuss/deb_arabesque_1.mid",
    "debussy-reverie.mid": "http://www.piano-midi.de/debuss/deb_reverie.mid",
    "liszt-liebestraum-3.mid": "http://www.piano-midi.de/liszt/liszt_lieb_3.mid",
    "liszt-hungarian-rhapsody-2.mid": "http://www.piano-midi.de/liszt/liszt_hung_2.mid",
    "rachmaninoff-prelude-op3-2.mid": "http://www.piano-midi.de/rach/rach_prel_op3_2.mid",
    "rachmaninoff-prelude-op23-5.mid": "http://www.piano-midi.de/rach/rach_prel_op23_5.mid",
    "schubert-impromptu-op90-3.mid": "http://www.piano-midi.de/schub/schub_imp_op90_3.mid",
    "schubert-impromptu-op90-4.mid": "http://www.piano-midi.de/schub/schub_imp_op90_4.mid",
    "schumann-kinderszenen.mid": "http://www.piano-midi.de/schum/schum_kinderszenen.mid",
    "schumann-träumerei.mid": "http://www.piano-midi.de/schum/schum_traumerei.mid",
    "brahms-intermezzo-op118-2.mid": "http://www.piano-midi.de/brahms/brahms_intermezzo_op118_2.mid",
    "grieg-lyric-pieces-op54.mid": "http://www.piano-midi.de/grieg/grieg_lyric_op54.mid",
    "bach-goldberg-variations.mid": "http://www.piano-midi.de/bach/bach_goldberg.mid",
    "bach-italian-concerto.mid": "http://www.piano-midi.de/bach/bach_italian_concerto.mid",
    "bach-well-tempered-clavier-prelude-1.mid": "http://www.piano-midi.de/bach/bach_wtc_1.mid",
    "scarlatti-sonata-k380.mid": "http://www.piano-midi.de/scar/scar_k380.mid",
    "scarlatti-sonata-k466.mid": "http://www.piano-midi.de/scar/scar_k466.mid",
    "haydn-sonata-hob-xvi-50.mid": "http://www.piano-midi.de/haydn/haydn_sonata_hob50.mid",
    "mendelssohn-songs-without-words.mid": "http://www.piano-midi.de/mendelssohn/mendelssohn_sww.mid",
    "satie-gymnopedie-1.mid": "http://www.piano-midi.de/satie/satie_gymno_1.mid",
    "satie-gymnopedie-2.mid": "http://www.piano-midi.de/satie/satie_gymno_2.mid",
    "satie-gymnopedie-3.mid": "http://www.piano-midi.de/satie/satie_gymno_3.mid",
    "satie-gnossienne-1.mid": "http://www.piano-midi.de/satie/satie_gnoss_1.mid",
    "ravel-pavane.mid": "http://www.piano-midi.de/ravel/ravel_pavane.mid",
    "prokofiev-sonata-7.mid": "http://www.piano-midi.de/prok/prok_sonata_7.mid",
    "tchaikovsky-seasons.mid": "http://www.piano-midi.de/tschai/tschai_seasons.mid",
}

# Hong Kong / Cantonese / C-Pop MIDI sources
HK_POP_MIDIS = {
    # From various C-pop MIDI collections
    "beyond-glory-days.mid": "https://www.midifind.com/files/b/beyond/beyond_glory_days.mid",
    "beyond-sea-of-sky.mid": "https://www.midifind.com/files/b/beyond/beyond_sea_of_sky.mid",
    "beyond-really-love-you.mid": "https://www.midifind.com/files/b/beyond/beyond_really_love_you.mid",
    "leslie-cheung-miss-you.mid": "https://www.midifind.com/files/l/leslie_cheung/leslie_miss_you.mid",
    "leslie-cheung-monica.mid": "https://www.midifind.com/files/l/leslie_cheung/leslie_monica.mid",
    "anita-mui-bad-girl.mid": "https://www.midifind.com/files/a/anita_mui/anita_bad_girl.mid",
    "anita-mui-seems-like-old-friend.mid": "https://www.midifind.com/files/a/anita_mui/anita_seems_like_old_friend.mid",
    "jacky-cheung-kiss-goodbye.mid": "https://www.midifind.com/files/j/jacky_cheung/jacky_kiss_goodbye.mid",
    "jacky-cheung-love-you-million-years.mid": "https://www.midifind.com/files/j/jacky_cheung/jacky_love_million_years.mid",
    "andy-lau-forget-love.mid": "https://www.midifind.com/files/a/andy_lau/andy_forget_love.mid",
    "andy-lau-chinese.mid": "https://www.midifind.com/files/a/andy_lau/andy_chinese.mid",
    "faye-wong-red-bean.mid": "https://www.midifind.com/files/f/faye_wong/faye_red_bean.mid",
    "faye-wong-dream-lover.mid": "https://www.midifind.com/files/f/faye_wong/faye_dream_lover.mid",
    "eason-chan-ten-years.mid": "https://www.midifind.com/files/e/eason_chan/eason_ten_years.mid",
    "eason-chan-king-of-karaoke.mid": "https://www.midifind.com/files/e/eason_chan/eason_king_karaoke.mid",
    "jay-chou-cannot-say.mid": "https://www.midifind.com/files/j/jay_chou/jay_cannot_say.mid",
    "jay-chou-simple-love.mid": "https://www.midifind.com/files/j/jay_chou/jay_simple_love.mid",
    "jay-chou-chrysanthemum.mid": "https://www.midifind.com/files/j/jay_chou/jay_chrysanthemum.mid",
    "jay-chou-blue-and-white.mid": "https://www.midifind.com/files/j/jay_chou/jay_blue_white.mid",
    "gem-bubble.mid": "https://www.midifind.com/files/g/gem/gem_bubble.mid",
    "gem-light-years-away.mid": "https://www.midifind.com/files/g/gem/gem_light_years.mid",
    "khalil-fong-soul-boy.mid": "https://www.midifind.com/files/k/khalil_fong/khalil_soul_boy.mid",
    "khalil-fong-love-song.mid": "https://www.midifind.com/files/k/khalil_fong/khalil_love_song.mid",
    "khalil-fong-rocket.mid": "https://www.midifind.com/files/k/khalil_fong/khalil_rocket.mid",
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
    print(f"Downloading to {OUTPUT_DIR}")
    print("=" * 60)
    
    all_midis = {**CLASSICAL_MIDIS, **HK_POP_MIDIS}
    print(f"Total: {len(all_midis)} MIDIs ({len(CLASSICAL_MIDIS)} classical + {len(HK_POP_MIDIS)} HK/C-pop)")
    
    success = 0
    failed = []
    
    for filename, url in all_midis.items():
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