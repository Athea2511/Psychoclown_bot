import discord
from discord.commands import slash_command, Option
from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Modul: admin geladen!")

    @slash_command(descripion="kicke einen Member")
    @discord.default_permissions(administrator=True, kick_members=True)
    @discord.guild_only()
    async def kick(self,
                   ctx,
                   member: Option(discord.Member, "wähle einen Member")):
        try:
            await member.kick()
        except discord.Forbidden as e:
            await ctx.respond("Ich habe keine Berechtigung um diesen Member zu kicken", ephemeral=True)
            return
        await ctx.respond(f"{member.mention} wurde erfolgreich gekickt", ephemeral=True)

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        raise error


def setup(bot):
    bot.add_cog(Admin(bot))
