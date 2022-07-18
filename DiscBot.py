import discord
import requests
from apscheduler.schedulers.asyncio import AsyncIOScheduler

client = discord.Client()
wowTokenAPI = requests.get("ENTER WOW TOKEN API HERE")

@client.event  #INIT
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    # Setting `Watching` status
    await updateStatus()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$token'):
        await message.channel.send(wowToken())

    if message.content.startswith('$update'):
        await updateStatus()

def wowToken():
    call = wowTokenAPI.json()
    price = call['price']
    output = int(price / 10000)  #WOW TOKEN IS FOR SOME REASON MULTIPLIED BY 10,000
    wowT = "{:,}".format(output)+'G'
    print(wowT)
    return wowT

async def updateStatus(): #UPDATES SUBSCRIPT OF BOT WITH WATCHING TOKEN: 200,000G
    cost = wowToken()
    print('Status Updated')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Token: " + cost))

scheduler = AsyncIOScheduler() #RUNS UPDATESTATUS ON THE BOT EVERY X SECONDS / MINUTES / HOURS
scheduler.add_job(updateStatus, 'interval', minutes=5)
scheduler.start()


client.run('ENTER DISCORD TOKEN HERE')
