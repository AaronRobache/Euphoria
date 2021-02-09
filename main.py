import discord
import os
import config

from discord.ext import commands

client = commands.Bot(
    command_prefix='!',
    description='Bot de Mahesvara le tous puissant !',
    case_insensitive=True,
    intents=discord.Intents(guilds=True, members=True, messages=True, reactions=True, presences=True)
)


@client.event
async def on_ready():
    """ Permet d'avoir log de connexion plus status de jeu """
    await client.change_presence(activity=discord.Game('Mahesvara mon maître ♥'))
    print(f'-----\nLogged in as: {client.user} : {client.user.id}\n-----')

# @client.command()
# async def load(ctx, extension):
#     client.load_extension(f'cogs.{extension}')

# @client.command()
# async def unload(ctx, extension):
#     client.unload_extension(f'cogs.{extension}')

# va chercher tous les cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

try:
    client.run(config.TOKEN_DISCORD)
except Exception as e:
    print(f'Error when logging in: {e}')
