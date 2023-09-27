import discord
import requests
import json
from weather import *

token = 'MTE1NjMxMDE4NzA5MTcwNTk0OQ.GOYQrr.UdCymBJmX5K8tOK5TjkN5U_cF_qf5qePzWw97Y'
api_key = '221d4acf2c0f08de4b905bc4d005742f'



intents = discord.Intents.default()

intents.message_content = True

client = discord.Client(intents=intents)
command_prefix = '!w'

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='!w [location]'))

@client.event
async def on_message(message):
    if message.author != client.user and message.content.startswith(command_prefix):
        if len(message.content.replace(command_prefix, '')) >= 1:
            location = message.content.replace(command_prefix, '').lower()
            url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric'
            try:
                data = parse_data(json.loads(requests.get(url).content)['main'])
                await message.channel.send(embed=weather_message(data, location))
            except KeyError:
                await message.channel.send(embed=error_message(location))

print("Bot has started running")
client.run(token)