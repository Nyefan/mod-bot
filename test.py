import asyncio
import discord

#custom classes
import globalValues

#print out the number of messages the user has in the last 100 messages from that channel
#TODO: make this admin-only and work like a unit test
async def main(message, client):
	counter = 0
	tmp = await client.send_message(message.channel, 'Calculating messages...')
	async for log in client.logs_from(message.channel, limit=100):
			if log.author == message.author:
				counter += 1
	await client.edit_message(tmp, 'You have {} messages.'.format(counter))

function = main
