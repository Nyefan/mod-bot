import asyncio
import discord

# custom classes
import diceParser

_todo_message = 'This functionality has not yet been implemented.  Please contact the bot maintainer.'
_permission_message = 'You do not have permission to do that.  Please contact an admin.'
_rate_limit = 0.5

#TODO: implement this
#print the currently available commands 
async def bothelp(message, client):
	await client.send_message(message.channel, _todo_message)

#delete last x messages
async def delete(message, client):
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

#delete message
async def deleteme(message, client):
	await client.delete_message(message)

#print the numbers from 1 to x
async def printme(message, client):
	if (message.author.permissions_in(message.channel).administrator):
		for i in range(int(float(message.content.split()[1]))):
			await client.send_message(message.channel, i+1)
			await asyncio.sleep(_rate_limit)
	else:
		await client.sent_message(_permission_message)

#parse dice rolls
async def roll(message, client):
	await client.send_message(message.channel, diceParser.parseDiceString(message.content))

#sleep the bot
async def sleep(message, client):
	tmp = float(message.content.split()[1])
	await asyncio.sleep(tmp)
	await client.send_message(message.channel, 'Done sleeping')

#print out the number of messages the user has in the last 100 messages from that channel
async def test(message, client):
	counter = 0
	tmp = await client.send_message(message.channel, 'Calculating messages...')
	async for log in client.logs_from(message.channel, limit=100):
			if log.author == message.author:
				counter += 1
	await client.edit_message(tmp, 'You have {} messages.'.format(counter))

switchDict = { "/delete": delete,
			   "/deleteme": deleteme,
			   "/help": bothelp,
			   "/print": printme,
			   "/roll": roll,
			   "/sleep": sleep,
			   "/test": test
			 }

async def parse(message, client):
	if message.content.startswith("/"):
		#TODO: only split once
		await switchDict.get(message.content.split()[0], bothelp)(message, client)

#DEPRECATED
async def parse_old(message, client):
	#print out the number of messages the user has in the last 100 messages from that channel
	if message.content.startswith('/test'):
		counter = 0
		tmp = await client.send_message(message.channel, 'Calculating messages...')
		async for log in client.logs_from(message.channel, limit=100):
			if log.author == message.author:
				counter += 1
		
		await client.edit_message(tmp, 'You have {} messages.'.format(counter))
	#delete message
	elif message.content.startswith('/deleteme'):
		await client.delete_message(message)
	#print the numbers from 1 to x
	elif message.content.startswith('/print'):
		if (message.author.permissions_in(message.channel).administrator):
			for i in range(int(float(message.content.split()[1]))):
				await client.send_message(message.channel, i+1)
				await asyncio.sleep(_rate_limit)
		else:
			await client.sent_message(_permission_message)
	#delete last x messages
	elif message.content.startswith('/delete'):
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
	elif message.content.startswith('/sleep'):
		tmp = float(message.content.split()[1])
		await asyncio.sleep(tmp)
		await client.send_message(message.channel, 'Done sleeping')
	
	#parse dice rolls
	elif message.content.startswith('/roll'):
		await client.send_message(message.channel, diceParser.parseDiceString(message.content))
