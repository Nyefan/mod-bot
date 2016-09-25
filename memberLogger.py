import asyncio
import datetime
import discord
import functools
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
    # DON'T CHANGE THE ORDER OF THESE OPERATIONS
    threading.Timer(interval, fixedIntervalScheduler, (server, interval, action, actionargs)).start()
    action(server, actionargs)

def dateTimeStamp(member):
    # returns the string, "yyyy-mmm-dd HH:MM:SS"
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
    
def memberRoles(member):
    # returns the string, "{member.roles.id[1], member.roles.id[2], ..., member.roles.id[last]}"
    return "{{{}}}".format(functools.reduce((lambda a, b: "{}, {}".format(a, b)), map((lambda x: x.id), member.roles)))
    
def memberStatus(member):
    return member.status

def roleColor(role):
    return role.color
    
def roleHoist(role):
    return role.hoist
    
def roleID(role):
    return role.id

def roleManaged(role):
    return role.managed
    
def roleMentionable(role):
    return role.mentionable
    
def roleMentionString(role):
    return role.mention
    
def roleName(role):
    return role.name
    
def rolePermissions(role):
    return role.permissions.value
    
def rolePosition(role):
    return role.position
    
optionDict = { "dateTimeStamp" : dateTimeStamp,
               "memberGame"    : memberGame,
               "memberID"      : memberID,
               "memberIdle"    : memberIdle,
               "memberName"    : memberName,
               "memberNick"    : memberNick,
               "memberOffline" : memberOffline,
               "memberOnline"  : memberOnline,
               "memberRoles"   : memberRoles,
               "memberStatus"  : memberStatus,
               "roleID"        : roleID,
               "roleName"      : roleName,
               "rolePerms"     : rolePermissions,
               "roleColor"     : roleColor,
               "roleColour"    : roleColor,
               "roleHoist"     : roleHoist,
               "rolePosition"  : rolePosition,
               "roleManaged"   : roleManaged,
               "roleMention"   : roleMentionable,
               "roleMentionStr": roleMentionString
             }



#TODO: refactor these out into separate functions
#TODO: require dateTimeStamp, memberID, and roleID to be passed in like any other query             
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
    
def printRoleList(client, optionString):
    localServer = None
    for s in client.servers:
        if s.id == serverID:
            localServer = s
    options = optionString.split()
    printString = ""
    for r in localServer.roles:
        printString = "{}{{roleID: {}".format(printString, r.id)
        for o in options:
            printString = "{}, {}: {}".format(printString, o, optionDict[o](r))
        printString = "{}}}\n".format(printString)
    
    with open(localServer.name + " - " + outputFile + ".rolelist", "w") as file:
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