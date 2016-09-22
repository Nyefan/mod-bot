# This version runs only the logging capabilities

import asyncio
import discord
import logging

# custom classes
import dataLogger
import memberLogger
import tokenFubar

statusLogger = logging.getLogger('discord')
statusLogger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='logBot.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
statusLogger.addHandler(handler)

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    #print(client.servers)
    print('------')
    dataLogger.run(client, 300, "dateTimeStamp membersOnline adminsOnline membersActive")
    memberLogger.run(client, 60*60*24, "memberName memberNick")

client.run(tokenFubar.token)