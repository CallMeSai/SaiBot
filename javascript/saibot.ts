require('dotenv').config();
import {anime} from "./anime";

const discord = require('discord.js');
const client = new discord.Client();
const TOKEN =  process.env.TOKEN;


client.on('ready', () => {
    console.log(`Logged in as ${client.user.tag}!`);
    client.user.setActivity("with catnip", { type: "PLAYING" });
});

client.on('message', (msg:any) => {
    try{ 
        DoStuff(msg)
    }
    catch(err){
        console.log(err.message)
    }
});

client.login(TOKEN);

function GetMessageContent(message: string){
    let splitMessage: string[]  = message.split('\n').pop()!.split(' ');
    console.log(splitMessage.length);
    console.log(splitMessage);
    if (splitMessage.length > 1){
        let newMessage: string[] = [splitMessage.shift()!];
        newMessage.push(splitMessage.join(" "));
        return newMessage;
    }
    else{
        return splitMessage;
    }
    
}

function DoStuff(msg: any){
    if (msg.content.startsWith("$$")){
        let messageContent: string[] = GetMessageContent(msg.content);
           
        let content: string ;
        console.log(messageContent);
        switch (messageContent[0]){
            case "$$ping":
                content = "pong";
                break;
            case "$$a":
                anime(messageContent[1], msg.channel);
                break;
            default:
                content = "Invalid command";
                break;
        }


    }

}