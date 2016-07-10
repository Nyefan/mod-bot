import asyncio
import discord
import logging

# custom classes
import diceParser
import commandParser
import tokenFubar

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='bot.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = discord.Client()

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	#TODO: print server names
	#print(client.servers)
	print('------')
	
@client.event
async def on_message(message):
	await commandParser.parse(message, client)

client.run(tokenFubar.token)
