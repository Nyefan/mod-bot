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
    
def memberID(member):
    return member.id

def memberGame(member):
    return member.game
    
def memberStatus(member):
    return member.status

def memberName(member):
    return member.name
    
def memberNick(member):
    return member.nick
    
optionDict = { "dateTimeStamp" : dateTimeStamp,
               "memberID"      : memberID,
               "memberStatus"  : memberStatus,
               "memberName"    : memberName,
               "memberNick"    : memberNick
             }



def printStamp(server, optionString):
    options = optionString.split()
    printString = ""
    for m in server.members:
        printString = "{}{{memberID: {}".format(printString, m.id)
        for i in options:
            printString = "{}, {}: {}".format(printString, i, optionDict[i](m))
        printString = "{}}}\n".format(printString)
    
    with open(server.name + " - " + outputFile + ".memberlist", "w") as file:
        file.write(printString)
    
def run(client, timeDelay, optionString=""):
    localServer = None
    for s in client.servers:
        if s.id == serverID:
            localServer = s
    fixedIntervalScheduler(localServer, timeDelay, printStamp, optionString)