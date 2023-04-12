# Import necessary libraries
import hashlib
import json
import time
from flask import Flask, jsonify, redirect, request, render_template

# Define the Block class
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        # Hashes the block's data using SHA-256 algorithm
        sha = hashlib.sha256()
        sha.update((str(self.index) + str(self.timestamp) + json.dumps(self.data) + str(self.previous_hash) + str(self.nonce)).encode('utf-8'))
        return sha.hexdigest()

    def mine_block(self, difficulty):
        # Mines the block by finding a hash with a certain number of leading zeros
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

# Define the Blockchain class
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4  # Difficulty level for mining

    def create_genesis_block(self):
        # Creates the first block (genesis block) in the chain
        return Block(0, time.time(), "Genesis Block", "0")

    def get_latest_block(self):
        # Returns the latest block in the chain
        return self.chain[-1]

    def add_block(self, new_block):
        # Adds a new block to the chain
        new_block.index = len(self.chain)
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self):
        # Checks if the blockchain is valid by verifying the hashes and previous hash of each block
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash() or current_block.previous_hash != previous_block.hash:
                return False
        return True

# Create Flask app
app = Flask(__name__)

# Create instance of Blockchain class
my_chain = Blockchain()

# Define API endpoints
@app.route('/mine', methods=['GET'])
def mine_block():
    # Mine a new block and add it to the blockchain
    new_block = Block(0, time.time(), "Transaction Data", "")
    my_chain.add_block(new_block)
    response = {
        'message': 'Block mined and added to the blockchain',
        'block': {
            'index': new_block.index,
            'timestamp': new_block.timestamp,
            'data': new_block.data,
            'previous_hash': new_block.previous_hash,
            'hash': new_block.hash,
            'nonce': new_block.nonce
        }
    }
    return jsonify(response), 200

#@app.route('/')
#def root():
    # Redirect to /chain instead of /
 #   return redirect('/chain', code=302)

@app.route('/chain', methods=['GET'])
def get_chain():
    # Get the current state of the blockchain
    response = {
        'chain': [{
            'index': block.index,
            'timestamp': block.timestamp,
            'data': block.data,
            'previous_hash': block.previous_hash,
            'hash': block.hash,
            'nonce': block.nonce
} for block in my_chain.chain]
    }
    return jsonify(response), 200

@app.route('/validate', methods=['GET'])
def validate_chain():
# Validate the integrity of the blockchain
    is_valid = my_chain.is_chain_valid()
    if is_valid:
        response = {'message': 'Blockchain is valid'}
        status = 200
    else:
        response = {'message': 'Blockchain is not valid'}
        status = 400
    return jsonify(response), status

@app.route('/', methods=['GET'])
def home():
    # Render the HTML file
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)