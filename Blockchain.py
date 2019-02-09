blockchain = []
open_transactions = []
owner = 'Eugene'

def get_last_bc_value():
    '''Returns the last val ue in the blockchain'''
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(recipient, sender=owner, amount=1.0):
    '''Append new value and the last blockchain value to the blockchain list
        Arguments:
            sender: Sender of the coins
            recipient: Receiver of the coins
            amount: Amount of the transactio'''
    transaction = {
        'sender': sender, 
        'recipient': recipient, 
        'amount': amount}    
    open_transactions.append(transaction)


def mine_block():
    pass


def get_transaction_value():
    '''Returns input of user(transaction amount) 
    as a float'''
    tx_recipient =  input('Enter the recipient of the transaction: ')
    print(type(tx_recipient))
    tx_amount = float(input('The transaction amount please: '))
    print(type(tx_amount))
    return (tx_recipient, tx_amount)


def print_blockchain_elements():
    '''Output all blocks of the chain'''
    for block  in blockchain:
        print('Outputting Block')
        print(block)
    else:
        print('-'*20)


def get_user_choice():
    '''Prompts the user for their input and returns it'''
    user_input = input('Your Choice: ')
    return user_input


def verify_chain():
    '''Verify the current blockchain and return True if valid, False otherwise'''
    is_valid = True
    for block_index in range(len(blockchain)):
        if block_index == 0:
            continue
        elif block_index[block_index][0] == blockchain[block_index-1]:
            is_valid = True
        else:
            is_valid = False
        return is_valid

waiting_for_input = True

while waiting_for_input:
    print('Please Choose')
    print('1: Add a new transaction amount')
    print('2: Output the blockchain blocks')
    print('h: Manipulate the chain')
    print('q: Quit')
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_data = get_transaction_value()
        recipient, amount = tx_data 
        add_transaction(recipient, amount=amount)
        print(open_transactions)
    elif user_choice == '2':
        print_blockchain_elements()
    elif user_choice == 'h':  
        if len(blockchain) >= 1:
            blockchain[0] = [2]
    elif user_choice == 'q':
        waiting_for_input = False
        break
    else:
        print('Input was invalid, please pick a value from the list..')
    print('Choice registered')

print('Done!!')

