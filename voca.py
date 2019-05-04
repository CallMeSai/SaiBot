import json
import requests
import re
import discord
import datetime
#store api url
vocaapi = "https://vocadb.net/api/"

def voca(vocamsg):
    #if error occurs return no value error. User mistyped request or requests
    #  request does not exist.
    try:
        #if request does not contain only artist
        if vocamsg[0] != "a":
            #if request only contains song, request top song matching request
            if vocamsg[0] == "s":
                r = requests.get(vocaapi + "songs?query=" + vocamsg[1] + "&maxResults=1&sort=RatingScore&nameMatchMode=Auto&fields=Artists,ThumbUrl,PVs,Tags&Lang=Default,English").json()['items']
                if not r: raise Exception("NoValue")
                else: r = r[0]
            #else user requesting specific song and artist.
            #  request song and artist separately
            else:
                #request all songs matching user request
                rs = requests.get(vocaapi + "songs?query=" + vocamsg[0] + "&sort=RatingScore&nameMatchMode=Auto&fields=Artists,ThumbUrl,PVs,Tags&Lang=Default,English").json()['items']
                #if rs is empty return NoValue exception
                if not rs:
                    raise Exception("NoValue")
                #request all artists matching user request
                ra = requests.get(vocaapi + "artists?query=" + vocamsg[1] + "&nameMatchMode=Auto&lang=English&sort=FollowerCount").json()['items']

                output = []
                #for each song in rs and each artist in song, if artist matches
                #  user requested artist, add songid, artistid and songrating
                #  a list and stop loop
                for a in ra:
                    for s in rs:
                        for sa in s['artists']:
                            try:
                                if a['id'] == sa['artist']['id']:
                                    output = s['id']
                                    break
                        #if artist does not have an id, go to next result.
                            except KeyError: continue
                #select top song w/ artist from rs
                try:
                    for a in rs:
                        if output == a['id']:
                            r = a
                    if not r:
                        r = rs[0]
                #if no song w/ artist could be found, return first song in rs
                except: r = rs[0]
            tags = []
            pvs = []
            #put top 5 tags into tags list
            for t in range(5):
                try:
                    tags.append(sorted(r['tags'],key=lambda tag: tag['count'],reverse=True)[t]['tag']['name'])
                #if song has less than 5 tags, break loop at final tag
                except IndexError: break
            #put all PV links into pv list
            for p in r['pvs']:
                if p['pvType'] == "Original":
                    pvs.append(p['url'])
            tags.sort(reverse=True)
            #structure and return embed response.
            embed = discord.Embed(title=r['name'] + ' - ' + r['artistString'],url="https://vocadb.net/S/"+str(r['id']))
            embed.set_thumbnail(url=r['thumbUrl'])
            embed.add_field(name="Type",value = r['songType'])
            embed.add_field(name="Duration",value=str(datetime.timedelta(seconds=int(r['lengthSeconds']))))
            if tags:embed.add_field(name="Tags",value=", ".join(tags))
            if pvs:embed.add_field(name="PV",value="\n".join(pvs))

        #else if message contains only an artist request artist with most
        #  followers
        elif vocamsg[0] == "a":
            r = requests.get(vocaapi + "artists?query=" + vocamsg[1] + "&fields=Tags,MainPicture&maxResults=1&nameMatchMode=Auto&lang=English&sort=FollowerCount").json()['items'][0]
            #put top 5 tags into tags list
            tags = []
            for t in range(5):
                try:
                    tags.append(sorted(r['tags'],key=lambda tag: tag['count'],reverse=True)[t]['tag']['name'])
                #if aritst has less than 5 tags, break loop at final tag.
                except IndexError: break
            #structure and return embed response
            embed = discord.Embed(title=r['name'] + ", " + r['defaultName'],url="https://vocadb.net/Ar/"+str(r['id']))
            embed.set_thumbnail(url=r['mainPicture']['urlTinyThumb'])
            embed.add_field(name="Type",value = r['artistType'])
            embed.add_field(name="Tags",value=", ".join(tags))
        return embed
    except IndexError: return Exception("IndexError")
    except: return Exception("NoValue")
