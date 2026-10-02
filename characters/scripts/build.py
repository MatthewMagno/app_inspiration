"""Build ../data/gallery.json: character + item icon packs hosted in public GitHub repos.

Needs only `git` (blobless shallow clones, tree listing only; no image is downloaded).
Images are hot-linked from raw.githubusercontent.com at view time.

    python3 build.py            # clones into ./_raw, writes ../data/gallery.json
"""
import json, os, random, re, subprocess, unicodedata, urllib.parse

random.seed(7)
RAW = os.path.join(os.path.dirname(__file__), "_raw")
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "gallery.json")
os.makedirs(RAW, exist_ok=True)

_trees = {}
def tree(repo):
    """-> (branch, [paths]) for a repo, via blobless depth-1 clone."""
    if repo in _trees: return _trees[repo]
    d = os.path.join(RAW, repo.replace("/", "_"))
    if not os.path.isdir(d):
        subprocess.run(["git", "clone", "-q", "--depth", "1", "--filter=blob:none", "--no-checkout",
                        f"https://github.com/{repo}", d], check=True, env={**os.environ, "GIT_LFS_SKIP_SMUDGE": "1"})
    br = subprocess.check_output(["git", "-C", d, "symbolic-ref", "--short", "HEAD"], text=True).strip()
    files = subprocess.check_output(["git", "-C", d, "ls-tree", "-r", "--name-only", "HEAD"], text=True).split("\n")
    _trees[repo] = (br, [f for f in files if f])
    return _trees[repo]

IMG = (".png", ".svg", ".webp", ".jpg", ".jpeg")
def clean(s): return re.sub(r"\s+", " ", re.sub(r"[_\-]+", " ", s)).strip()
def stem(p): return os.path.splitext(os.path.basename(p))[0]

sources = []
def add(repo, id, label, kind, style, note, license, pick, name=None, cat=None, cap=None, k=None, url=None):
    """pick(path)->bool selects files; name/cat/k are functions of the path."""
    br, files = tree(repo)
    sel = sorted(f for f in files if f.lower().endswith(IMG) and pick(f))
    if cap and len(sel) > cap: sel = sorted(random.sample(sel, cap))
    items = []
    for f in sel:
        it = [(name or (lambda p: clean(stem(p))))(f), f]
        c = cat(f) if cat else ""
        kk = k(f) if k else ""
        if c or kk: it.append(c)
        if kk: it.append(kk)
        items.append(it)
    if not items: print("EMPTY", id); return
    sources.append({"id": id, "label": label, "kind": kind, "style": style, "note": note, "license": license,
                    "url": url or f"https://github.com/{repo}",
                    "base": f"https://raw.githubusercontent.com/{repo}/{br}/", "items": items})
    print(f"{id:34s}{len(items):6d}")

def after(prefix):  # category = first folder after prefix
    return lambda p: p[len(prefix):].split("/")[0] if "/" in p[len(prefix):] else ""

# ------------------------------------------------------------------ CHARACTERS
add("alohe/avatars", "alohe-avatars", "Avatars (alohe)", "character", "mixed", "Diverse avatar illustrations: 3d, bluey, memo, notion, teams, toon, vibrent...", "free, see repo",
    lambda p: p.startswith("png/"), cat=lambda p: re.sub(r"_\d+$", "", stem(p)))

PK = "PokeAPI/sprites"
num = lambda p: "#" + stem(p)
add(PK, "pokeapi-artwork", "Pokémon official artwork", "character", "painted", "Official character art, 475px", "© Nintendo — inspiration only",
    lambda p: p.startswith("sprites/pokemon/other/official-artwork/") and p.count("/") == 4 and stem(p).isdigit(), name=num, cap=800)
add(PK, "pokeapi-home", "Pokémon HOME renders", "character", "3d", "3D-rendered characters", "© Nintendo — inspiration only",
    lambda p: p.startswith("sprites/pokemon/other/home/") and p.count("/") == 4 and stem(p).isdigit(), name=num, cap=800)
add(PK, "pokeapi-dream", "Pokémon dream world (SVG)", "character", "flat", "Flat vector characters", "© Nintendo — inspiration only",
    lambda p: p.startswith("sprites/pokemon/other/dream-world/") and p.count("/") == 4 and stem(p).isdigit(), name=num, cap=800)
add("msikma/pokesprite", "pokesprite-mons", "Pokémon box sprites", "character", "pixel", "Gen 8 pixel box sprites (named)", "MIT code; sprites © Nintendo",
    lambda p: p.startswith("pokemon-gen8/regular/"))
add("msikma/pokesprite", "pokesprite-items", "Pokémon item sprites", "item", "pixel", "Berries, balls, medicine, key items, gems...", "MIT code; sprites © Nintendo",
    lambda p: p.startswith("items/") and p.count("/") == 2, cat=after("items/"))
add(PK, "pokeapi-items", "Pokémon items (PokeAPI)", "item", "pixel", "Every item sprite from the games", "© Nintendo — inspiration only",
    lambda p: p.startswith("sprites/items/") and p.count("/") == 2)

T = "Tiddybub/2d-assets"  # CC0 mirror of Kenney + OpenGameArt packs
K = lambda s: s
add(T, "kenney-toon", "Toon characters (Kenney)", "character", "cartoon", "Zombie, robot, male/female person, adventurer — many poses", "CC0 · Kenney",
    lambda p: p.startswith("characters/toon-characters/") and "/PNG/Poses/" in p, cat=lambda p: p.split("/")[2])
add(T, "kenney-animals", "Animal pack (Kenney)", "character", "flat", "Round + square animal faces, no outlines", "CC0 · Kenney",
    lambda p: p.startswith("characters/animal-pack-remastered/PNG/") and p.split("/")[3] in ("Round", "Square", "Round without details", "Square without details"),
    cat=lambda p: p.split("/")[3])
add(T, "kenney-monsters", "Monster builder (Kenney)", "character", "flat", "Mix-and-match monster parts and full monsters", "CC0 · Kenney",
    lambda p: p.startswith("characters/monster-builder-pack/PNG/Default/"))
add(T, "kenney-fish", "Fish pack (Kenney)", "character", "flat", "Fish, bubbles and sea life", "CC0 · Kenney",
    lambda p: p.startswith("characters/fish-pack/PNG/Default/"))
add(T, "kenney-shapes", "Shape characters (Kenney)", "character", "flat", "Geometric blob characters with expressions", "CC0 · Kenney",
    lambda p: p.startswith("misc/shape-characters/PNG/Default/"))
add(T, "kenney-platformer", "Platformer characters (Kenney)", "character", "cartoon", "Adventurer, player, soldier, zombie, female poses", "CC0 · Kenney",
    lambda p: p.startswith("characters/platformer-characters/PNG/") and "/Poses/" in p, cat=lambda p: p.split("/")[3])
add(T, "kenney-newplat", "New platformer pack (Kenney)", "character", "cartoon", "Characters + enemies, flat style", "CC0 · Kenney",
    lambda p: re.match(r"characters/new-platformer-pack/Sprites/(Characters|Enemies)/Default/", p), cat=lambda p: p.split("/")[3])
add(T, "kenney-enemies", "Extended enemies (Kenney)", "character", "cartoon", "Enemy + alien sprites", "CC0 · Kenney",
    lambda p: p.startswith("characters/platformer-art-extended-enemies/") and ("Enemy sprites" in p or "Alien sprites" in p), cat=lambda p: p.split("/")[2])
add(T, "kenney-voxel-chars", "Voxel pack: characters + items", "both", "voxel", "Isometric voxel characters, items and tiles", "CC0 · Kenney",
    lambda p: p.startswith("characters/voxel-pack/PNG/") and p.split("/")[3] in ("Characters", "Items"), cat=lambda p: p.split("/")[3],
    k=lambda p: "c" if p.split("/")[3] == "Characters" else "i")

# ------------------------------------------------------------------ ITEMS
add("game-icons/icons", "game-icons", "game-icons.net", "item", "line", "Silhouette RPG icons: weapons, creatures, potions, skills (~4,200)", "CC BY 3.0 — credit authors",
    lambda p: p.endswith(".svg") and "/" in p and not p.startswith("."), cat=lambda p: p.split("/")[0])
add("designclarity/rpg-icon-mega-pack", "rpg-mega", "RPG icon mega-pack", "item", "pixel", "1,273 pixel RPG icons: weapons, armor, potions, treasure, magic", "CC0",
    lambda p: p.startswith("png64/"), cat=lambda p: p.split("/")[1])
add("Gwillewyn/dnd-item-icons-by-gwill", "dnd-gwill", "D&D item icons (Gwill)", "item", "line", "Magical items, gear, treasure, potions, scrolls", "see repo",
    lambda p: p.startswith("Library/"), cat=lambda p: p.split("/")[1])
add("Nieobie/Game-Icon-Pack", "nieobie", "Game icon pack (Nieobie)", "item", "flat", "800+ rounded-style game icons", "CC0",
    lambda p: p.startswith("svg/padding/"), cat=lambda p: re.sub(r"^\d+-", "", p.split("/")[2]))
add(T, "kenney-generic-items", "Generic items (Kenney)", "item", "flat", "Colored generic item icons", "CC0 · Kenney",
    lambda p: p.startswith("misc/generic-items/PNG/Colored/"))
add(T, "oga-magic-icons", "Magic skill + item icons (OGA)", "item", "painted", "582 painted skill/item icons", "CC0 · OpenGameArt",
    lambda p: p.startswith("ui/oga-modified-and-cliped-magic-skill-item-icons/64x64_unpacked/64x64/"))
add(T, "oga-skill-spell", "Skill, item + spell icons (OGA)", "item", "painted", "Painted spell/item icons", "CC0 · OpenGameArt",
    lambda p: p.startswith("ui/oga-skill-item-and-spell-icons/icons_unpacked/"))
add(T, "kenney-game-icons", "Game icons expansion (Kenney)", "item", "flat", "Colored + base UI/game icons", "CC0 · Kenney",
    lambda p: p.startswith("ui/game-icons-expansion/") and ("/Colored/" in p or "Game icons (base)/PNG" in p))
add(T, "kenney-boardgame", "Board game icons (Kenney)", "item", "flat", "Dice, cards, pawns, tokens", "CC0 · Kenney",
    lambda p: p.startswith("ui/board-game-icons/PNG/Default (64px)/"))
mc = "PrismarineJS/minecraft-assets"
mcv = sorted({f.split("/")[1] for f in tree(mc)[1] if f.startswith("data/") and f.count("/") >= 2}, key=lambda v: [int(x) if x.isdigit() else 0 for x in v.split(".")])[-1]
add(mc, "minecraft-items", f"Minecraft items ({mcv})", "item", "pixel", "Item textures", "© Mojang — inspiration only",
    lambda p: p.startswith(f"data/{mcv}/items/") and p.count("/") == 3)
add(mc, "minecraft-blocks", f"Minecraft blocks ({mcv})", "item", "pixel", "Block textures", "© Mojang — inspiration only",
    lambda p: p.startswith(f"data/{mcv}/blocks/") and p.count("/") == 3)
add("osrsbox/osrsbox-db", "osrs-items", "Old School RuneScape items", "item", "pixel", "Random 1,500 of ~26k item icons (numbered by item id)", "© Jagex — inspiration only",
    lambda p: p.startswith("docs/items-icons/"), name=lambda p: "item #" + stem(p), cap=1500)
add("aifazi/items-images", "fivem-items", "Inventory item images (FiveM)", "item", "realistic", "Food, weapons, tools, clothing, tech, toys (random 1,800)", "see repo",
    lambda p: p.endswith(".png") and "ghost_icons" not in p, cat=lambda p: p.split("/")[0], cap=1800)

# ------------------------------------------------------------------ EMOJI SETS (characters + items in one style)
def cps(p):
    s = stem(p).lower().replace("emoji_u", "")
    try: return [int(x, 16) for x in re.split(r"[-_]", s) if x]
    except ValueError: return None
def emoji_ok(p):
    c = cps(p)
    return bool(c) and not any(0x1F3FB <= x <= 0x1F3FF or 0x1F1E6 <= x <= 0x1F1FF or 0xE0020 <= x <= 0xE007F or x == 0x20E3 for x in c)
def emoji_name(p):
    parts = []
    for x in cps(p):
        if x in (0xFE0F, 0x200D): continue
        try: parts.append(unicodedata.name(chr(x)).lower())
        except ValueError: parts.append(chr(x))
    return " + ".join(parts[:3]) or stem(p)
def emoji_kind(p):
    c = cps(p)[0]
    people = 0x1F466 <= c <= 0x1F487 or 0x1F600 <= c <= 0x1F64F or 0x1F910 <= c <= 0x1F92F or 0x1F9B8 <= c <= 0x1F9B9 or 0x1F9D0 <= c <= 0x1F9DF or 0x1F470 <= c <= 0x1F47F
    animals = 0x1F400 <= c <= 0x1F43F or 0x1F980 <= c <= 0x1F9AE or c in (0x1F577, 0x1F578, 0x1F54A)
    return "c" if people or animals else "i"
E = dict(name=emoji_name, k=emoji_kind)
add("googlefonts/noto-emoji", "noto-3d", "Noto Emoji 3D", "both", "3d", "Google's 3D emoji: faces, people, animals, objects (skin tones/flags omitted)", "Apache 2.0",
    lambda p: p.startswith("3D/png/128/") and emoji_ok(p), **E)
add("googlefonts/noto-emoji", "noto-2d", "Noto Emoji flat", "both", "flat", "Classic flat Noto emoji (SVG)", "Apache 2.0",
    lambda p: p.startswith("2D/svg/") and emoji_ok(p), **E)
add("jdecked/twemoji", "twemoji", "Twemoji", "both", "flat", "Twitter-style flat emoji", "CC BY 4.0",
    lambda p: p.startswith("assets/svg/") and emoji_ok(p), **E)
add("hfg-gmuend/openmoji", "openmoji-color", "OpenMoji color", "both", "flat", "Outlined, friendly emoji", "CC BY-SA 4.0",
    lambda p: p.startswith("color/svg/") and emoji_ok(p), **E)
add("hfg-gmuend/openmoji", "openmoji-black", "OpenMoji black line", "both", "line", "Monochrome line emoji", "CC BY-SA 4.0",
    lambda p: p.startswith("black/svg/") and emoji_ok(p), **E)
add("microsoft/fluentui-emoji", "fluent-3d", "Fluent Emoji 3D", "both", "3d", "Microsoft's glossy 3D emoji", "MIT",
    lambda p: p.startswith("assets/") and p.count("/") == 3 and p.split("/")[2] == "3D" and p.endswith(".png"),
    name=lambda p: p.split("/")[1].lower())
add("microsoft/fluentui-emoji", "fluent-color", "Fluent Emoji color", "both", "flat", "Microsoft's flat color emoji", "MIT",
    lambda p: p.startswith("assets/") and p.count("/") == 3 and p.split("/")[2] == "Color", name=lambda p: p.split("/")[1].lower())
add("microsoft/fluentui-emoji", "fluent-flat", "Fluent Emoji flat", "both", "flat", "Microsoft's simplified flat emoji", "MIT",
    lambda p: p.startswith("assets/") and p.count("/") == 3 and p.split("/")[2] == "Flat", name=lambda p: p.split("/")[1].lower())
add("microsoft/fluentui-emoji", "fluent-hc", "Fluent Emoji high contrast", "both", "line", "Monochrome high-contrast emoji", "MIT",
    lambda p: p.startswith("assets/") and p.count("/") == 3 and p.split("/")[2] == "High Contrast", name=lambda p: p.split("/")[1].lower())
add("C1710/blobmoji", "blobmoji", "Blobmoji", "both", "blob", "Google's old blob-style emoji", "Apache 2.0",
    lambda p: p.startswith("svg/") and p.count("/") == 1 and not re.search(r"flag|skin tone", p) and (not stem(p).startswith("emoji_u") or emoji_ok(p)),
    name=lambda p: emoji_name(p) if stem(p).startswith("emoji_u") else clean(stem(p)))
add("mozilla/fxemoji", "fxemoji", "Firefox emoji", "both", "flat", "Mozilla FxEmoji (people, nature, objects, symbols)", "CC BY 4.0",
    lambda p: p.startswith("svgs/FirefoxEmoji/") and "layer" not in p, name=lambda p: clean(re.sub(r"^u[0-9A-Fa-f-]+-?", "", stem(p))) or stem(p))

# ------------------------------------------------------------------ DICEBEAR (live API; seeds generate endless characters)
DB = ["adventurer", "adventurer-neutral", "avataaars", "avataaars-neutral", "big-ears", "big-ears-neutral", "big-smile", "bottts", "bottts-neutral",
      "croodles", "croodles-neutral", "dylan", "fun-emoji", "glass", "icons", "lorelei", "lorelei-neutral", "micah", "miniavs", "notionists",
      "notionists-neutral", "open-peeps", "personas", "pixel-art", "pixel-art-neutral", "rings", "shapes", "thumbs"]
SEEDS = ["Felix", "Aneka", "Mia", "Leo", "Zoe", "Max", "Luna", "Oscar", "Ivy", "Jasper", "Nova", "Milo", "Ruby", "Finn", "Sage", "Atlas",
         "Cleo", "Otis", "Wren", "Hugo", "Pearl", "Rex", "Dune", "Fable"]
sources.append({"id": "dicebear", "label": "DiceBear (28 styles, live)", "kind": "character", "style": "mixed",
                "note": "Avatar generator — each style x 24 seeds, rendered live by api.dicebear.com. Change a seed in the URL for infinite variations.",
                "license": "styles vary (mostly CC0 / CC BY)", "url": "https://www.dicebear.com/styles/", "base": "",
                "items": [[f"{s} · {seed}", f"https://api.dicebear.com/9.x/{s}/svg?seed={seed}", s] for s in DB for seed in SEEDS]})
print("dicebear", len(DB) * len(SEEDS))

# base URLs need percent-encoding of paths; do it once here so the page stays simple
for s in sources:
    if s["id"] == "dicebear": continue
    for it in s["items"]:
        it[1] = "/".join(urllib.parse.quote(seg) for seg in it[1].split("/"))
json.dump(sources, open(OUT, "w"), separators=(",", ":"))
print("total", sum(len(s["items"]) for s in sources), "->", os.path.getsize(OUT) // 1024, "KB")
