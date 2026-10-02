# App Inspiration

Static site for browsing design references for apps. The home page (`index.html`) links to each section.

## Sections

- **App icons** (`icons/`): about 14,700 icons from community GitHub icon packs and real App Store apps. Images are loaded from their original hosts, so nothing is stored here except names and URLs (`icons/data/gallery.json`). For inspiration only.
- Screenshots, Onboarding, Paywalls: planned.

## Run locally

    python3 -m http.server 8765 --bind 127.0.0.1

Then open http://127.0.0.1:8765/.

## Rebuild the icon data

    cd icons/scripts
    mkdir -p _raw
    python3 fetch.py   # App Store icons via the iTunes Search API
    python3 repos.py   # list image files in the GitHub icon-pack repos (needs `gh auth login`)
    python3 build.py   # writes ../data/gallery.json

## Rebuild the characters & items data

    cd characters/scripts
    mkdir -p _raw
    python3 repos.py       # list image files in candidate GitHub repos (needs `gh auth login`)
    python3 fetch_apps.py  # App Store apps with characters, via the iTunes Search API
    python3 build.py       # writes ../data/gallery.json

Sources: game-icons.net, Fluent emoji (3D and flat), OpenMoji, Noto emoji, Pokesprite, PokeAPI official artwork, Minecraft items, DiceBear avatars. Check each repo's license before shipping anything in an app.
