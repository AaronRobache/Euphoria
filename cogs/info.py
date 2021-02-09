import discord
import psutil
import os

from discord.ext import commands


class Information(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.process = psutil.Process(os.getpid())

    @commands.command(brief="Ping le serveur du client est renvoie une réponse")
    async def ping(self, ctx):
        """ Pong! """
        await ctx.send(f"Pong ! {round(self.client.latency * 1000)}ms")

    @commands.command(name='invite', brief='Donne une invitation pour le bot')
    async def invite_bot(self, ctx):
        """ Invite moi sur ton serveur """
        await ctx.send(
            f"**{ctx.author.name}**, utilise ce lien pour m'inviter\n<{discord.utils.oauth_url(self.client.user.id)}>"
        )

    @commands.command(name="source", aliases=["git", "github"],
                      brief="Donne le lien github du bot alias[git or github]")
    async def source_github(self, ctx):
        """ Permet de voir le code source du bot """
        await ctx.send(
            f"**{self.client.user.name}** voici mon source code\nhttps://github.com/AaronRobache/Euphoria"
        )

    @commands.command(name="info", aliases=["stats"], bief="Permet d'avoir les infos du serveur")
    async def info_server(self, ctx):
        """ Donne les info sur le le client """
        avgMembers = sum(guilds.member_count for guilds in self.client.guilds) / len(self.client.guilds)
        ramUsed = self.process.memory_full_info().rss / 1024 ** 2

        embedColour = discord.Embed.Empty
        if hasattr(ctx, "guild") and ctx.guild is not None:
            embedColour = ctx.me.top_role.colour

        embed = discord.Embed(colour=embedColour)
        embed.set_thumbnail(url=self.client.user.avatar_url)
        # embed.add_field(name='Dernier boot', value=f"{time.time() - psutil.boot_time()} min", inline=True)
        embed.add_field(name="Librairie", value="discord.py", inline=True)
        embed.add_field(name="Serveur", value=f"{len(self.client.guilds)} ( avg: {avgMembers:,.2f} user/server)",
                        inline=True)
        embed.add_field(name="Commande charger", value=len([x.name for x in self.client.commands]), inline=True)
        embed.add_field(name="RAM", value=f"{ramUsed:.2f} MB", inline=True)

        await ctx.send(content=f"ℹ About **{self.client.user}**", embed=embed)


def setup(client):
    client.add_cog(Information(client))
