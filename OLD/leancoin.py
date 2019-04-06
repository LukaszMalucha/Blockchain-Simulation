import os
import datetime
import hashlib
import json
from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
import requests
from uuid import uuid4
from urllib.parse import urlparse



## App Settings


app = Flask(__name__)
app.config['SECRET_KEY'] = 'BiggestSecret'
Bootstrap(app)

##################################################################### Creating LeanCoin Cryptocurrency ######################################################################################################################################


## Init Class

class Blockchain:
    
    def __init__(self):
        self.chain = []                                                         ## init empty chain
        self.transactions = []                                                  ## has to be before create block in order to include transactions in mined block
        self.create_block(proof = 1, previous_hash = '0')                       ## genesis block     
        self.nodes = set()                                                      ## nodes as a set        


## Init block  

    def create_block(self, proof, previous_hash):                               ## init block  
        block = {'index': len(self.chain) + 1,                                  ## def block index as a length of chain + 1
                 'timestamp': str(datetime.datetime.now()),                     ## time when block was created - as a string for json format
                 'proof': proof,                                                ## proof of work
                 'transactions': self.transactions,                             ## included transactions
                 'previous_hash': previous_hash}                                ## previous block hash   
        self.transactions = []                                                  ## emptying transaction list
        self.chain.append(block)                                                ## add to blockchain list    
        return block

## Get last block 

    def get_previous_block(self):                                                          
        return self.chain[-1]


## Def proof of work 

    def proof_of_work(self, previous_proof):      
        new_proof = 1                                                               
        check_proof = False
        while check_proof is False:
            ## simple asymetrical operation turned it into sha256 character
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()   
            ##set the reward:
            if hash_operation[:4] == '0000':                                    ## simple problem to allow quick mining
                check_proof = True
            else: 
                new_proof  += 1
        return new_proof  
        
## hash function that turns block (dictionary) into sha256 (as expected by hashlib)
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
        
## Blockchain Validation test   

    def is_chain_valid(self, chain):
        previous_block = chain[0]                                               ## init first block variable
        block_index = 1                                                        
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):             ## if p.h. of a current block is different than p.h. of previous block
                return False
            previous_proof = previous_block['proof']                            ## check if hash_operations start with '0000'
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block   
            block_index += 1 
        return True    
        
        
## Init transactions

    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({'sender': sender, 
                                  'receiver': receiver, 
                                  'amount': amount})
        previous_block = self.get_previous_block()                          
        return previous_block['index'] + 1                                      ## get index of the last block of a chain                          
        
        
## Add node

    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)                                       ## get the address from http
        
        
## Update blockchain

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
        
## Initiating node address on Port 5000
node_address = str(uuid4()).replace('-','')

## Create a Blockchain:

blockchain = Blockchain()

##################################################################### ROUTES + MINING  ######################################################################################################################################


########## MAIN PAGE

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    response = {}
    
    return render_template('index.html', response = response)



########## MINING BLOCKCHAIN

@app.route('/mine_block', methods=['GET', 'POST'])
def mine_block():
    
    ## First get previous_proof
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    
    ## Second - get previous_hash
    previous_hash = blockchain.hash(previous_block)
    
    ## Include transactions in a block
    # blockchain.add_transaction(sender = node_address, receiver = 'LeakyWiks', amount = 10)
    
    ## Create new block
    block = blockchain.create_block(proof, previous_hash)
    
    response = {'message': "Congratulations, you've successfully mined a LeanCoin Block!!!",
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'transactions': block['transactions'],
                'previous_hash': block['previous_hash']}
                
    return render_template('index.html', response = response)


########### DISPLAY FULL BLOCKCHAIN

@app.route('/display_blockchain', methods = ['GET'])
def display_blockchain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
                
    return render_template('blockchain.html', response = response)        
    
    
########### DISPLAY VALIDATION TEST

@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'BLOCKCHAIN IS VALID',
                    'chain': blockchain.chain,
                    'length': len(blockchain.chain)}
    else:
        response = {'message': 'THERE ARE ERRORS IN A BLOCKCHAIN',
                    'chain': blockchain.chain,
                    'length': len(blockchain.chain)}
    return render_template('blockchain.html', response = response)  
    
    
########### POST TRANSACTION

@app.route('/add_transaction', methods=['GET', 'POST'])
def add_transaction():
    response = {}
    if request.method == 'POST':
        index = blockchain.add_transaction(request.form['sender'], request.form['receiver'], request.form['amount'])
        response = {'message': "Transaction will be added to Block {0}".format(index)}
        return render_template('index.html', response = response)
        
    return render_template('add_transaction.html', response = response)  
    
        
##################################################################### LEANCOIN DECENTALIZATION  ######################################################################################################################################


########### CONNECT NEW NODE (USER)

@app.route('/connect_node', methods = ['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return "No node", 400
    for node in nodes:
        blockchain.add_node(node)
    response = {'message': "All nodes are connected. Nodes:",
                'total_nodes': list(blockchain.nodes)}    
    return jsonify(response), 201     
    

########### UPDATE CHAIN WITH THE LONGEST VALID VERSION

@app.route('/replace_chain', methods = ['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if True:
        response = {'message': 'Blockchain was updated with the longest version',
                    'new_chain' : blockchain.chain }
    else:
        response = {'message': 'Blockchain is up to date',
                    'actual_chain' : blockchain.chain }
                    
    return render_template('index.html', response = response)     
    
    
########### BITS TO TARGET CONVERTER
@app.route('/converter', methods=['GET', 'POST'])
def converter():
    response = {}
    if request.method == 'POST':
        dec = int(request.form['bits'], 16)
        true_hex = hex(dec)[2:]
        hex_string = str(true_hex)
        first_two = true_hex[:2]
        the_rest = true_hex[2:]
        first_two_decimal = int(first_two, 16)
        target_length = int(first_two_decimal) * 2
        following_zeros_amount = int(target_length) - len(the_rest)
        following_zeros = '0' * following_zeros_amount
        base_hex = the_rest + following_zeros  
        leading_zeros = '0'* (64 - len(base_hex))
        final_hex = leading_zeros + base_hex
        response = {'target': final_hex }
        return render_template('converter.html', response = response)
        
    return render_template('converter.html', response = response)




if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 