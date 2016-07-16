import asyncio
import discord

#custom classes
import globalValues

#delete message
async def main(message, client):
	await client.delete_message(message)
	
function = main
