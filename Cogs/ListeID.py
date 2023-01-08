from discord.ext import commands


class IDs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Modul: IDs geladen!")


# Channel
Live_channel_id = 756162155056857263
Stream_channel_id = 756162155056857263
warteraum_stream_id = 756163961430474882
Bot_sends_id = 756180632777916537
# Channel

# Group, Guilds, Message, Client
Server_Guild_id = 756162155056857258
Regel_message_id = 1054365293234901032
Bot_Client_id = 756176227441705000
# Group, Guilds, Message, Client

# Roles
BotMod_role_id = 756180660359659580
Verified_role_id = 808380196663066685
New_Member = 756192056811978864
Level5_role_id = 756192826118635661
Level4_role_id = 756193204348518462
Level3_role_id = 756191153195450419
Level2_role_id = 756191365179900024
Level1_role_id = 756189792089145444
Level0_role_id = 756192056811978864
All_rights_id = 756162476743065661


# Roles

def setup(bot):
    bot.add_cog(IDs(bot))
