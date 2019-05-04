import json
import requests
import re
import discord
import datetime

vocaapi = "https://vocadb.net/api/"
output = []
def artist(vocamsg):
    r = requests.get(vocaapi + "artists?query=" + vocamsg + "&fields=Tags,MainPicture&maxResults=1&nameMatchMode=Auto&lang=English&sort=FollowerCount").json()['items'][0]
    print(json.dumps(r,sort_keys=True,indent=2))
#def song(vocamsg):
#    r = requests.get(vocaapi + "songs?query=" + vocamsg[0] + "&maxResults=1&sort=RatingScore&nameMatchMode=Auto&fields=Artists,ThumbUrl,PVs,Tags&lang=English").json()['items'][0]
#    tags = []
#    pvs = []
#    for t in range(5):
#        tags.append(sorted(r['tags'],key=lambda tag: tag['count'],reverse=True)[t]['tag']['name'])
#    print (json.dumps(tags,sort_keys=True,indent=4))


#def voca(vocamsg):
#    if vocamsg[0] == "s":
#    rs = requests.get(vocaapi + "songs?query=" + vocamsg[0] + "&sort=RatingScore&nameMatchMode=Auto&fields=Artists,ThumbUrl,PVs,Tags&lang=English")
#    ra = requests.get(vocaapi + "artists?query=" + vocamsg[1] + "&nameMatchMode=Auto&lang=English&sort=FollowerCount")
#    for s in rs.json()['items']:
#        for sa in s['artists']:
#            for a in ra.json()['items']:
#                try:
#                    if a['id'] == sa['artist']['id']:
#                        row = [s['id'],a['id'],s['ratingScore']]
#                        output.append(row)
#                        break
#                except KeyError: continue
#    r = [r for r in rs.json()['items'] if output[0][0] == r['id']][0]
#    tags = []
#    pvs = []
#    for t in range(5):
#        tags.append(sorted(r['tags'],key=lambda tag: tag['count'],reverse=True)[t]['tag']['name'])
#    for p in r['pvs']:
#        if p['pvType'] == "Original":
#            pvs.append(p['url'])
#    tags.sort(reverse=True)
##    embed = discord.Embed(title=r['name'] + ' - ' + r['artistString'])
#    embed.set_thumbnail(url=r['thumbUrl'])
#    embed.add_field(name="Type",value = r['songType'])
#    embed.add_field(name="Duration",value=str(datetime.timedelta(seconds=int(r['lengthSeconds']))))
#    embed.add_field(name="Tags",value=", ".join(tags))
#    embed.add_field(name="PV",value="\n".join(pvs))

#    return embed


vocamsg = "yunosuke"
artist(vocamsg)
