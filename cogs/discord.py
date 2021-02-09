import discord
import datetime

from discord.ext import commands
from io import BytesIO


class DiscordCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="avatar", aliases=["pp"], brief="donne l'avatar")
    @commands.guild_only()
    async def get_avatar(self, ctx, *, user: discord.Member = None):
        """ Donne ton avatar ou celui de quelqu'un """
        user = user or ctx.author
        await ctx.send(f"Avatar de **{user.name}**\n{user.avatar_url_as(size=1024)}")

    @commands.command(name="roles", aliases=["role"], brief="Donne tous les roles du serveur")
    @commands.guild_only()
    async def get_role(self, ctx):
        """ Donne tous les roles du serveur """
        allRoles = ""
        for num, role in enumerate(sorted(ctx.guild.roles, reverse=True), start=1):
            allRoles += f"[{str(num).zfill(2)}] {role.id}\t{role.name}\t [ Membre: {len(role.members)}]\r\n"

        data = BytesIO(allRoles.encode('utf-8'))
        await ctx.send(
            content=f"Roles dans **{ctx.guild.name}**",
            file=discord.File(data, filename=f"Roles_{datetime.datetime.now().strftime('%d-%m-%Y')}.txt")
        )

    @commands.command(name="server", brief="Donnes les statistiques du serveur")
    @commands.guild_only()
    async def server_info(self, ctx):
        """ Donne les infos du serveur Discord """
        if ctx.invoked_subcommand is None:
            findBots = sum(1 for member in ctx.guild.members if member.bot)
            embed = discord.Embed()

            if ctx.guild.icon:
                embed.set_thumbnail(url=ctx.guild.icon_url)
            if ctx.guild.banner:
                embed.set_thumbnail(url=ctx.guild.banner_url_as(format="png"))

            embed.add_field(name="Nom du Serveur", value=ctx.guild.name, inline=True)
            embed.add_field(name="ID Serveur", value=ctx.guild.id, inline=True)
            embed.add_field(name="Membre", value=ctx.guild.member_count, inline=True)
            embed.add_field(name="Bots", value=findBots, inline=True)
            embed.add_field(name="Propriétaire", value=ctx.guild.owner, inline=True)
            embed.add_field(name="Région", value=ctx.guild.region, inline=True)
            embed.add_field(name="Crée", value=ctx.guild.created_at.strftime('%d-%m-%Y'), inline=True)
            await ctx.send(content=f"ℹ information sur **{ctx.guild.name}**", embed=embed)

    @commands.command(name="member", brief="Donne le nombre de membre du serveur")
    @commands.guild_only()
    async def members_count(self, ctx):
        """ Donne le nombre de membre du serveur Discord """
        findBots = sum(1 for member in ctx.guild.members if member.bot)
        await ctx.send(f"IL y a {ctx.guild.member_count - findBots} membres biologique dans notre serveur")

    @commands.command(name="avatar_server", aliases=["icon", "avserver"], brief="Donne l'avatar du serveur")
    @commands.guild_only()
    async def avatar_server(self, ctx):
        """ Donne l'avatar du serveur Discord """
        await ctx.send(f"Bannière de **{ctx.guild.name}**\n{ctx.guild.banner_url_as(format='png')}")

    @commands.command(name="user", brief="Donne les informations de l'user")
    @commands.guild_only()
    async def user(self, ctx, *, user: discord.Member = None):
        """ Donne les informations de l'utilisateur """
        user = user or ctx.author

        showRoles = ", ".join(
            [f"<@&{i.id}>" for i in sorted(user.roles, key=lambda i: i.position, reverse=True) if i.id != ctx.guild.default_role.id]
        ) if len(user.roles) > 1 else "None"

        embed = discord.Embed(colour=user.top_role.colour.value)
        embed.set_thumbnail(url=user.avatar_url)

        embed.add_field(name="Nom complet", value=user, inline=True)
        embed.add_field(name="Pseudo", value=user.nick if hasattr(user, "nick") else "None", inline=True)
        embed.add_field(name="Compte crée", value=user.created_at.strftime('%d-%m-%Y'), inline=True)
        embed.add_field(name="Rejoin le serveur", value=user.joined_at.strftime('%d-%m-%Y'), inline=True)
        embed.add_field(name="Roles", value=showRoles, inline=True)
        await ctx.send(content=f"ℹ Sur **{user.id}**", embed=embed)


def setup(client):
    client.add_cog(DiscordCommand(client))
