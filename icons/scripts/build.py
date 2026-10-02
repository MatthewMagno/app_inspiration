import json, random, urllib.parse, os
random.seed(7)
repos = {r["repo"]: r for r in json.load(open("_raw/repos.json"))}
spec = [
 ("lihaoyun6/BigSur-icons", lambda p: p.startswith("thumbs/"), None, "macOS Big Sur-style replacements"),
 ("elrumo/macOS_Big_Sur_icons_replacements", lambda p: p.startswith("public/img/icons/"), None, "macOS Big Sur-style"),
 ("santielectronics/iOS14icons", lambda p: True, None, "iOS 14 home-screen packs (fade / gradient)"),
 ("SysAdminDoc/iOSIconPack", lambda p: "drawable-xxxhdpi" in p, None, "Six eras of iOS-inspired icons"),
 ("Delta-Icons/android", lambda p: "drawable-nodpi" in p, 1500, "Delta icon pack (Android, colorful)"),
 ("Arcticons-Team/Arcticons", lambda p: "app/src/normal/res/drawable-nodpi" in p, 700, "Arcticons (monotone line icons)"),
 ("wei1769/ColorfulOS", lambda p: "IconBundles" in p, None, "ColorfulOS iOS theme"),
 ("jimeh/emacs-liquid-glass-icons", lambda p: p.startswith("img/"), None, "Liquid Glass style"),
 ("pomegranar/kitty-liquid-glass", lambda p: p.startswith("exported_icons/"), None, "Liquid Glass style"),
]
sources = []
for repo, keep, cap, note in spec:
    r = repos[repo]
    files = [f for f in r["files"] if keep(f)]
    if cap and len(files) > cap: files = random.sample(files, cap)
    items = []
    for f in sorted(files):
        base = os.path.splitext(os.path.basename(f))[0].replace("_"," ").replace("-"," ")
        u = f"https://raw.githubusercontent.com/{repo}/{r['branch']}/" + "/".join(urllib.parse.quote(s) for s in f.split("/"))
        items.append({"n": base, "u": u, "l": f"https://github.com/{repo}/blob/{r['branch']}/{urllib.parse.quote(f)}"})
    sources.append({"id": repo, "type": "repo", "stars": r["stars"], "note": note, "url": f"https://github.com/{repo}", "items": items})
    print(repo, len(items))
apps = json.load(open("_raw/apps.json"))
apps = [a for a in apps if a["ratings"] >= 200]
items = [{"n": a["name"], "u": a["icon"].replace("512x512bb","256x256bb"), "l": a["url"], "g": a["genre"], "r": a["ratings"], "s": a["avg"]} for a in apps]
sources.append({"id": "App Store", "type": "store", "note": "Real App Store icons, most-rated first", "url": "https://apps.apple.com", "items": items})
print("appstore", len(items))
json.dump(sources, open("../data/gallery.json","w"), separators=(",",":"))
