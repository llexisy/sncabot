import discord
import json
import asyncio
import re

with open("config.json") as f:
    configjson = json.load(f)

TOKEN = configjson['token']
CHANNELS = configjson.get('channels', {})

def getrealdur(dur):
    match = re.fullmatch(r'(\d+)(s|m|h|d)', dur.strip())
    if not match:
        raise ValueError(f"error invalid dur: {dur}")
    value, unit = int(match.group(1)), match.group(2)
    return value * {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}[unit]

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

@bot.event
async def on_message(message):
    channel_id = str(message.channel.id)
    if channel_id in CHANNELS:
        delay = getrealdur(CHANNELS[channel_id])
        await asyncio.sleep(delay)
        try:
            await message.delete()
        except discord.NotFound:
            pass
        except discord.Forbidden:
            print(f"invalid perms {channel_id}")

bot.run(TOKEN)
