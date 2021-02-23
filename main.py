import os
import discord
from discord.ext import commands, tasks
from discord import Intents
import os
import random
from data.secrets import secret
intents = Intents.all()

client = commands.Bot(
    command_prefix=">",
    allowed_mentions=discord.AllowedMentions(everyone=False, roles=False, users=True),
    intents=intents,
    case_sensitive=False,
)

@client.command(name="load")
async def load(ctx, extension):
    if ctx.author.id == 711444754080071714:
        try:
            client.load_extension(f'cogs.{extension.lower()}')
            await ctx.send(f"> <a:DC_verified2:749472983487217694> loaded {extension}!")
        except:
            await ctx.send(f"{extension} is either not loaded or is not there")
    else:
        await ctx.send("Are you donut?")

@client.command(name="unload")
async def unload(ctx, extension):
    if ctx.author.id == 711444754080071714:
        try:
            client.unload_extension(f'cogs.{extension.lower()}')
            await ctx.send(f"> <a:DC_verified2:749472983487217694> Unloaded {extension}!")
        except:
            await ctx.send(f"{extension} is either not loaded or is not there")
    else:
        await ctx.send("Are you donut?")

@client.command(name="reload")
async def reload(ctx):
    if ctx.author.id == 711444754080071714:
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                client.unload_extension(f'cogs.{filename[:-3]}')
                client.load_extension(f'cogs.{filename[:-3]}')
                print(f"Loaded {filename[:-3]}")

        await ctx.send(f"> <a:DC_verified2:749472983487217694> Reloaded all!")
    else:
        await ctx.send("Are you donut?")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        print(f"Loaded {filename[:-3]}")

@client.event
async def on_ready():
    print(f"Logged in as {client.user}!")
    change_status.start()

status = ['Jamming out to music', 'With Beer 🍻 ', 'Watching Donuts Café!!: https://discord.gg/xV98GwE', 'Minecraft', "Donut's Cafe Security!"]

@tasks.loop(seconds=20)
async def change_status():
    await client.change_presence(activity=discord.Game(random.choice(status)))

client.run(secret['token'])