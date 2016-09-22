import asyncio
import datetime
import discord
import sched
import threading
import time

serverID = "143463728317202434"

localScheduler = sched.scheduler(time.time, time.sleep)

def fixedIntervalScheduler(server, interval, action, actionargs):
    threading.Timer(interval, fixedIntervalScheduler, (server, interval, action, actionargs)).start()
    #scheduler.enter(interval, 1, fixedIntervalScheduler, (server, scheduler, interval, action, actionargs))
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
    printString = "{{serverID: {}, ".format(server)
    printString = "{{serverID: {}, ".format(server)
    for i in options:
        printString = printString + "{}: {}, ".format(i, optionDict[i](server))
    printString = printString + "}"
    print(printString)
    
def run(client, timeDelay, optionString):
    localServer = None
    for s in client.servers:
        if s.id == serverID:
            localServer = s
    fixedIntervalScheduler(localServer, timeDelay, printStamp, optionString)