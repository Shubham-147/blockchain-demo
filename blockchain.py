# Creating A Block Chain

import datetime
import hashlib
import json
from flask import Flask, jsonify

class BlockChain:
    
    def __init__(self):
        self.chain = []
        self.createBlock(proof = 1, prevHash = '0')
        
    def createBlock(self, proof, prevHash):
        block = { 'index': len(self.chain) + 1, 
                  'timeStamp': str(datetime.datetime.now()),
                  'proof': proof,
                  'prevHash': prevHash }
        self.chain.append(block)
        return block
    
    def getPrevHash(self):
        return self.chain[-1]
    
    def proofOfWork(self, prevProof):
        newProof = 1
        while True:
            message = str(newProof ** 2 - prevProof ** 2); 
            hashOperation = hashlib.sha256(message.encode()).hexdigest()
            if hashOperation[:4] == '0000':
                break
            else:
                newProof += 1
        return newProof
    
    def hash(self, block):
        encodedBlock = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encodedBlock).hexdigest()

    def isChainValid(self, chain):
        prevBlock = chain[0]
        blockIndex = 1
        while blockIndex < len(chain):
            block = chain[blockIndex]
            if block['prevHash'] != self.hash(prevBlock):
                return False
            prevProof = prevBlock['proof']
            proof = block['proof']
            message = str(proof ** 2 - prevProof ** 2); 
            hashOperation = hashlib.sha256(message.encode()).hexdigest()
            if hashOperation[:4] != '0000':
                return False
            prevBlock = block
            blockIndex += 1
        return True
    
# Mining Blockchain
 
# Using Flask to create Flash Web App
  
app = Flask(__name__)
blockchain = BlockChain() 

# Mining a new Block
@app.route('/mine-block' , methods = ['GET'])
def mineBlock():
    prevBlock = blockchain.getPrevHash()
    prevProof = prevBlock['proof']
    proof = blockchain.proofOfWork(prevProof)
    prevHash = blockchain.hash(prevBlock)
    block = blockchain.createBlock(proof, prevHash)
    response = {'message': 'You Cracked It !!', 
                'index': block['index'], 
                'timeStamp': block['timeStamp'],
                'proof': block['proof'],
                'prevHash': block['prevHash'] }
    return jsonify(response), 200

# Get Full Block Chain
@app.route('/get-block-chain', methods = ['GET'])
def getBlockChain():
    response = {'chain' : blockchain.chain,
                'lenght' : len(blockchain.chain),
                'message': 'Here is the blockchain'}
    return jsonify(response), 200

# Check if blockchain is Valid 
@app.route('/is-block-chain-valid', methods = ['GET'])
def isBlockChainValid():
    valid = blockchain.isChainValid(blockchain.chain)
    response = {'valid' : valid,
                'BlockChain lenght' : len(blockchain.chain) }
    return jsonify(response), 200

# Running the app
app.run(host = '0.0.0.0' , port = 5000)
        
    
            
            
        