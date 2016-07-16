import asyncio
import discord

#TODO: make a parent class for the commands
#custom classes
import botHelp
import diceParser
import deleteMe
import deleteMessage
import globalValues
import printMe
import sleep
import test

switchDict = { "/delete": deleteMessage.function,
			   "/deleteme": deleteMe.function,
			   "/help": botHelp.function,
			   "/print": printMe.function,
			   "/roll": diceParser.function,
			   "/sleep": sleep.function,
			   "/test": test.function
			 }

async def parse(message, client):
	if message.content.startswith("/"):
		#TODO: only split once
		#TODO: a special case might be needed for help and test
		await switchDict.get(message.content.split()[0], botHelp.function)(message, client)
