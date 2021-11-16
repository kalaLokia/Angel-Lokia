import discord
from discord.ext import commands

import blackjack.bjack as bjack


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def games(self, ctx):
        await ctx.send("Category games now available")

    def check(self, author):
        def inner_check(message):
            return message.author == author

        return inner_check

    @commands.command(name="bk", help="Blackjack Game")
    async def on_blackjack(self, ctx):
        await ctx.send("Welcome to BlackJack Game")
        # Tell game rules here, may be
        await ctx.send("Do you want to start the game (Y/n):")
        response = await self.bot.wait_for(
            "message", check=self.check(ctx.author), timeout=60
        )
        if response.content.lower() != "y":
            play = False
            await ctx.send("You have been exited from the game")
        else:
            play = True
        # Ask for bet amount later
        while play:
            bj = bjack.BlackJack()
            bj.cards.shuffle()
            await ctx.send("Cards on the table is now shuffled\n")
            bj.playershand = list(bj.cards.initiate())
            bj.dealershand = list(bj.cards.initiate())
            r1 = f"{bj.player.name}'s hand:\n   {bj.playershand[0]} - {bj.playershand[1]}\nHand value: {bj.cards.handValue(bj.playershand)}\n"
            r2 = f"\nDealer's hand:\n   {bj.dealershand[0]} - ?\n"
            await ctx.send(r1 + r2)
            # Game starts now
            if bj.cards.handValue(bj.playershand) == 21:
                # If player got black jack, no need to wait for a response.
                # Checks dealer's card and send the result
                bj.blackjack = True
                await ctx.send(bj.dealersMove())

                await ctx.send("Do you want to play again (Y/n) ?")
                response = await self.bot.wait_for(
                    "message", check=self.check(ctx.author), timeout=60
                )
                if response.content.lower() != "y":
                    await ctx.send("Game End!")
                    play = False
                continue

            while not bj.bust(bj.playershand):
                # While player is not got busted, wait for his response action
                await ctx.send(
                    f"{bj.player.name}'s turn: Do you want to hit or stand ?"
                )
                response = await self.bot.wait_for(
                    "message", check=self.check(ctx.author), timeout=60
                )

                if response.content == "hit":
                    bj.playershand.append(bj.cards.hit())
                    await ctx.send(bj.showCards(bj.playershand, bj.player.name))
                elif response.content == "stand":
                    await ctx.send(bj.dealersMove())
                    break
                else:
                    await ctx.send("Please enter a valid action !")
            else:
                await ctx.send(f"{bj.player.name} has been BUSTED")
            # Asks if player wanna play again or not
            await ctx.send("Do you want to play again (Y/n) ?")
            response = await self.bot.wait_for(
                "message", check=self.check(ctx.author), timeout=60
            )
            if response.content.lower() != "y":
                await ctx.send("Game End!")
                play = False


def setup(bot):
    bot.add_cog(Games(bot))
