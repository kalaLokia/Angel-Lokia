import os
import random
import discord
import blackjack.bjack as bjack 

from dotenv import load_dotenv
from discord.ext import commands


load_dotenv()
token = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has got ALIVE!')

def check(author):
    def inner_check(message):
        return message.author == author
    return inner_check

# @bot.command(name='hello', help='Replies, Hi there!')
# async def on_msg(ctx):
#     await ctx.send('Hi there!')
#     msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=5)
#     print(msg.content)

@bot.command(name='test', help='Replies, Hi there!')
async def on_msg(kL):
    await kL.send('Hi there!')
    # msg = await bot.wait_for('message', check=check(ctx.author), timeout=30)
    # print(msg.content)

@bot.command(name='bj', help='Blackjack Game')
async def on_blackjack(self):
    await self.send('Welcome to BlackJack Game')
    # Tell game rules here, may be
    await self.send('Do you want to start the game (Y/n):')
    response = await bot.wait_for('message', check=check(self.author), timeout=60)
    if(response.content.lower()!='y'):
        play = False
        await self.send('You have been exited from the game')
    else:
        play = True
    # Ask for bet amount later
    while(play):
        bj = bjack.BlackJack()
        bj.cards.shuffle()
        await self.send('Cards on the table is now shuffled\n')
        bj.playershand = list(bj.cards.initiate())
        bj.dealershand = list(bj.cards.initiate())
        r1 = f"{bj.player.name}'s hand:\n   {bj.playershand[0]} - {bj.playershand[1]}\nHand value: {bj.cards.handValue(bj.playershand)}\n"
        r2 = f"\nDealer's hand:\n   {bj.dealershand[0]} - ?\n"
        await self.send(r1+r2)
        # Game starts now
        if(bj.cards.handValue(bj.playershand) == 21): 
            # If player got black jack, no need to wait for a response.
            # Checks dealer's card and send the result
            bj.blackjack = True
            await self.send(bj.dealersMove())
           
            await self.send('Do you want to play again (Y/n) ?')
            response = await bot.wait_for('message', check=check(self.author), timeout=60)
            if(response.content.lower() != 'y'):
                await self.send('Game End!')
                play = False
            continue
        
        while(not bj.bust(bj.playershand)):
            # While player is not got busted, wait for his response action
            await self.send(f"{bj.player.name}'s turn: Do you want to hit or stand ?")
            response = await bot.wait_for('message', check=check(self.author), timeout=60)

            if(response.content == 'hit'):
                bj.playershand.append(bj.cards.hit())
                await self.send(bj.showCards(bj.playershand, bj.player.name))
            elif(response.content == 'stand'):
                await self.send(bj.dealersMove())
                break
            else:
                await self.send('Please enter a valid action !')
        else:
            await self.send(f'{bj.player.name} has been BUSTED')
        # Asks if player wanna play again or not
        await self.send('Do you want to play again (Y/n) ?')
        response = await bot.wait_for('message', check=check(self.author), timeout=60)
        if(response.content.lower() != 'y'):
            await self.send('Game End!')
            play = False
        
bot.run(token)
