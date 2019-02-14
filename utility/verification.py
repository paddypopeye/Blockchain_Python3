from utility.hash_util import hash_block, hash_string_256
from wallet import Wallet

class Verification:
    @classmethod
    def verify_transactions(cls, open_transactions, get_balance):
        return all([cls.verify_transaction(tx, get_balance, False)\
        for tx in open_transactions()])
    @staticmethod
    def verify_transaction(transaction, get_balance, check_funds=True):
        '''Verifies the validity of the given transaction,
            by checking current balance against the transaction amount.
            Returns True if sufficient balance False otherwise
            Arguments:  
                transaction: the transaction to validate
        '''
        if check_funds:
            sender_balance = get_balance()
            return sender_balance >= transaction.amount and Wallet.verify_transaction(transaction)
        else:
            return Wallet.verify_transaction(transaction)
    
    @classmethod
    def verify_chain(cls, blockchain):
        '''Verify the current blockchain and return True if valid, False otherwise'''
        for (index, block) in enumerate(blockchain):
            if index == 0:
                continue
            if block.previous_hash != hash_block(blockchain[index-1]):
                return False
            if not cls.valid_proof(
                block.transactions[:-1], 
                block.previous_hash,
                block.proof):
                print('Proof of Work is invalid')
                return False  
        return True
    
    @staticmethod 
    def valid_proof(transactions, last_hash, proof):
        '''Returns True if the guessed hash meets POW criteria, False otherwise
        Arguments:
            transactions: list of current open transactions
            last_hash: hash of the previous block
            proof: numeric value for calculating valid proof'''
 
        guess = (str([tx.to_ordered_dict() for tx in transactions])
            +str(last_hash) + str(proof)).encode()
        
        guess_hash = hash_string_256(guess)
        # print("This is the GUESS_HASH", guess_hash)
        
        return guess_hash[0:2] == '00'