blockchain = [[1]]

def get_last_bc_value():
    return blockchain[-1]

def add_value(transaction_amount, last_transaction=[1]):
    blockchain.append([last_transaction,transaction_amount, ])
    

add_value(2)
add_value(0.9, get_last_bc_value())
add_value(10.98, get_last_bc_value())
print(blockchain)
