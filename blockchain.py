from functools import reduce
import hashlib as hl
import json
import pickle
from hash_util import hash_block
from block import Block
from transaction import Transaction
from verification import Verification

MINING_REWARD = 10

class Blockchain:
    def __init__(self, hosting_node):
        #Genesis Block
        genesis_block = Block(0, '', [], 100)
        #Initializing open_transactions and blockchain
        self.__chain = [genesis_block]
        self.__open_transactions = []
        self.load_data()
        self.hosting_node = hosting_node
    

    #Funtion declarations
    def get_chain(self):
        return self.__chain[:]
    
    def get_open_transactions(self):
        return self.__open_transactions[:]
        
    def load_data(self):
        try:
            with open('blockchain.txt', mode='r') as f:
                # file_content = pickle.loads(f.read())
                file_content = f.readlines()
                # blockchain = file_content['chain']

                # open_transactions = file_content['ot']
                blockchain = json.loads(file_content[0][:-1])
                #Updating the blockchain
                updated_blockchain = []
                for block in blockchain:
                    converted_tx= [Transaction(
                        tx['sender'],
                        tx['recipient'],
                        tx['amount']
                    ) for tx in block['transactions']]

                    # converted_tx =  [OrderedDict(
                    # [('sender', block['sender']),
                    # ('recipient', block['recipient']),
                    # ('amount', block['amount'])])\
                    # for tx in block['transactions']]
                    
                    updated_block = Block(
                    block['index'],
                    block['previous_hash'],
                    converted_tx,
                    block['proof'],
                    block['timestamp'])
                    
                    updated_blockchain.append(updated_block)
                
                self.__chain = updated_blockchain
                #Updating the open_transactions
                self.__open_transactions = json.loads(file_content[1])
                updated_transactions = []
                for tx in open_transactions:
                    updated_transaction = Transaction(
                        tx['sender'],
                        tx['recipient'],
                        tx['amount'])

                    # updated_transaction = OrderedDict(
                    #     [('sender', tx['sender']),
                    #     ('recipient', tx['recipient']),
                    #     ('amount', tx['amount'])])

                    updated_transactions.append(updated_transaction)
                self.__open_transactions = updated_transactions
        except:
            # blockchain = [genesis_block]
            # open_transactions = []
            print('Error loading data')
    

    def save_data(self):
        '''Saves data to the specified file'''
        try:
            with open('blockchain.txt', mode='w') as f:
                saveable_chain = [block.__dict__ for block in [Block(
                    block_el.index,
                    block_el.previous_hash,
                    [tx.__dict__ for tx in block_el.transactions],
                    block_el.proof,
                    block_el.timestamp) for block_el in self.__chain]]
                
                f.write(json.dumps(saveable_chain))
                f.write('\n')
                saveable_tx = [block.__dict__ for tx in self.__open_transactions]
                f.write(json.dumps(saveable_tx))
                
                # save_data = {
                #     'chain': blockchain,
                #     'ot': open_transactions
                # }
                # f.write(pickle.dumps(save_data))
        except:
            print('Loading Blockchain data failed')

    def proof_of_work(self):
        '''Set the `proof` value and, checks the validity of the current proof value.
            Returns `proof` if POW criteria is met.'''

        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        proof  = 0 
        
        while not Verification.valid_proof(self.__open_transactions, last_hash, proof):
            proof += 1
        return proof


    def get_balance(self):
        '''Returns the current balance for the given participent'''
        participant = self.hosting_node
        tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant] for block in self.__chain]
        open_tx_sender = [tx.amount for tx in self.__open_transactions if tx.sender == participant]
        tx_sender.append(open_tx_sender)
        amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt)\
            if len(tx_amt) > 0 else tx_sum + 0,tx_sender,0)
        
        tx_recipient = [[tx.amount for tx in block.transactions
                         if tx.recipient == participant] for block in self.__chain]
        amount_received = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt)\
            if len(tx_amt) > 0 else tx_sum + 0,tx_recipient,0)
        return amount_received - amount_sent

    def get_last_bc_value(self):
        '''Returns the last value in the blockchain'''

        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]

    def add_transaction(self, recipient, sender, amount=1.0):
        '''Append new transaction value to the last blockchain value.
            Adds sender and recipient to participents 
            to the blockchain list
                Arguments:
                    sender: Sender of the coins
                    recipient: Receiver of the coins
                    amount: Amount of the transaction'''
        transaction = Transaction(sender, recipient, amount)
        # transaction = OrderedDict([
        #     ('sender', sender),
        #     ('recipient', recipient),
        #     ('amount', amount)
        #     ])
        
        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            self.save_data()
            # participants.add(sender)
            # participants.add(recipient)
            return True
        
        return False

    def mine_block(self):
        '''Mining function to add new block to the 
            blockchain, and generate the 
             transaction
            after executing proof_of_work()
        '''
        last_block = self.__chain[-1]

        hashed_block = hash_block(last_block)
        print("This is the HASHED_BLOCK", hashed_block)
        proof = self.proof_of_work()
        reward_transaction = Transaction('MINING', self.hosting_node, MINING_REWARD)
        # reward_transaction = OrderedDict([
        #     ('sender', 'MINING'),
        #     ('recipient', owner),
        #     ('amount', MINING_REWARD)
        # ])
        
        copied_transactions = self.__open_transactions[:]
        copied_transactions.append(reward_transaction)
        block = Block(len(self.__chain),hashed_block, 
                copied_transactions, proof)    
        
        self.__chain.append(block)
        self.__open_transactions = []
        self.save_data()
        return True