import discord
from discord.ext import commands
import aiosqlite
from discord import slash_command
from Cogs import ListeID as IDs


class Level(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.DB = f"level.db"

    @staticmethod
    def get_level(xp):
        lvl = 1
        amount = 10

        while True:
            xp -= amount
            if xp < 0:
                print("LEVEL")
                return lvl

            lvl += 1
            amount *= 2.2   # level 1 10 level 2 32 level 3 81 level 4 187 level 5 422 level 6 937
            print(amount)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Modul: Level geladen!")
        async with aiosqlite.connect(self.DB) as db:
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS users(
                user_id INTEGER PRIMARY KEY, 
                msg_count INTEGER DEFAULT 0,
                xp INTEGER DEFAULT 0
                )
                """
            )

    async def check_user(self, user_id):
        async with aiosqlite.connect(self.DB) as db:
            await db.execute(
                "INSERT OR IGNORE INTO users(user_id) VALUES (?)", (user_id,)
            )
            await db.commit()

    async def get_xp(self, user_id):
        await self.check_user(user_id)
        async with aiosqlite.connect(self.DB) as db:
            async with db.execute("SELECT xp FROM users WHERE user_id = ?", (user_id,)) as cursor:
                result = await cursor.fetchone()

        return result[0]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if not message.guild:
            return

        await self.check_user(message.author.id)
        async with aiosqlite.connect(self.DB) as db:

            await db.execute(
                "UPDATE users SET msg_count = msg_count + 1, xp = xp + ? WHERE user_id = ?", (1, message.author.id)
            )
            await db.commit()

        # check level up
        new_xp = await self.get_xp(message.author.id)
        role0 = message.guild.get_role(IDs.New_Member)
        level = message.guild.get_role(IDs.Level0_role_id)
        level1 = message.guild.get_role(IDs.Level1_role_id)
        level2 = message.guild.get_role(IDs.Level2_role_id)
        level3 = message.guild.get_role(IDs.Level3_role_id)
        level4 = message.guild.get_role(IDs.Level4_role_id)
        level5 = message.guild.get_role(IDs.Level5_role_id)
        level6 = message.guild.get_role(IDs.Level6_role_id)
        lvl = self.get_level(new_xp)

        new_lvl = self.get_level(new_xp)
        old_lvl = self.get_level(new_xp - 1)

        if old_lvl == new_lvl:
            return

        if new_lvl == 2:  # Level 1 10xp
            await message.author.remove_roles(level)
            await message.author.add_roles(level1)
            await message.channel.send(f'<@{message.author.id}> Du bist nun Level **{lvl}**. Du bekommst:'
                                       f' **{level1.mention}**!')
        if new_lvl == 3:  # Level 2 32xp
            await message.author.add_roles(level2)
            await message.author.remove_roles(level1)
            await message.channel.send(f'<@{message.author.id}> Du bist nun Level **{lvl}**. Du bekommst:'
                                       f' **{level2.mention}**!')
        if new_lvl == 4:  # Level 3 81xp
            await message.author.add_roles(level3)
            await message.author.remove_roles(level2)
            await message.channel.send(f'<@{message.author.id}> Du bist nun Level **{lvl}**. Du bekommst:'
                                       f' **{level3.mention}**!')
        if new_lvl == 5:  # Level 4 187xp
            await message.author.add_roles(level4)
            await message.author.remove_roles(level3)
            await message.channel.send(f'<@{message.author.id}> Du bist nun Level **{lvl}**. Du bekommst:'
                                       f' **{level4.mention}**!')
        if new_lvl == 6:  # Level 5 422xp
            await message.author.add_roles(level5)
            await message.author.remove_roles(level4)
            await message.channel.send(f'<@{message.author.id}> Du bist nun Level **{lvl}**. Du bekommst:'
                                       f' **{level5.mention}**!')
        if new_lvl == 7:  # Level 6 937xp
            await message.author.add_roles(level6)
            await message.author.remove_roles(level5)
            await message.channel.send(f'<@{message.author.id}> Du bist nun Level **{lvl}**. Du bekommst:'
                                       f' **{level6.mention}**!')

    @slash_command()
    async def level(self, ctx):
        xp = await self.get_xp(ctx.author.id)
        lvl = self.get_level(xp)

        await ctx.respond(f"Du hast **{xp}** XP. Du bist Level {lvl}", ephemeral=True)

    @slash_command()
    async def rank(self, ctx):
        desc = ""
        counter = 1
        async with aiosqlite.connect(self.DB) as db:
            async with db.execute(
                    "SELECT user_id, xp FROM users WHERE msg_count > 0 ORDER BY xp DESC LIMIT 3"
            ) as cursor:
                async for user_id, xp in cursor:
                    desc += f"{counter}.<@{user_id}> - {xp} XP\n"
                    counter += 1

        embed = discord.Embed(
            title="Rangliste",
            description=desc,
            color=discord.Color.yellow()

        )
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Level(bot))
