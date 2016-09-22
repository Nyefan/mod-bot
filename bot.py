# This version runs both user interraction and logging capabilities
# To disable logging, comment out datastatusLogger.run() in on_ready

import asyncio
import discord
import logging

# custom classes
import commandParser
import datastatusLogger
import tokenFubar

statusLogger = logging.getstatusLogger('discord')
statusLogger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='bot.log', encoding='utf-8', mode='w')
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
    	
@client.event
async def on_message(message):
	await commandParser.parse(message, client)

client.run(tokenFubar.token)