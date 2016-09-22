import asyncio
import discord

#custom classes
import botHelp
#there's got to be a more elegant way to do this
import commandParser
import diceParser
import deleteMe
import deleteMessage
import globalValues
import printMe
import sleep
import test

#TODO: make a parent class for the commands
switchDict = { "delete": deleteMessage,
			   "deleteme": deleteMe,
			   "help": commandParser,
			   "print": printMe,
			   "roll": diceParser,
			   "sleep": sleep,
			   "test": test
			 }

async def function(message, client):
    try:
        await switchDict.get(message.content.split()[1], botHelp).helpFunction(message, client)
    except (AttributeError, IndexError):
        await botHelp.function(message, client)

async def parse(message, client):
	if message.content.startswith("/"):
		#TODO: only split once
		#TODO: a special case might be needed for help and test
		await switchDict.get(message.content.split()[0][1:], botHelp).function(message, client)
        

