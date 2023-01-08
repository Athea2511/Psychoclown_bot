import discord
from discord import slash_command
from discord.commands import Option
from discord.ext import commands


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Modul: Commands geladen!")

    @slash_command()
    @discord.default_permissions(administrator=True)
    @discord.guild_only()
    async def activity(self, ctx,
                       typ: Option(str, choices=["game", "stream"]),
                       name: Option(str)
                       ):
        if typ == "game":
            act = discord.Game(name=name)
        else:
            act = discord.Streaming(
                name=name,
                url='https://www.twitch.tv/psychoclown97'
            )
        await self.bot.change_presence(activity=act, status=discord.Status.online)
        await ctx.respond("Status wurde geändert!")


def setup(bot):
    bot.add_cog(Commands(bot))
