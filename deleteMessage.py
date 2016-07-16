import asyncio
import discord

#custom classes
import globalValues

helpMessage = "."

#delete last x messages
#TODO: raise permissionExceededException for _permission_message
#      and a functionNotImplementedException for _todo_message
async def main(message, client):
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
		await client.send_message(message.channel, globalValues._permission_message)
		
function = main
