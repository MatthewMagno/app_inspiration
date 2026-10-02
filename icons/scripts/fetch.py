import json, urllib.parse, time, subprocess
terms = """photo editor,journal,diary,couple,relationship,dating,wedding,habit tracker,meditation,sleep,fitness,workout,running,yoga,recipe,cooking,meal planner,budget,finance,banking,investing,crypto,weather,maps,travel,flights,hotel,notes,todo,calendar,planner,focus timer,reading,books,audiobook,podcast,music,radio,video editor,camera,filters,scanner,pdf,keyboard,wallpaper,widgets,social,chat,messenger,family,kids,education,language learning,math,puzzle,word game,casual game,strategy game,rpg,card game,trivia,shopping,coupons,delivery,food,coffee,pets,plants,garden,health,period tracker,pregnancy,therapy,mood,gratitude,vpn,password,security,vpn,productivity,email,browser,ai assistant,chatbot,translator,dictionary,drawing,sketch,design,fonts,stickers,emoji,memories,scrapbook,photo book,gift,birthday,anniversary,countdown,bucket list,date ideas,location,sports,golf,soccer,basketball,fishing,cars,parking,news,stocks,tv,streaming,movies,fashion,beauty,home,real estate,jobs""".split(",")
seen = {}
for t in dict.fromkeys(terms):
    for country in ("us",):
        u = "https://itunes.apple.com/search?" + urllib.parse.urlencode({"term": t, "entity": "software", "limit": 200, "country": country})
        try:
            data = json.loads(subprocess.run(['curl','-s','--max-time','25',u],capture_output=True,text=True).stdout)
        except Exception as e:
            print("fail", t, e); time.sleep(2); continue
        for r in data.get("results", []):
            i = r["trackId"]
            if i in seen: continue
            seen[i] = {"id": i, "name": r["trackName"], "genre": r.get("primaryGenreName",""), "icon": r["artworkUrl512"], "url": r.get("trackViewUrl",""), "ratings": r.get("userRatingCount",0), "avg": round(r.get("averageUserRating",0) or 0,1), "dev": r.get("artistName",""), "term": t}
        print(t, len(seen), flush=True)
        time.sleep(0.4)
apps = sorted(seen.values(), key=lambda a: -a["ratings"])
json.dump(apps, open("_raw/apps.json","w"))
print("TOTAL", len(apps))
