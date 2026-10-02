import json, urllib.parse, time, subprocess
terms = "virtual pet,tamagotchi,mascot,monster collector,creature,cozy game,idle rpg,farm game,pixel rpg,dungeon crawler,card battler,avatar maker,cute pet,dragon,fairy tale,adventure rpg,hero,animals,kawaii,sticker characters,emoji maker,memoji,character creator,mythology,knight,wizard,robot,alien,dinosaur,cat game,dog game,fish tank,garden pets,monster battle,tower defense heroes,merge game,match three characters,kids learning characters,story game,visual novel".split(",")
seen={}
for t in terms:
    u="https://itunes.apple.com/search?"+urllib.parse.urlencode({"term":t,"entity":"software","limit":200,"country":"us"})
    try: data=json.loads(subprocess.run(['curl','-s','--max-time','25',u],capture_output=True,text=True).stdout)
    except Exception as e: print("fail",t); continue
    for r in data.get("results",[]):
        if r["trackId"] in seen: continue
        seen[r["trackId"]]={"id":r["trackId"],"name":r["trackName"],"genre":r.get("primaryGenreName",""),"icon":r["artworkUrl512"],"url":r.get("trackViewUrl",""),"ratings":r.get("userRatingCount",0),"avg":round(r.get("averageUserRating",0) or 0,1)}
    print(t,len(seen),flush=True)
    time.sleep(0.3)
json.dump(sorted(seen.values(),key=lambda a:-a["ratings"]),open("_raw/apps.json","w"))
print("TOTAL",len(seen))
