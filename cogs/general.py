import discord
from discord.ext import commands
from core.permissions import bot_perms

from core.utils import generateProductionDates
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def general(self, ctx):
        await ctx.send("Category general now available")

    @commands.command()
    @commands.check(bot_perms.isAdmin)
    async def say(self, ctx, *, txt):
        # await ctx.channel.purge(limit=1)
        await ctx.send(txt)
        await ctx.message.delete()

    @say.error
    async def say_err(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("You need to be a Lokia family to use this command")

    @commands.command()
    @commands.check(bot_perms.isAdmin)
    async def pr(self, ctx, *, txt):
        # await ctx.channel.purge(limit=1)
        try:
            s = generateProductionDates(txt)
            await ctx.send(s)

        except Exception as e:
            logger.exception(e)
            await ctx.send(f"Error occured:\n {e}")

    @say.error
    async def pr_err(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("You need to be a Lokia family to use this command")


def setup(bot):
    bot.add_cog(General(bot))
