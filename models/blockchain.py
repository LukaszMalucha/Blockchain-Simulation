import datetime
import hashlib
import json
import requests
from urllib.parse import urlparse

class Blockchain:
    """Blockchain Constructor"""

    def __init__(self):
        self.chain = []  # init empty chain
        self.create_block(proof=1, previous_hash='0')  # genesis block

    def create_block(self, proof, previous_hash):
        """Create a single Block"""
        block = {'index': len(self.chain) + 1,  # def block index as a length of chain + 1
                 'timestamp_date': str(datetime.date.today()),
                 'timestamp_time': str(datetime.datetime.now().time()),
                 # time when block was created - as a string for json format
                 'proof': proof,  # proof of work
                 'previous_hash': previous_hash}  # previous block hash
        self.chain.append(block)  # add to blockchain list
        return block

    def get_previous_block(self):
        """Get a previous Block"""
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        """Define proof of work"""
        new_proof = 1
        check_proof = False
        while check_proof is False:
            # simple asymetrical operation turned it into sha256 character
            hash_operation = hashlib.sha256(str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            # set the reward (low difficulty to allow quick mining):
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        """hash function that turns block (dictionary) into sha256 (as expected by hashlib)"""
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        """Blockchain Validation test (is not tampered)"""
        previous_block = chain[0]  # init first block variable
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            # if p.h. of a current block is different than p.h. of previous block
            if block['previous_hash'] != self.hash(
                    previous_block):
                return False
            previous_proof = previous_block['proof']  # check if hash_operations start with '0000'
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True

    def add_transaction(self, sender, receiver, amount):
        """Add transaction to the block"""
        self.transactions.append({'sender': sender,
                                  'receiver': receiver,
                                  'amount': amount})
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1

    def add_node(self, address):
        """Add node"""
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)  # get the address from http


    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get('https://{0}/display_blockchain'.format(node))
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False



def block_mining(blockchain):
    # First get previous_proof
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)

    # Second - get previous_hash
    previous_hash = blockchain.hash(previous_block)

    # Create new block
    block = blockchain.create_block(proof, previous_hash)

    response = {
        'index': block['index'],
        'timestamp_date': block['timestamp_date'],
        'timestamp_time': block['timestamp_time'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
        }

    return response
