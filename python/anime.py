import discord
import requests
from pathlib import Path
import json
#store api url
anilist = 'https://graphql.anilist.co'


def anime(split_message):
    #check if anime file exists
    file = Path('anime/anime_' + split_message + ".txt")
    if file.is_file() is False:
        #structure api query
        query = '''
        query($title: String){
            Media (search: $title, type : ANIME, sort : SEARCH_MATCH){
                id
                title{
                    romaji
                    english
                    native
                }
                description
                averageScore
                coverImage{
                    medium
                }
            }
        }
        '''
        #store variables for query
        variables = {
            'title' : split_message
        }
        #send request to api. Store headers in headers and response in r
        r = requests.post(anilist, json={'query':query, 'variables': variables})
        status = r.status_code
        if status == 404: return Exception("NoValue")
        #create new file and dump response into file
        else:
            with file.open('w+') as newfile:
                json.dump(r.json(),newfile,indent=4)
                newfile.close()
    #open file
    if file.is_file() is True:
        anime = json.load(file.open())
        #store english and native names. Check if values are empty. If values are
        #empty, replace with '-'
        english = anime['data']['Media']['title']['english']
        native = anime['data']['Media']['title']['native']
        if not anime['data']['Media']['title']['english'] : english = '-'
        if not anime['data']['Media']['title']['native'] : native = '-'

        #remove <br> from desc
        desc = anime['data']['Media']['description'].replace('<br>','')

        #structure and return embed response.
        embed=discord.Embed(title=anime['data']['Media']['title']['romaji'], description=desc, color=0x02A9FF)
        embed.set_thumbnail(url=anime['data']['Media']['coverImage']['medium'])
        embed.add_field(name="Romaji", value=anime['data']['Media']['title']['romaji'], inline=True)
        embed.add_field(name="English", value=english, inline=True)
        embed.add_field(name="Native", value=native, inline=True)
        embed.add_field(name="Score", value=anime['data']['Media']['averageScore'],inline=True)
        embed.add_field(name="Link", value = "http://anilist.co/anime/" + str(anime['data']['Media']['id']),inline=True)
        return embed
