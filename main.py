import logging
from discord.ext import commands
from discord import Intents
import internal_functions as ifunc
import os
from token import token

logging.basicConfig(filename = "bot.log",
                    filemode = 'a',
                    format = '[%(asctime)s.%(msecs)d] [%(levelname)s] [%(name)s] %(message)s',
                    datefmt = '%Y%m%d %H%M%S',
                    level = logging.WARN)

bot = commands.Bot(command_prefix = "mib!", 
                   intents = Intents.default(),
                   owner_id = 233018119856062466)

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

bot.run(token)