# bot.py
import os
import json
import discord
#from dotenv import load_dotenv
from scrape import stockmarket, cryptocurrency, economy
from discord.ext import tasks
import sqlite3
from discord.ext import commands
import requests

import scrapetube

videos = scrapetube.get_channel("UCbMxL09h7hHn8cypnrlQJFA/videos")


#load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True
stockchannelid = "975382026867859526"
cryptochannelid = "975378563400368148"
youtubechannelid = "975378520438104107"
economychannelid = "975620805381734440"
guildid = "975378520438104104"
JSON_FILE = str(os.path.dirname(os.path.realpath(__file__))) + '/data.json'

bot = commands.Bot(command_prefix='!', intents=intents)

conn = sqlite3.connect('database.db')
conn.execute("CREATE TABLE IF NOT EXISTS news (title TEXT NOT NULL)")
conn.close()
conn = sqlite3.connect('database.db')
conn.execute("DROP TABLE youtube")
conn.commit()
conn.execute("CREATE TABLE IF NOT EXISTS youtube (title TEXT NOT NULL)")

conn.close()

@tasks.loop(seconds=30)
async def checkforvideos():
 for video in videos:
     title = video['title']['runs'][0]['text']
     link = "https://www.youtube.com/watch?v=" + video['videoId']
     conn = sqlite3.connect('database.db')
     row = conn.execute("SELECT * from youtube  WHERE title = '{}'".format(title))
     target = row.fetchall()
     if len(target) == 0:
         conn.execute("INSERT into youtube Values ('{}')".format(title))
         conn.commit()
         youtubechannel = await bot.fetch_channel(youtubechannelid)
         guild = await bot.fetch_guild(guildid)
         await youtubechannel.send(f""" Hey {guild.default_role} **{title}** \n {link}""")
     conn.close()


@tasks.loop(seconds=300)
async def news():
    news = stockmarket()
    crypto = cryptocurrency()
    eco = economy()
    conn = sqlite3.connect('database.db')
    for new in news:
        try:
            row = conn.execute("SELECT * from news  WHERE title = '{}'".format(new['title']))

            target = row.fetchall()


            if len(target) == 0:
                conn.execute("INSERT into news Values ('{}')".format(new['title']))
                conn.commit()
                stockchannel = await bot.fetch_channel(stockchannelid)
                await stockchannel.send(f""" **{new['title']}** \n{new['link']}""")
        except:
            pass

    for new in crypto:
        try:
            row = conn.execute("SELECT * from news  WHERE title = '{}'".format(new['title']))
            target = row.fetchall()
            if len(target) == 0:
                conn.execute("INSERT into news Values ('{}')".format(new['title']))
                conn.commit()
                cryptochannel = await bot.fetch_channel(cryptochannelid)
                await cryptochannel.send(f""" **{new['title']}** \n{new['link']} """)
        except:
            pass


    for new in eco:
        try:
            row = conn.execute("SELECT * from news  WHERE title = '{}'".format(new['title']))
            target = row.fetchall()
            if len(target) == 0:
                conn.execute("INSERT into news Values ('{}')".format(new['title']))
                conn.commit()
                economychannel = await bot.fetch_channel(economychannelid)
                await economychannel.send(f""" **{new['title']}** \n{new['link']}""")
        except:
            pass

    conn.close()

@bot.event
async def on_ready():

    print(f'{bot.user} has connected to Discord!')


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )
    await update_member_count_channel_name(member.guild)


@bot.event
async def on_member_remove(member):
    """ gets triggered when a new member leaves or gets removed from a guild """
    print(f"* {member} left {member.guild}")
    await update_member_count_channel_name(member.guild)


@bot.command(name="update")
async def on_update_cmd(ctx):
    """ triggers manual update of member count channel """
    print(f"* {ctx.author} issued update")
    await update_member_count_channel_name(ctx.guild)


async def update_member_count_channel_name(guild):
    """ updates the name of the member count channel """
    member_count_channel_id = get_guild_member_count_channel_id(guild)
    member_count_praefix = get_guild_member_count_praefix(guild)

    if member_count_channel_id != None and member_count_praefix != None:
        member_count_channel = discord.utils.get(guild.channels, id=member_count_channel_id)
        new_name = f"{member_count_praefix} {get_guild_member_count(guild)}"
        if member_count_channel.name != new_name:
            await member_count_channel.edit(name=new_name)

    else:
        print(f"* could not update member count channel for {guild}, id not found in {JSON_FILE}")


def get_guild_member_count(guild):
    """ returns the member count of a guild """
    return len(guild.members)


def get_guild_member_count_channel_id(guild):
    """ returns the channel id for the channel that should display the member count """
    with open(JSON_FILE) as json_file:
        # open JSON file
        data = json.load(json_file)
        for data_guild in data['guilds']:
            if int(data_guild['id']) == guild.id:
                return data_guild['channel_id']

            return None


def get_guild_member_count_praefix(guild):
    """ returns the the praefix that should be displayed after the member count """
    with open(JSON_FILE) as json_file:
        # open JSON file
        data = json.load(json_file)
        for data_guild in data['guilds']:
            if int(data_guild['id']) == guild.id:
                return data_guild['praefix']

            return None


if __name__ == "__main__":

    checkforvideos.start()
    news.start()
    bot.run("TOKEN")
