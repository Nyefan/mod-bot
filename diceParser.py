import asyncio
import discord
import re
import random

#custom classes
import globalValues

validDiceString = re.compile(r'''
								(
								 \dd\d+             # (1) required ndm
								 (k[hl]{1}\d+)?     # (2) optional khn or kln
								 \+?                # (3) optional +
								)+                  # (4) (1)-(3) may repeat
								(
								 \d+                # (5) optional final integer modifiers
								)*
							''', re.X)

validDice = re.compile(r'''
					   (
						   \dd\d+         # (1) required ndm
						   (k[hl]{1}\d+)? # (2) optional khn or kln
						   \+?            # (3) optional +
						)+                # (4) (1)-(3) may repeat
					   ''', re.X)

#ndice is the number of dice to roll
#diceSize is the number of values per dice
#keep is negative for keep lowest and positive for keep highest
def rollDice(nDice, diceSize, keep=0):
	total = 0
	dice = []
	keepHigh = True
	for i in range(nDice):
		dice.append(random.randint(1,diceSize))
	if keep < 0:
		keep*=-1
		keepHigh = False
	elif (keep == 0 or keep > nDice):
		keep = nDice
	for i in range(keep):
		if(keepHigh):
			temp = max(dice)
			total += temp
			dice.remove(temp)
		else:
			temp = min(dice)
			total += temp
			dice.remove(temp)
	return total

#diceString should be either a validDice or an integer string
#passing an integer string into diceString will return the integer
def parseDice(diceString):
	if not validDice.match(diceString):
		if re.fullmatch(r'\d+', diceString):
			return int(float(diceString))
		else: 
			return False
	
	temp = re.compile(r'(d)|(kh|kl)').split(diceString)
	if len(temp)==4:
		return rollDice(int(float(temp[0])),int(float(temp[3])))
	
	if temp[5] == 'kl': 
		temp[6]=-1*int(float(temp[6]))
		
	return rollDice(int(float(temp[0])), int(float(temp[3])), int(float(temp[6])))

def parseDiceString(diceString):
	diceString = diceString.split()[-1]
	
	if not validDiceString.match(diceString):
		return False
	
	total = 0
	for str in diceString.split('+'):
		total+=parseDice(str)
	
	return total

#parse dice rolls
async def main(message, client):
	await client.send_message(message.channel, parseDiceString(message.content))

function = main
