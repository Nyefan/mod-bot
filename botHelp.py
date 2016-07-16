import asyncio
import discord

#custom classes
import globalValues

#TODO: implement this
#print the currently available commands 
async def main(message, client):
	await client.send_message(message.channel, globalValues._todo_message)

function = main
