import json, subprocess, collections, sys
repos = ["game-icons/icons","microsoft/fluentui-emoji","hfg-gmuend/openmoji","PokeAPI/sprites","msikma/pokesprite","PrismarineJS/minecraft-assets","googlefonts/noto-emoji","twitter/twemoji","dicebear/dicebear","KenneyNL/Starter-Kit-3D-Platformer","miukimiu/react-kawaii","shinokada/svelte-kawaii","kenneyNL/assets"]
out=[]
for r in repos:
    p = subprocess.run(["gh","api",f"repos/{r}","--jq","[.default_branch,.stargazers_count,.description,.license.spdx_id]"],capture_output=True,text=True)
    try: br,stars,desc,lic = json.loads(p.stdout)
    except Exception: print("skip",r,p.stderr[:60]); continue
    t = subprocess.run(["gh","api",f"repos/{r}/git/trees/{br}?recursive=1"],capture_output=True,text=True)
    try: j=json.loads(t.stdout); tree=j["tree"]
    except Exception: print("notree",r); continue
    imgs=[x["path"] for x in tree if x["type"]=="blob" and x["path"].lower().endswith((".png",".svg",".webp",".jpg")) and x.get("size",0)<2_000_000]
    dirs=collections.Counter('/'.join(f.split('/')[:-1][:3]) for f in imgs).most_common(4)
    print(r,stars,lic,"trunc" if j.get("truncated") else "",len(imgs),dirs)
    out.append({"repo":r,"stars":stars,"branch":br,"desc":desc,"license":lic,"files":imgs,"truncated":j.get("truncated")})
json.dump(out,open("_raw/repos.json","w"))
