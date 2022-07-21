#!/bin/bash
import discord
from discord.ext import commands
import requests
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import yaml
import os

with open('config.yml', 'r') as file: #Load Config
    conf=yaml.safe_load(file)

try:
    for disc,client,secret in os.environ.items():
        conf['discordToken'] = disc
        conf['clientID'] = client
        conf['clientSecret'] = secret
        conf['setup'] = False
        with open("config.yml", "w") as save:
            yaml.dump(conf, save)
except:
    print("No arguments provided. Attempting terminal setup.")
    if conf['setup'] == True:
        try:
            print("enter discord token")
            conf['discordToken'] = input()
            print("\033c")
            print("enter blizz client id")
            conf['clientID'] = input()
            print("\033c")
            print("enter blizz client secret")
            conf['clientSecret'] = input()
            print("\033c")
            print("Settings Saved.")
            conf['setup'] = False
            with open("config.yml", "w") as save:
                yaml.dump(conf, save)
        except:
            print("Terminal setup failed.")


bot = commands.Bot()

def getAccessToken(client_id, client_secret, region = conf['region']):
    data = { 'grant_type': 'client_credentials' }
    response = requests.post('https://%s.battle.net/oauth/token' % region, data=data, auth=(client_id, client_secret))
    tok = response.json()['access_token']
    return tok

wowTokenAPI = requests.get('https://eu.api.blizzard.com/data/wow/token/index?namespace=dynamic-' + str(conf['region']) + '&locale=en_US&access_token=' + str(getAccessToken(conf['clientID'], conf['clientSecret'])))

@bot.event  #Bot Init
async def on_ready():
    print("\033c") #Clear Terminal
    await update() #Set `Watching` status

#@bot.event #Standard Commands, Disabled
#async def on_message(message):
#    if message.author == bot.user:
#        return
#    if message.content.startswith('$token'):
#       await message.channel.send(wowToken())

@bot.slash_command(name="token", description="Prints the current EU WoW Token cost.")
async def tokenSlash(ctx): #This block adds a /command to Discord.
    await ctx.respond(getToken(formatted = True)) #This is the response given to the user.

def getToken(formatted=False): #This is where we're pulling the API. Grab price, then divide by 10000 (format bug)
    out = int(wowTokenAPI.json()['price'] / 10000)
    if formatted:
        out = "{:,}".format(out)+' Gold' #Adds the commas e.g 100,000,000,000
    return out

async def update(): #This updates the "Watching: Token 100,000 Gold"
    print("\033c")
    print("Current Token Price: " + getToken(formatted=True))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Token: " + getToken(formatted=True)))
    trig = "{:,}".format(int(conf["tokenAlarmCost"]))+' Gold'
    print("Current Alarm Threshold: " + trig)
    await tokenAlarm()

async def tokenAlarm(): #Handles the alarm should the price rise above the set threshold.
    cost = getToken(formatted=False)
    if cost > int(conf['tokenAlarmCost']):
        dout = "WoW token is currently exceeding " + "{:,}".format(int(conf["tokenAlarmCost"]))+' Gold' + ". Current Rate: " + "{:,}".format(cost)+' Gold.'
        await bot.get_channel(conf['tokenAlarmChannel']).send(dout) #Send to channel specified.

scheduler = AsyncIOScheduler() #This is just basically a crom job, it'll run the API every X seconds.
scheduler.add_job(update, 'interval', seconds=conf['updateInterval'])
scheduler.start()

bot.run(conf['discordToken']) #Get the party started!
