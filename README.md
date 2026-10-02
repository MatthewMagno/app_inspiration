# App Inspiration

Static site for browsing design references for apps. The home page (`index.html`) links to each section.

## Sections

- **App icons** (`icons/`): about 14,700 icons from community GitHub icon packs and real App Store apps. Images are loaded from their original hosts, so nothing is stored here except names and URLs (`icons/data/gallery.json`). For inspiration only.
- **Characters & items** (`characters/`): about 39,000 character, avatar, emoji and game-item icons from 40 packs in public GitHub repos (Kenney/OpenGameArt via Tiddybub/2d-assets, game-icons.net, Pokémon sprites, Minecraft, OSRS, Noto/Twemoji/OpenMoji/Fluent/Blobmoji/Firefox emoji, and more), plus 28 live DiceBear avatar styles. Filter by kind, art style, pack and category; shuffle/mix packs; pick favorites. Images are hot-linked from raw.githubusercontent.com (nothing stored except names and paths in `characters/data/gallery.json`). Several packs are copyrighted game art: inspiration only; each pack's license is shown in the viewer.
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

## Rebuild the character/item data

    cd characters/scripts
    python3 build.py   # blobless git clones into _raw/ (tree listing only), writes ../data/gallery.json

Add a pack by adding an `add(...)` call in `build.py`.
