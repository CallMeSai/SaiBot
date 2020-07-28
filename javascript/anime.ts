import { query } from "express";

const anilist = 'https://graphql.anilist.co'
const fetch = require("node-fetch");
const discord = require('discord.js');

interface queryResponse {
    data:{
        Media : {
            id: number
            title: {
                romaji:string
                english:string
                native:string
            }
            description:string
            averageScore:number
            coverImage:{
                medium:string
            }
        }
    }
}

export function anime(command: string, channel:any){
    //TODO: List of previously polled anime
    let query:string = 
    `query($title: String){
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
    }`;

    let variables: object = {
        title: command
    };

    let request = anilist,
    options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
        body: JSON.stringify({
            query: query,
            variables: variables
        })
    };
    //let variables: JSON = JSON.parse(`{"title": "${command}"}`)
    let response;
    fetch(request,options)
        .then(handleResponse)
        .then(formatEmbed)
        .then((msg: any) => {channel.send(msg)})
        .catch(handleError);
}

function handleResponse(response:any ){
    return response.json().then(function(json: JSON){
        return response.ok ? json : Promise.reject(json);
    });
}

function handleError(error: any){
    alert('Error, check console');
    console.error(error);
}

function formatEmbed(data:queryResponse){
    let title: string = data.data.Media.title.romaji;
    let engName:string = data.data.Media.title.english;
    let nativeName:string = data.data.Media.title.native;
    let thumbnail:string = data.data.Media.coverImage.medium;
    let score:number = data.data.Media.averageScore;
    let id:number = data.data.Media.id;
    let link:string = `http://anilist.co/anime/${id}`;
    let description:string = data['data']['Media']['description'].replace("<br>","");

    let message:any = new discord.MessageEmbed({
            title : title,
            description: description,
            hexColor: "0x02a9ff",
            thumbnail: {
                url: thumbnail
            }
    });
    message.addField("Romanji",title,true);
    message.addField("English",engName,true);
    message.addField("Native",nativeName,true);
    message.addField("Score",score,true);
    message.addField("Link",link,true);

    console.log(message);

    return message;
}
