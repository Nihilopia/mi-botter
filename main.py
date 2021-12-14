import configuration as conf
import discord
from discord import Intents, Forbidden
from discord.ext import commands
import internal_functions as ifunc
import logging
import os
import weatherstack

discord.Intents.guilds = True

logging.basicConfig(filename = conf.log_filename,
                    filemode = 'a',
                    format = conf.log_format,
                    datefmt = conf.log_dateformat,
                    level = logging.WARN)

bot = commands.Bot(command_prefix = conf.bot_prefix, 
                   intents = Intents.default(),
                   owner_id = conf.bot_owner)

class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = weatherstack.Session(conf.weatherstack_key)

    # Admin commands
    @bot.command()
    async def loglevel(ctx, arg):
        if commands.is_owner():
            ifunc.change_log_level(arg)
            await ctx.send("Log level changed to " + arg)

    @bot.command()
    async def eval(ctx, arg):
        ctx.send("Eval command not implemented yet.")
        return
        if commands.is_owner():
            exitCode = await os.system(arg)
            ctx.send(f"Evaluated: `{arg}`\n" +
                        f"Exit code: `{exitCode}`")

    # User commands
    @bot.command()
    async def ping(ctx):
        await ctx.send(f"Pong {round(bot.latency * 1000)}ms")

    @bot.command()
    async def weather(ctx, *args):
        arg = " ".join(args)
        weather = weatherstack.get_current_weather(arg)
        if list(weather.keys())[0] == "successs":
            await ctx.send(f"Couldn't get weather data for {arg}")
        else:
            await ctx.send(f"Weather for **{weather['location']['name']}, {weather['location']['region']}, {weather['location']['country']}**:\n" + 
                            f"{weather['current']['weather_descriptions'][0]} at **{weather['current']['temperature']}°C**\n" +
                            f"Wind speed **{weather['current']['wind_speed']}km/h** ({weather['current']['wind_dir']})")

    @bot.event
    async def on_thread_join(thread: discord.Thread) -> None:
        announce_channel = [channel for channel in thread.parent.guild.channels if channel.id == 920405713782702125][0]
        try:
            announce_message_id = await announce_channel.send(f"{thread.mention} was created in {thread.parent.mention}")
            announce_message_id = announce_message_id.id
            ifunc.update_thread_info_json(thread, announce_message_id)
        except Forbidden:
            pass
        return
    
    @bot.event
    async def on_thread_delete(thread: discord.Thread) -> None:
        pass

    @bot.command()
    async def delete_all_threads(ctx):
        if ctx.guild.owner_id == conf.bot_owner:
            if commands.is_owner():
                threads = ctx.channel.threads
                for thread in threads:
                    await thread.delete()
                await ctx.send("All threads deleted.")
            else:
                await ctx.send("You are not allowed to use this command.")

    bot.run(os.environ["mibtoken"])
    
