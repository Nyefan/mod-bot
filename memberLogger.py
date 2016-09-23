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
outputFile = "memberLogger"

localScheduler = sched.scheduler(time.time, time.sleep)

def fixedIntervalScheduler(server, interval, action, actionargs):
    threading.Timer(interval, fixedIntervalScheduler, (server, interval, action, actionargs)).start()
    action(server, actionargs)

def dateTimeStamp(member):
    return '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.utcnow())
    
def memberGame(member):
    return member.game
    
def memberID(member):
    return member.id

def memberIdle(member):
    return member.status == discord.status.idle

def memberName(member):
    return member.name
    
def memberNick(member):
    return member.nick
    
def memberOffline(member):
    return member.status == discord.status.offline
    
def memberOnline(member):
    return member.status == discord.status.offline
    
def memberStatus(member):
    return member.status
    
optionDict = { "dateTimeStamp" : dateTimeStamp,
               "memberGame"    : memberGame,
               "memberID"      : memberID,
               "memberIdle"    : memberIdle,
               "memberName"    : memberName,
               "memberNick"    : memberNick,
               "memberOffline" : memberOffline,
               "memberOnline"  : memberOnline,
               "memberStatus"  : memberStatus
             }



def printMemberList(client, optionString):
    localServer = None
    for s in client.servers:
        if s.id == serverID:
            localServer = s
    options = optionString.split()
    printString = ""
    for m in localServer.members:
        printString = "{}{{memberID: {}".format(printString, m.id)
        for i in options:
            printString = "{}, {}: {}".format(printString, i, optionDict[i](m))
        printString = "{}}}\n".format(printString)
    
    with open(localServer.name + " - " + outputFile + ".memberlist", "w") as file:
        file.write(printString)
    
def printStamp(server, optionString):
    options = optionString.split()
    printString = "{{dateTimeStamp: {}".format(dateTimeStamp(None))
    for o in options:
        printString = "{}, {}: {{".format(printString, o)
        for m in server.members:
            if optionDict[o](m):
                printString = "{}{}: {}, ".format(printString, m.id, optionDict[o](m))
        printString = "{}}}".format(printString)
    printString = "{}\n".format(printString)
    
    with open(server.name + " - " + outputFile + ".membertimeseries", "a") as file:
        file.write(printString)
    
def run(client, timeDelay, optionString=""):
    localServer = None
    for s in client.servers:
        if s.id == serverID:
            localServer = s
    fixedIntervalScheduler(localServer, timeDelay, printStamp, optionString)