import configuration as conf
from discord import Intents
from discord.ext import commands
import internal_functions as ifunc
import logging
import os

logging.basicConfig(filename = conf.log_filename,
                    filemode = 'a',
                    format = conf.log_format,
                    datefmt = conf.log_dateformat,
                    level = logging.WARN)

bot = commands.Bot(command_prefix = conf.bot_prefix, 
                   intents = Intents.default(),
                   owner_id = conf.bot_owner)

# Admin commands
@bot.command()
async def loglevel(ctx, arg):
    if commands.is_owner():
        ifunc.change_log_level(arg)
        await ctx.send("Log level changed to " + arg)

@bot.command()
async def eval(ctx, arg):
    if commands.is_owner():
        exitCode = await os.system(arg)
        ctx.send(f"Evaluated: `{arg}`\n" +
                 f"Exit code: `{exitCode}`")

# User commands
@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong {round(bot.latency * 1000)}ms")

bot.run(os.environ['mibtoken'])