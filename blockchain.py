from functools import reduce
import hashlib as hl
from utility.hash_util import hash_block
from utility.verification import Verification
from block import Block
from transaction import Transaction
from wallet import Wallet


import json
import pickle
import requests
MINING_REWARD = 10
print(__name__)


class Blockchain:
    """Blockchain class

            Attributes:
                chain : List of all blocks
                
                open_transactions (private) : List of open transactions
                
                hosting_node : Connected nodes
    """

    def __init__(self, public_key, node_id):
        
        #Genesis Block
        genesis_block = Block(0, '', [], 100, 0)        
        self.chain = [genesis_block]        
        self.__open_transactions = []
        self.public_key = public_key
        self.__peer_nodes = set()
        self.node_id = node_id
        self.load_data()
    
    @property
    def chain(self):
        return self.__chain[:]

    
    @chain.setter
    def chain(self, val):
        self.__chain = val

    def get_open_transactions(self):
        """Returns a copy of the open transactions list."""
        return self.__open_transactions[:]

    def load_data(self):
        """Load data from a fille in order to initialize blockchain & 
            open transactions """
        try:
            with open('blockchain-{}.txt'.format(self.node_id), mode='r') as f:
                
                file_content = f.readlines()
                blockchain = json.loads(file_content[0][:-1])
                
                updated_blockchain = []
                for block in blockchain:
                    converted_tx = [Transaction(
                        tx['sender'], tx['recipient'], tx['signature'], tx['amount']) for tx in block['transactions']]
                    updated_block = Block(
                        block['index'], block['previous_hash'], converted_tx, block['proof'], block['timestamp'])
                    updated_blockchain.append(updated_block)
                self.chain = updated_blockchain
                open_transactions = json.loads(file_content[1][:-1])
                
                updated_transactions = []
                for tx in open_transactions:
                    updated_transaction = Transaction(
                        tx['sender'], tx['recipient'], tx['signature'], tx['amount'])
                    updated_transactions.append(updated_transaction)
                self.__open_transactions = updated_transactions
                peer_nodes = json.loads(file_content[2])
                self.__peer_nodes = set(peer_nodes)
        except (IOError, IndexError):
            pass
        finally:
            print('Cleanup. Data loaded successfully!')

    def save_data(self):
        """Save blockchain & open transactions daat
            to the given file."""
        try:
            with open('blockchain-{}.txt'.format(self.node_id), mode='w') as f:
                saveable_chain = [block.__dict__ for block in [Block(block_el.index, block_el.previous_hash, [
                    tx.__dict__ for tx in block_el.transactions], block_el.proof, block_el.timestamp) for block_el in self.__chain]]
                f.write(json.dumps(saveable_chain))
                f.write('\n')
                saveable_tx = [tx.__dict__ for tx in self.__open_transactions]
                f.write(json.dumps(saveable_tx))
                f.write('\n')
                f.write(json.dumps(list(self.__peer_nodes)))
                
        except IOError:
            print('Saving the dta failed!')

    def proof_of_work(self):
        """Function to generate a proof of work 
            for open transaction, meeting the POW criteria """
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        
        while not Verification.valid_proof(self.__open_transactions, last_hash, proof):
            proof += 1
        return proof

    def get_balance(self, sender=None):
        """Return the balance teh given participant.
        """
        if sender == None:
            if self.public_key == None:
                return None
            participant = self.public_key
        else:
            participant = sender
        tx_sender = [[tx.amount for tx in block.transactions
                      if tx.sender == participant] for block in self.__chain]
        
        open_tx_sender = [tx.amount
                          for tx in self.__open_transactions if tx.sender == participant]
        tx_sender.append(open_tx_sender)
        print(tx_sender)
        amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt)
                             if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)
        tx_recipient = [[tx.amount for tx in block.transactions
                         if tx.recipient == participant] for block in self.__chain]
        amount_received = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt)
                                 if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)
        
        return amount_received - amount_sent

    def get_last_bc_value(self):
        """ Returns the last value of the current blockchain. """
        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]

    

    def add_transaction(self, recipient, sender, signature, amount=1.0, is_receiving=False):
        """ Adds a new value to the blockchain, as well as to the last blockchain value.

        Arguments:
            :sender: The sender.
            :recipient: The recipient.
            :amount: The amount of the transaction
        """
        transaction = Transaction(sender, recipient, signature, amount)
        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            self.save_data()
            if not is_receiving:
                for node in self.__peer_nodes:
                    url = 'http://{}/broadcast-transaction'.format(node)
                    try:
                        response = requests.post(url, json={
                                                 'sender': sender, 'recipient': recipient,
                                                 'amount': amount, 'signature': signature})
                        if response.status_code == 400 or response.status_code == 500:
                            print('Transaction declined, needs resolving')
                            return False
                    except requests.exceptions.ConnectionError:
                        continue
            return True
        return False

    def mine_block(self):
        """Create a new block, and add open transactions to it."""        
        if self.public_key == None:
            return None
        last_block = self.__chain[-1]
        
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work()
        reward_transaction = Transaction(
            'MINING',
            self.public_key,
            '',
            MINING_REWARD)

        copied_transactions = self.__open_transactions[:]
        for tx in copied_transactions:
            if not Wallet.verify_transaction(tx):
                return None
        copied_transactions.append(reward_transaction)
        
        block = Block(len(self.__chain), hashed_block,
                      copied_transactions, proof)
        self.__chain.append(block)
        self.resolve_conflicts = False
        self.__open_transactions = []
        self.save_data()
        
        for node in self.__peer_nodes:
            url = 'http://{}/broadcast-block'.format(node)
            converted_block = block.__dict__.copy()
            converted_block['transactions'] = [
                tx.__dict__ for tx in converted_block['transactions']]
            try:
                response = requests.post(url,
                json={'block': converted_block})
                
                if response.status_code == 400 or response.status_code == 500:
                    print('Block declined, needs resolving')
                if response.status_code == 409:
                    self.resolve_conflicts == True
            
            except requests.exceptions.ConnectionError:
                print('There was a connection error')
                continue
        
        return block

    def add_block(self, block):
        transactions = [Transaction(
            tx['sender'],
            tx['recipient'],
            tx['signature'],
            tx['amount'])
            for tx in block['transactions']]
        
        proof_is_valid = Verification.valid_proof(
            transactions[:-1],
            block['previous_hash'],
            block['proof'])
        
        hashes_match = hash_block(self.chain[-1]) == block['previous_hash']
        
        if not proof_is_valid or not hashes_match:
            return False        

        converted_block = Block(
            block['index'],
            block['previous_hash'],
            transactions,
            block['proof'],
            block['timestamp'])
        self.__chain.append(converted_block)
        
        stored_transactions = self.__open_transactions[:]
        for tx in block['transactions']:
            for opentx in stored_transactions:
                if opentx.sender == tx['sender']\
                and opentx.recipient == tx['recipient']\
                and opentx.amount == tx['amount']\
                and opentx.signature == tx['signature']:
                    try:
                        self.__open_transactions.remove(opentx)
                    except ValueError:
                        print('Item was already removed')
        stored_transactions = self.__open_transactions[:]
        for itx in block['transactions']:
            for opentx in stored_transactions:
                if opentx.sender == itx['sender']\
                    and opentx.recipient == itx['recipient']\
                        and opentx.amount == itx['amount']\
                            and opentx.signature == itx['signature']:
                            try:
                                self.__open_transactions.remove(opentx)
                            except ValueError:
                                print('Item was already removed!!')
        self.save_data()
        return True

    def resolve(self):
        winner_chain = self.chain
        replace = False
        for node in self.__peer_nodes:
            url = 'http://{}/chain'.format(node)
            try:
                response = requests.get(url)
                node_chain = response.json()
                node_chain = [Block(
                    block['index'],
                    block['previous_hash'],
                    
                    [Transaction(
                     tx['sender'],
                     tx['recipient'],
                     tx['signature'],
                     tx['amount']
                 )for tx in block['transactions']],
                    
                    block['proof'],
                    block['timestamp']
                )for block in node_chain]
                
                node_chain_length = len(node_chain)
                local_chain_length = len(self.chain)
                if node_chain_length > local_chain_length\
                    and Verification.verify_chain(node_chain):
                    winner_chain = node_chain
                    replace = True

            except requests.exceptions.ConnectionError:
                continue
            
        self.resolve_conflicts = False
        self.chain = winner_chain
        if replace:
            self.__open_transactions = []
        self.save_data()
        return replace

    def add_peer_node(self, node):
        """Adds a new node.

        Arguments:
            :node: The node URL which should be added.
        """
        self.__peer_nodes.add(node)
        self.save_data()

    def remove_peer_node(self, node):
        """Removes a node.

        Arguments:
            :node: The node URL which should be removed.
        """
        self.__peer_nodes.discard(node)
        self.save_data()

    def get_peer_nodes(self):
        """Return all connected peer_nodes."""
        return list(self.__peer_nodes)