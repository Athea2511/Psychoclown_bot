import discord
from discord import slash_command
from discord.commands import Option
from discord.ext import commands


class Userinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Modul: Userinfo geladen!")

    @slash_command(description="Zeige Infos über einen User", name="userinfo")
    @commands.cooldown(1, 30 * 60, commands.BucketType.user)
    async def info(
            self, ctx,
            user: Option(discord.Member, "Gib einen User an", default=None)
    ):
        if user is None:
            user = ctx.author

        embed = discord.Embed(
            title=f"Infos über{user.name}",
            description=f"Hier siehst du alle Details über{user.mention}",
            color=discord.Color.blue()
        )

        time = discord.utils.format_dt(user.created_at, "R")

        embed.add_field(name="Account erstellt", value=time, inline=False)
        embed.add_field(name="ID", value=user.id)
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.set_footer(text="das ist ein footer")

        await ctx.respond(embed=embed)

    @staticmethod
    def convert_time(seconds):
        if seconds < 60:
            return f"{round(seconds)} Sekunden"

        minutes = seconds / 60

        if minutes < 60:
            return f"{round(minutes)} Minuten"

        hours = minutes / 60

        if hours < 60:
            return f"{round(hours)} Stunden"

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            seconds = ctx.command.get_cooldown_retry_after(ctx)
            final = self.convert_time(seconds)
            await ctx.respond(f"Du must noch{final} warten", ephemeral=True)


def setup(bot):
    bot.add_cog(Userinfo(bot))
