import discord
import requests
from pathlib import Path
import json
import datetime

#Osu gamemodes
modes = ['osu','taiko','fruits','mania']

def osu(osumsg,key):
    #declare osuapi message
    osuapi = "https://osu.ppy.sh/api/get_beatmaps?k=" + str(key)
    #check if beatmapset file exists
    file = Path("osu\\beatmapset_" + osumsg[0] + ".txt")
    if file.is_file() is False:
        #send request to api, store response in r
        r = requests.post(osuapi + "&s=" + osumsg[0]).json()
        if not r:
            print("broke")
            return Exception("NoValue")
        #create new file and dump response into file
        else:
            with file.open('w+') as newfile:
                json.dump(r,newfile,indent=4)
                newfile.close()
    #open file
    print("Okay")
    if file.is_file() is True:
        osudata = json.load(file.open())
        #structure and return embed response.
        embed = discord.Embed(title=osudata[0]['title'])
        embed.set_thumbnail(url="https://b.ppy.sh/thumb/" + osudata[0]['beatmapset_id'] + ".jpg")
        embed.add_field(name="Duration",value = str(datetime.timedelta(seconds=int(osudata[0]['total_length']))),inline=False)
        #loop through each beatmap in beatmapset
        for x in osudata:
            try:
                count =0
                #if no beatmap was specified raise exception
                if osumsg[1] == '':
                    raise Exception
                #else find beatmapid in file and add CS, OD, AR and SR to embed
                # message
                elif x['beatmap_id'] == osumsg[1]:
                    embed.add_field(name="Circle Size",value = x['diff_size'],inline=True)
                    embed.add_field(name="OD", value = x['diff_overall'],inline=True)
                    embed.add_field(name="AR",value = x['diff_approach'], inline=True)
                    embed.add_field(name="SR", value = round(float(x['difficultyrating']),2),inline=True)
                    count +=1
            #if an exception was raised, add all beatmap modes, SR and diff name
            #  from beatmapset to embed message
            except:
                embed.add_field(name="Mode - Star - Diff", value = modes[int(x['mode'])] + " - " + str(round(float(x['difficultyrating']),2)) + " - " + x['version'],inline = False)

            if count == 0 and len(osumsg)>1: embed.add_field(name="Sorry",value="Beatmap not found",inline=True)
        #end embed with beatmapset audio clip and download link and return embed
        #  response
        embed.add_field(name="Audio Clip", value ="https://b.ppy.sh/preview/" + osudata[0]['beatmapset_id'] + ".mp3",inline=False)
        embed.add_field(name="Download" , value = "https://osu.ppy.sh/beatmapsets/" + osudata[0]['beatmapset_id'] + "/download",inline=True)
        return embed
