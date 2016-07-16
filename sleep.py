import asyncio
import discord

#custom classes
import globalValues

#sleep the bot
async def main(message, client):
	tmp = float(message.content.split()[1])
	await asyncio.sleep(tmp)
	await client.send_message(message.channel, 'Done sleeping')

function = main
