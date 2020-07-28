"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
require('dotenv').config();
var anime_1 = require("./anime");
var discord = require('discord.js');
var client = new discord.Client();
var TOKEN = process.env.TOKEN;
client.on('ready', function () {
    console.log("Logged in as " + client.user.tag + "!");
    client.user.setActivity("with catnip", { type: "PLAYING" });
});
client.on('message', function (msg) {
    try {
        DoStuff(msg);
    }
    catch (err) {
        console.log(err.message);
    }
});
client.login(TOKEN);
function GetMessageContent(message) {
    var splitMessage = message.split('\n').pop().split(' ');
    console.log(splitMessage.length);
    console.log(splitMessage);
    if (splitMessage.length > 1) {
        var newMessage = [splitMessage.shift()];
        newMessage.push(splitMessage.join(" "));
        return newMessage;
    }
    else {
        return splitMessage;
    }
}
function DoStuff(msg) {
    if (msg.content.startsWith("$$")) {
        var messageContent = GetMessageContent(msg.content);
        var content = void 0;
        console.log(messageContent);
        switch (messageContent[0]) {
            case "$$ping":
                content = "pong";
                break;
            case "$$a":
                anime_1.anime(messageContent[1], msg.channel);
                break;
            default:
                content = "Invalid command";
                break;
        }
    }
}
