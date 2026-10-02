import json, random, urllib.parse, os, re
random.seed(11)
R={r["repo"]:r for r in json.load(open("_raw/repos.json"))}
om={e["hexcode"].upper():e["annotation"] for e in json.load(open("_raw/openmoji.json"))}
def raw(repo,path):
    return f"https://raw.githubusercontent.com/{repo}/{R[repo]['branch']}/"+"/".join(urllib.parse.quote(s) for s in path.split("/"))
def blob(repo,path):
    return f"https://github.com/{repo}/blob/{R[repo]['branch']}/"+"/".join(urllib.parse.quote(s) for s in path.split("/"))
def pretty(s): return re.sub(r"[_\-]+"," ",os.path.splitext(os.path.basename(s))[0]).strip()
def hexname(f):
    h=re.sub(r"^emoji_u","",os.path.splitext(os.path.basename(f))[0]).replace("_","-").upper()
    return om.get(h) or om.get(h+"-FE0F") or om.get(h.replace("-FE0F","")) or h
def make(repo,pred,cap,namer,note,label,group=None):
    fs=[f for f in R[repo]["files"] if pred(f)]
    if cap and len(fs)>cap: fs=random.sample(fs,cap)
    items=[{"n":namer(f),"u":raw(repo,f),"l":blob(repo,f),**({"g":group(f)} if group else {})} for f in sorted(fs)]
    print(label,len(items))
    return {"id":label,"type":"repo","stars":R[repo]["stars"],"license":R[repo]["license"],"note":note,"url":f"https://github.com/{repo}","items":items}
S=[]
S.append(make("game-icons/icons",lambda f:f.endswith(".svg"),1800,pretty,"Fantasy/RPG item and character glyphs (CC BY 3.0, credit authors)","game-icons.net",lambda f:f.split("/")[0]))
S.append(make("microsoft/fluentui-emoji",lambda f:"/3D/" in f and f.endswith(".png") and "/Default/" not in f and "/Medium" not in f and "/Dark" not in f and "/Light" not in f,1500,lambda f:f.split("/")[1],"Glossy 3D emoji: characters, food, objects","Fluent 3D emoji"))
S.append(make("microsoft/fluentui-emoji",lambda f:"/Flat/" in f and f.endswith(".svg") and "/Default/" not in f and "/Medium" not in f and "/Dark" not in f and "/Light" not in f,1500,lambda f:f.split("/")[1],"Flat vector emoji","Fluent Flat emoji"))
S.append(make("hfg-gmuend/openmoji",lambda f:f.startswith("color/72x72/") and "-" not in os.path.basename(f),1300,hexname,"Outlined flat-color emoji (CC BY-SA 4.0)","OpenMoji"))
S.append(make("googlefonts/noto-emoji",lambda f:f.startswith("3D/png/128/") and "_" not in os.path.basename(f)[7:],900,hexname,"Google's 3D Noto emoji (OFL)","Noto 3D emoji"))
S.append(make("msikma/pokesprite",lambda f:f.startswith("icons/pokemon/regular/") and "-" not in os.path.basename(f),600,pretty,"Pixel-art creature icons","Pokesprite creatures"))
S.append(make("msikma/pokesprite",lambda f:f.startswith("items/") and f.count("/")==2,0,pretty,"Pixel-art item icons (potions, balls, gear)","Pokesprite items",lambda f:f.split("/")[1]))
S.append(make("PokeAPI/sprites",lambda f:f.startswith("sprites/pokemon/other/official-artwork/") and f.count("/")==4 and "shiny" not in f,700,lambda f:"#"+pretty(f),"Painted character art","Official-artwork creatures"))
S.append(make("PrismarineJS/minecraft-assets",lambda f:f.startswith("data/1.21.11/items/"),0,pretty,"Chunky pixel item icons","Minecraft items"))
# DiceBear
styles=["adventurer","avataaars","big-ears","big-smile","bottts","croodles","dylan","fun-emoji","lorelei","micah","miniavs","notionists","open-peeps","personas","pixel-art","thumbs","icons"]
seeds="fox,otter,comet,pepper,maple,bean,juniper,pixel,ember,cosmo,mochi,nova,pip,sage,tofu,velvet,wren,yuzu,zinc,biscuit,clover,dusk,echo,fable,gizmo,haze,iris,jelly".split(",")
db=[]
for st in styles:
    for sd in seeds:
        db.append({"n":f"{st} · {sd}","u":f"https://api.dicebear.com/9.x/{st}/svg?seed={sd}","l":f"https://www.dicebear.com/styles/{st}/","g":st})
S.append({"id":"DiceBear avatars","type":"repo","stars":R["dicebear/dicebear"]["stars"],"license":"per-style (mostly CC0/CC BY)","note":"Procedural character art in 17 styles, rendered by the DiceBear API","url":"https://github.com/dicebear/dicebear","items":db})
print("dicebear",len(db))
apps=[a for a in json.load(open("_raw/apps.json")) if a["ratings"]>=100]
S.append({"id":"App Store","type":"store","note":"Icons of real apps built around characters, pets and mascots","url":"https://apps.apple.com","items":[{"n":a["name"],"u":a["icon"].replace("512x512bb","256x256bb"),"l":a["url"],"g":a["genre"],"r":a["ratings"],"s":a["avg"]} for a in apps]})
print("appstore",len(apps))
os.makedirs("../data",exist_ok=True)
json.dump(S,open("../data/gallery.json","w"),separators=(",",":"))
