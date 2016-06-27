import asyncio
import discord
import logging

import diceParser

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='bot.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = discord.Client()

_permission_message = 'You do not have permission to do that.  Please contact an admin.'
_rate_limit = 0.5

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
	#print out the number of messages the user has in the last 100 messages from that channel
	if message.content.startswith('!test'):
		counter = 0
		tmp = await client.send_message(message.channel, 'Calculating messages...')
		async for log in client.logs_from(message.channel, limit=100):
			if log.author == message.author:
				counter += 1
		
		await client.edit_message(tmp, 'You have {} messages.'.format(counter))
	#delete message
	elif message.content.startswith('!deleteme'):
		await client.delete_message(message)
	#print the numbers from 1 to x
	elif message.content.startswith('!print'):
		if (message.author.permissions_in(message.channel).administrator):
			for i in range(int(float(message.content.split()[1]))):
				await client.send_message(message.channel, i+1)
				await asyncio.sleep(_rate_limit)
		else:
			await client.sent_message(_permission_message)
	#delete last x messages
	elif message.content.startswith('!delete'):
		perms = message.author.permissions_in(message.channel)
		if perms.administrator or perms.manage_messages:
			try: 
				tmp = int(float(message.content.split()[1]))
				await client.purge_from(message.channel, limit = tmp)
			except discord.errors.HTTPException as e:
				if e.response.status == 429:
					await asyncio.sleep(e.response['RETRY-AFTER'])
					await client.purge_from(message.channel, limit = tmp) 
		else:
			await client.send_message(message.channel, _permission_message)
			
	#sleep the bot
	elif message.content.startswith('!sleep'):
		tmp = float(message.content.split()[1])
		await asyncio.sleep(tmp)
		await client.send_message(message.channel, 'Done sleeping')
	
	#parse dice rolls
	elif message.content.startswith('/roll'):
		await client.send_message(message.channel, diceParser.parseDiceString(message.content))

client.run(token.token)
