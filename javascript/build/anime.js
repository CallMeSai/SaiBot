"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.anime = void 0;
var anilist = 'https://graphql.anilist.co';
var fetch = require("node-fetch");
var discord = require('discord.js');
function anime(command, channel) {
    //TODO: List of previously polled anime
    var query = "query($title: String){\n        Media (search: $title, type : ANIME, sort : SEARCH_MATCH){\n            id\n            title{\n                romaji\n                english\n                native\n            }\n            description\n            averageScore\n            coverImage{\n                medium\n            }\n        }\n    }";
    var variables = {
        title: command
    };
    var request = anilist, options = {
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
    var response;
    fetch(request, options)
        .then(handleResponse)
        .then(formatEmbed)
        .then(function (msg) { channel.send(msg); })
        .catch(handleError);
}
exports.anime = anime;
function handleResponse(response) {
    return response.json().then(function (json) {
        return response.ok ? json : Promise.reject(json);
    });
}
function handleError(error) {
    alert('Error, check console');
    console.error(error);
}
function formatEmbed(data) {
    var title = data.data.Media.title.romaji;
    var engName = data.data.Media.title.english;
    var nativeName = data.data.Media.title.native;
    var thumbnail = data.data.Media.coverImage.medium;
    var score = data.data.Media.averageScore;
    var id = data.data.Media.id;
    var link = "http://anilist.co/anime/" + id;
    var description = data['data']['Media']['description'].replace("<br>", "");
    var message = new discord.MessageEmbed({
        title: title,
        description: description,
        hexColor: "0x02a9ff",
        thumbnail: {
            url: thumbnail
        }
    });
    message.addField("Romanji", title, true);
    message.addField("English", engName, true);
    message.addField("Native", nativeName, true);
    message.addField("Score", score, true);
    message.addField("Link", link, true);
    console.log(message);
    return message;
}
