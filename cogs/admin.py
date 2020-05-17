import discord
from discord.ext import commands
from bot import lokia

class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    

    @commands.command()
    async def admin(self,ctx):
        await ctx.send('Admin commands are available')

    @commands.command()
    @commands.check(lokia)
    # @commands.has_permissions(manage_messages=True)
    async def clear(self,ctx, count:int):
        if(count > 0 and count < 101):
            await ctx.channel.purge(limit=count+1)
    @clear.error
    async def clear_err(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('You need to be a Lokia Family member to use this command')
            # await ctx.send('Please specify the amount of msg to delete.')

    # @commands.command()
    # @commands.has_permissions(kick_members=True)
    # async def kick(self,ctx, member : discord.Member, *, reason=None):
    #     await member.kick(reason=reason)

    # @commands.command()
    # @commands.has_permissions(ban_members=True)
    # async def ban(self,ctx, member : discord.Member, *, reason=None):
    #     await member.ban(reason=reason)
    #     await ctx.send(f'Banned {member.mention}')

    # @commands.command()
    # @commands.has_permissions(unban_members=True)
    # async def unban(self,ctx, *, member):
    #     banned_users = await ctx.guild.bans() 
    #     member_name,member_discr = member.split('#')

    #     for banned_user in banned_users:
    #         user = banned_user.user
    #         print(f'Descriminatorrrrr  :: {user.discriminator}')
    #         if (user.name, user.discriminator) == (member_name,member_discr):
    #             await ctx.guild.unban(user)
    #             await ctx.send(f'Unbanned {user.mention}')
    #             return
    #     else:
    #         await ctx.send(f"I don't see the user {member_name}#{member_discr} in banned list.")
    #         return


def setup(bot):
    bot.add_cog(Admin(bot))