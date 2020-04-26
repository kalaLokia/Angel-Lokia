class Account():
    '''
    All it talks about account details of the player
    '''

    def __init__(self, name='Player'):
        '''
        Initializes a player with {name} and initial account balance 100
        '''
        self.bal = 100
        self.name = name

    def balance(self):
        '''
        To show player's available balance in account
        '''
        print(f'Available balance in your account: {self.bal} chips')
    
    def deposit(self, amount):
        '''
        To deposit chips to player account
        '''
        self.bal += amount
        print(f'{amount} chips has been deposited to your account.')

    def withdraw(self, amount):
        '''
        To withdraw {amount} of chips from player balance
        '''
        if(self.bal >= amount):
            self.bal -= amount
            # print(f'{self.bal} chips has been deducted from your account')
            return True
        print(f'Not sufficient balance in your account, available balance is {self.bal} chips')
        return False
    
