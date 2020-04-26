from blackjack.account import Account
from blackjack.deckofcards import DeckOfCards

# Move this file to one folder up and run on termional: {python bjack.py}
#                          OR
# remove package blackjack. above * and __init__.py in the dir to run in terminal ^ 

class BlackJack():

    def __init__(self):
        self.player = Account('kalaLokia')
        self.cards = DeckOfCards()
        self.playershand = []
        self.dealershand = []
        self.action = ''
        self.blackjack = False


    def showCards(self,items, name):
        '''
        Shows {name}'s cards and hand value
        '''
        return f"{name}'s hand: \n{' - '.join(items)}\nHand value: {self.cards.handValue(items)}"


    def bust(self,hand):
        '''
        Whether a someone has busted or not
        '''
        if(self.cards.handValue(hand) > 21):
            return True
        return False


    def dealersMove(self):
        '''
        Dealers move: executes when player calls "stand"
        Dealer perform hit until he gets bust, wins or his hand value becomes >= 17
        When hand value is >17 and players has greater value, dealer loses ;-)
        '''
  
        if(self.cards.handValue(self.dealershand) == 21):
            return 'Dealer got a BLACKJACK\nDealer WINS'       

        elif(self.blackjack):
            self.blackjack = False
            return f'{self.player.name} got a BLACKJACK\n{self.player.name} WINS' 

        while(not self.bust(self.dealershand)):

            if(self.cards.handValue(self.dealershand) > self.cards.handValue(self.playershand)):      
                return 'Dealer WINS!\n' + self.showCards(self.dealershand, 'Dealer')
                
            elif(self.cards.handValue(self.dealershand) == self.cards.handValue(self.playershand)):
                return "It's a TIE!!\n Dealer WINS"
                
            elif(self.cards.handValue(self.dealershand) > 17):
                s1 = f'Dealer loses\n{self.player.name} has WON.\n'
                return s1 + f'{self.cards.handValue(self.playershand)} > {self.cards.handValue(self.dealershand)}'       

            self.dealershand.append(self.cards.hit())
        else:
            return f'Dealer busts! \n{self.player.name} has WON the game.'


if __name__ == "__main__":   

    print('Welcome to BlackJack Game')
    # Tell game rules here, may be
    response = input('Do you want to start the game (Y/n)? ').lower()
    if(response != 'y'):
        play = False
        print('You have been exited the game')
    else:
        play = True
    # Ask for bet amount later
    while(play):
        bj = BlackJack()
        bj.cards.shuffle()
        print('Cards on the table is now shuffled\n')
        bj.playershand = list(bj.cards.initiate())
        bj.dealershand = list(bj.cards.initiate())
        r1 = f"{bj.player.name}'s hand:\n   {bj.playershand[0]} - {bj.playershand[1]}\nHand value: {bj.cards.handValue(bj.playershand)}\n"
        r2 = f"\nDealer's hand:\n   {bj.dealershand[0]} - ?\n"
        print(r1+r2)
        # Game starts now
        if(bj.cards.handValue(bj.playershand) == 21): 
            # If player got black jack, no need to wait for a response.
            # Checks dealer's card and send the result
            bj.blackjack = True
            print(bj.dealersMove())
            if(input('Do you want to play again (Y/n)?').lower() != 'y'):
                print('The End')
                play = False
                break
            else:
                continue
            
        while(not bj.bust(bj.playershand)):
            # While player is not got busted, wait for his response action
            action = input(f"{bj.player.name}'s turn: Do you want to hit or stand ? ").lower()
        
            if(action == 'hit'):
                bj.playershand.append(bj.cards.hit())
                print(bj.showCards(bj.playershand, bj.player.name))
            elif(action == 'stand'):
                print(bj.dealersMove())
                break
            else:
                print('Please enter a valid action !')
        else:
            print(f'{bj.player.name} has been BUSTED')

        # Asks if player wanna play again or not
        if(input('Do you want to play again (Y/n)?').lower() != 'y'):
            print('The End')
            play = False