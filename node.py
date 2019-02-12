from utility.verification import Verification
from blockchain import Blockchain
from uuid import uuid4
from wallet import Wallet


class Node:

    def __init__(self):
        # self.id = str(uuid4())
        self.wallet = Wallet()
        self.wallet.create_keys()
        self.blockchain = Blockchain(self.wallet.public_key)
    
    
    def print_blockchain_elements(self):
        '''Output all blocks of the chain'''
        for block  in self.blockchain.chain:
            print('Outputting Block')
            print("This is the BLOCK:  ", block)
        else:
            print('-'*20)


    def get_user_choice(self):
        '''Prompts the user for their input and returns it'''
        user_input = input('Your Choice: ')
        
        return user_input
    
    def get_transaction_value(self):
        '''Returns transaction amount as inputted by user, 
        as a float'''
        tx_recipient =  input('Enter the recipient of the transaction: ')
        tx_amount = float(input('The transaction amount please: '))
        
        return tx_recipient, tx_amount


    def listen_for_input(self):
        #Start of main while loop for user input 
        #Initialize variable
        waiting_for_input = True

        while waiting_for_input:
            print('Please Choose')
            print('1: Add a new transaction amount')
            print('2: Mine a new block')
            print('3: Output the blockchain blocks')
            print('4: Check transaction validity')    
            print('5: Create a wallet')
            print('6: Load your wallet')
            print('7: Save Keys')
            print('q: Quit')
            user_choice = self.get_user_choice()
            if user_choice == '1':
                tx_data = self.get_transaction_value()
                recipient, amount = tx_data 
                signature = self.wallet.sign_transaction(
                    self.wallet.public_key,
                    recipient,
                    amount 
                )
                if self.blockchain.add_transaction(recipient, self.wallet.public_key, signature, amount=amount):
                    print('Added transaction')
                else:
                    print('Transaction failed')
                print (self.blockchain.get_open_transactions())
            elif user_choice == '2':
                 if not self.blockchain.mine_block():
                     print('Mining failed. Go no Wallet!?')
            
            elif user_choice == '3':
                self.print_blockchain_elements()
            
            elif user_choice == '4':
                if Verification.verify_transactions(self.blockchain.get_open_transactions, self.blockchain.get_balance):
                    print('All transactions are valid')
                else:
                    print('Invalid transactions found')
            
            elif user_choice == '5':
                self.wallet.create_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            
            elif user_choice == '6':
                self.wallet.load_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif user_choice == '7':
                self.wallet.save_keys()
            elif user_choice == 'q':
                waiting_for_input = False
                
            else:
                print('Input was invalid, please pick a value from the list..')
            
            if not Verification.verify_chain(self.blockchain.chain):
                self.print_blockchain_elements()
                print('Invalid blockchain!!')
                break
            print('The balance of {} is currently: {:6.2f}'.format(self.wallet.public_key, self.blockchain.get_balance()))
        else:
            print('User left..!')
        print('Done!!')

if __name__ == '__main__':
    node = Node()
    node.listen_for_input()