from discord.ext import commands


class Welcome(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """ Quand un membre rejoin le serveur """
        channel = member.guild.system_channel

        emoji1 = self.client.get_emoji(780425153187545090)
        emoji2 = self.client.get_emoji(780425166748385301)

        await channel.send(f"{emoji1}{emoji2}")
        await channel.send(f"{member.mention} Bienvenue sur le serveur {member.guild.name}")


def setup(client):
    client.add_cog(Welcome(client))
