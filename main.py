import os

import discord
from dotenv import load_dotenv

from Cogs import ListeID as IDs

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

status = discord.Status.dnd
activity = discord.Activity(type=discord.ActivityType.playing, name='Psychoclown_Boot |!help')

bot = discord.Bot(
    intents=intents,

    status=status,
    activity=activity
)

if __name__ == "__main__":
    for filename in os.listdir(r'Cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'Cogs.{filename[:-3]}')

    load_dotenv()
    bot.run(os.getenv("TOKEN"))


async def status_task():
    while True:
        await bot.change_presence(activity=discord.Game('Psychoclown_Boot |!help'))


@bot.event
async def on_ready():
    print(f"Wir sind eingeloggt als User {bot.user}")
    bot.loop.create_task(status_task())
    channel = bot.get_channel(IDs.Bot_sends_id)
    await channel.send('`BOT ONLINE`')
