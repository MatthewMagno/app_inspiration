import json, subprocess
repos = ["elrumo/macOS_Big_Sur_icons_replacements","lihaoyun6/BigSur-icons","Delta-Icons/android","Arcticons-Team/Arcticons","jasonlong/iterm2-icons","santielectronics/iOS14icons","jottumseijner/icons","veefan404/dark-icons-mac","olankens/papirika","jimeh/emacs-liquid-glass-icons","wei1769/ColorfulOS","SysAdminDoc/iOSIconPack","Zabriskije/macOS-Icons","przemek-jablonski/feathericons-for-mobile","pomegranar/kitty-liquid-glass","k0nserv/kitty-icon","danielsaidi/AppIconKit","alexaubry/alternate-icons"]
out = []
for r in repos:
    p = subprocess.run(["gh","api",f"repos/{r}","--jq","[.default_branch,.stargazers_count,.description]"],capture_output=True,text=True)
    try: br, stars, desc = json.loads(p.stdout)
    except Exception: print("skip", r, p.stderr[:80]); continue
    t = subprocess.run(["gh","api",f"repos/{r}/git/trees/{br}?recursive=1"],capture_output=True,text=True)
    try: tree = json.loads(t.stdout)["tree"]
    except Exception: print("notree", r); continue
    imgs = [x["path"] for x in tree if x["type"]=="blob" and x["path"].lower().endswith((".png",".jpg",".jpeg",".webp")) and x.get("size",0) < 3_000_000]
    print(r, stars, br, len(imgs))
    out.append({"repo": r, "stars": stars, "branch": br, "desc": desc, "files": imgs})
json.dump(out, open("_raw/repos.json","w"))
