import os
import datetime
import hashlib
import json
from flask import Flask, jsonify




##################################################################### Building Blockchain ######################################################################################################################################


########## BUILD BLOCKCHAIN CLASS  

class Blockchain:
    
    def __init__(self):
        self.chain = []                                                         ## init empty chain
        self.create_block(proof = 1, previous_hash = '0')                       ## genesis block     

## Init block  

    def create_block(self, proof, previous_hash):                               ## init block  
        block = {'index': len(self.chain) + 1,                                  ## def block index as a length of chain + 1
                 'timestamp': str(datetime.datetime.now()),                     ## time when block was created - as a string for json format
                 'proof': proof,                                                ## proof of work
                 'previous_hash': previous_hash}                                ## previous block hash   
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
        


########## CREATE FLASK APP

app = Flask(__name__)

## Create a Blockchain:

blockchain = Blockchain()




########## MINING BLOCKCHAIN

@app.route('/mine_block', methods = ['GET'])
def mine_block():
    
    ## First get previous_proof
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    
    ## Second - get previous_hash
    previous_hash = blockchain.hash(previous_block)
    
    ## Create new block
    block = blockchain.create_block(proof, previous_hash)
    
    response = {'message': 'Congratz, you mined a block',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
                
    return jsonify(response), 200 


########### DISPLAY FULL BLOCKCHAIN

@app.route('/display_blockchain', methods = ['GET'])
def display_blockchain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
                
    return jsonify(response), 200          
    
    
    
    
########### DISPLAY VALIDATION TEST

@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'Blockchain is valid'}
    else:
        response = {'message': 'There are errors in Blockchain'}
    return jsonify(response), 200     
        


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=False)