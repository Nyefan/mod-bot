import asyncio
import datetime
import discord
import io
import os
import sched
import threading
import time

import tokenFubar

serverID = tokenFubar.serverID
outputFile = "dataLogger"

localScheduler = sched.scheduler(time.time, time.sleep)

def fixedIntervalScheduler(server, interval, action, actionargs):
    threading.Timer(interval, fixedIntervalScheduler, (server, interval, action, actionargs)).start()
    action(server, actionargs)
    
def isAdmin(member):
    for r in member.roles:
        if r.name == "Mod":
            return True
    return False
    
    
def adminsOnline(server):
    numOnline = 0
    for member in server.members:
        if isAdmin(member) and (member.status == discord.Status.online or member.status == discord.Status.idle):
            numOnline+=1
    return numOnline

def dateTimeStamp(server):
    return '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.utcnow())
    
def membersActive(server):
    numOnline = 0
    for member in server.members:
        if member.status == discord.Status.online:
            numOnline+=1
    return numOnline
    
def membersOnline(server):
    numOnline = 0
    for member in server.members:
        if member.status == discord.Status.online or member.status == discord.Status.idle:
            numOnline+=1
    return numOnline
    
optionDict = { "adminsOnline"  : adminsOnline,
               "dateTimeStamp" : dateTimeStamp,
               "membersActive" : membersActive,
               "membersOnline" : membersOnline,
             }



def printStamp(server, optionString):
    options = optionString.split()
    printString = "{{serverID: {}".format(server)
    for i in options:
        printString = "{}, {}: {}".format(printString, i, optionDict[i](server))
    printString = printString + "}\n"
    
    with open(server.name + " - " + outputFile + ".log", "a") as file:
        file.write(printString)
    
def run(client, timeDelay, optionString=""):
    localServer = None
    for s in client.servers:
        if s.id == serverID:
            localServer = s
    fixedIntervalScheduler(localServer, timeDelay, printStamp, optionString)