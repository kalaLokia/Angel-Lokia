import os

import discord
from discord.ext import commands, tasks

from core import settings
from core.permissions import bot_perms


intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=".", intents=intents)
cmdlist = []


def refresh_cogs():
    cmdlist.clear()
    # Saving all cogs names to array {listcmd}
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            cmdlist.append(filename[:-3])


refresh_cogs()
activecmd = cmdlist.copy()
for filename in activecmd:
    bot.load_extension(f"cogs.{filename}")


@bot.event
async def on_ready():
    print(f"{bot.user.name} has got ALIVE!")
    change_status.start()  # Changes her status


@tasks.loop(minutes=3)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(bot_perms.cycle_bot_status)))


@bot.command(aliases=["f5"])
async def refresh(ctx, extension=""):
    if await bot.is_owner(ctx.author):
        refresh_cogs()
        await ctx.send(f"system refreshed ({len(cmdlist)} cogs)")


@bot.command()
async def load(ctx, extension=""):
    if await bot.is_owner(ctx.author):
        if len(cmdlist) == len(activecmd):
            await ctx.send("There is nothing new to load!")
            return
        if extension == "all":
            for filename in cmdlist:
                try:
                    bot.load_extension(f"cogs.{filename}")
                except:
                    # reload in this case
                    print(f"EXCEPTION : Extension {filename} already loaded")
            await ctx.send(f"All extensions loaded! [total : {len(cmdlist)}].")

        elif extension not in cmdlist:
            await ctx.send(
                "That is not a valid extension, all available extensions are: "
            )
            for e in cmdlist:
                await ctx.send(f"`{e}\n`")
        elif extension in activecmd:
            bot.unload_extension(f"cogs.{extension}")
            bot.load_extension(f"cogs.{extension}")
            await ctx.send(f"Extension `{extension}` reloaded.")
        else:
            bot.load_extension(f"cogs.{extension}")
            activecmd.append(extension)
            await ctx.send(f"Extension `{extension}` loaded.")


@bot.command()
async def unload(ctx, extension=""):
    if await bot.is_owner(ctx.author):
        global activecmd
        count = len(activecmd)
        if count < 1:
            await ctx.send(f"There is nothing to unload!")
            return
        if extension == "all":

            for filename in activecmd:
                try:
                    bot.unload_extension(f"cogs.{filename}")
                except:
                    print(
                        f"EXCEPTION : Extension {filename} not even loaded yet to unload"
                    )
            activecmd = []
            await ctx.send(f"{count} extensions unloaded.")

        elif extension not in activecmd:
            await ctx.send(
                "I don't see that extension loaded yet, all active extensions are: "
            )
            for e in activecmd:
                await ctx.send(f"`{e}\n`")
        else:
            bot.unload_extension(f"cogs.{extension}")
            activecmd.remove(extension)
            await ctx.send(f"Extension `{extension}` unloaded.")


@bot.command()
async def reload(ctx, extension=""):
    if await bot.is_owner(ctx.author):
        if extension == "all":
            for filename in activecmd:
                try:
                    bot.unload_extension(f"cogs.{filename}")
                except:
                    print(
                        f"EXCEPTION : Extension {filename} not even loaded yet to unload"
                    )
                bot.load_extension(f"cogs.{filename}")
            await ctx.send(f"{len(activecmd)} extensions reloaded.")

        elif extension not in activecmd:
            await ctx.send(
                "I don't see that extension loaded yet, all active extensions are: "
            )
            for e in activecmd:
                await ctx.send(f"```{e}\n```")
        else:
            bot.unload_extension(f"cogs.{extension}")
            bot.load_extension(f"cogs.{extension}")
            await ctx.send(f"Extension `{extension}` reloaded.")


# def check(author):
#     def inner_check(message):
#         return message.author == author
#     return inner_check

# # Error handling
# @bot.event
# async def on_error(ctx, error):
#     if isinstance(error, commands.MissingPermissions):
#         await ctx.send('Missing permisions ..')
#     elif isinstance(error, commands.MissingRole):
#         await ctx.send('Missing roles ..')


if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_TOKEN"))
