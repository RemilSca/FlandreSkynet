import os.path
import asyncio
import discord
from discord.ext import tasks
from saucenao_api import SauceNao

with open(f'api.txt', 'r') as f:
    api = f.read()

sauce = SauceNao(api)


intents = discord.Intents.default()
intents.messages = True
intents.members = True

from discord.ext import commands
bot = commands.Bot(command_prefix='%', intents=discord.Intents.all())




@bot.event
async def on_ready():
    print('Online')

    # guilg = await bot.fetch_guild(1092925838401486948)
    # bot.tree.copy_global_to(guild=guilg)
    # await bot.tree.sync(guild=guilg)
    guilg = await bot.fetch_guild(647798243207544842)
    bot.tree.copy_global_to(guild=guilg)
    await bot.tree.sync(guild=guilg)

@bot.event
async def on_message(ctx):
    await bot.process_commands(ctx)
    if ctx.author != bot.user:
        if isinstance(ctx.channel, discord.channel.DMChannel):
            pass

@bot.tree.command(name=f'ping', description=f'ping kurde')
async def ping(interaction: discord.Interaction) -> None:
    await interaction.response.send_message("ping")

@bot.command()
async def sauce(ctx):
    m = ctx.message.reference.resolved
    await m.fetch()
    x = m.embeds
    if(len(x)>0):
        for embed in x:
            results = sauce.from_url(embed.url)
            re = results.long_remaining
            best = results[0]
            await ctx.send(f'Remaining searches for 2day: {re}\nI am {best.similarity}% certain, it is {best.urls[0]}')
    else:
        for embed in m.attachments:
            results = sauce.from_url(embed.url)
            re = results.long_remaining
            best = results[0]
            await ctx.send(f'Remaining searches for 2day: {re}\nI am {best.similarity}% certain, it is {best.urls[0]}')


with open(f'token.txt', 'r') as f:
    token = f.read()


bot.run(token)

