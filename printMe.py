import asyncio
import discord

#custom classes
import globalValues

#print the numbers from 1 to x
async def main(message, client):
	if (message.author.permissions_in(message.channel).administrator):
		for i in range(int(float(message.content.split()[1]))):
			await client.send_message(message.channel, i+1)
			await asyncio.sleep(globalValues._rate_limit)
	else:
		await client.sent_message(globalValues._permission_message)
		
function = main
