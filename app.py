import json
import hashlib
from flask import Flask, request
import time
from uuid import uuid4
from flask.globals import request
from flask.json import jsonify

class Blockchain(object):
    difficulty_level = "000"
    idnr = 0

    def __init__(self):
        self.chain = []
        self.current_transaction = []
        genesis_Hash = self.Block_Hash("genesis_block")
        self.append_block(
            Previous_block_hash = genesis_Hash,
            nonce = self.PoW(0,genesis_Hash, [])
            )
        
    def Block_Hash(self,block):
        blockEncoder = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha512(blockEncoder).hexdigest()
    
    def PoW(self,index,Previous_block_hash,transactions):
        nonce=0
        while self.validate_Proof(index,Previous_block_hash,
                                  transactions, nonce) is False:
            nonce+=1
        return nonce
    
    def validate_Proof(self,index,Previous_block_hash,transactions,nonce):
        data = f'{index},{Previous_block_hash},{transactions},{nonce}'.encode()
        hash_data = hashlib.sha512(data).hexdigest()
        return hash_data[:len(self.difficulty_level)] == self.difficulty_level
        
    def append_block(self,nonce, Previous_block_hash):
        seconds = time.time()
        block ={
            'index': len(self.chain),
            'transactions':self.current_transaction,
            'timestamp': time.ctime(seconds),
            'nonce' : nonce,
            'Previous_block_hash': Previous_block_hash
        }
        self.current_transaction = []
        self.chain.append(block)
        return block
    
    def add_transaction(self, username, publicKey):
        self.idnr += 1
        self.current_transaction.append({
            'username':username,
            'id':self.idnr,
            'publicKey':publicKey,
            })
        return self.last_block['index']+1
    
    @property
    def last_block(self):
        return self.chain[-1]

# Flask
app = Flask(__name__)

node_identifier = str(uuid4()).replace('-',"")
blockchain = Blockchain()

@app.route('/')
def base():
    base_output = """ <!DOCTYPE html>
                <html>
                <head>
                <title>Identity Management</title>
                </head>
                <body>
                <h1>Welcome to the Identity Management Service of Benjamin and Julia!</h1>
                <h2>Website Options</h2>
                <p>These are the possible websites to have a look at the appending of the Identity and looking at the Blockchain.</p>
                <ul>
                    <li><a href="http://127.0.0.1:8000/blockchain">The Blockchain</a></li>
                    <li>To add an identity to the Blockchain do the following:</li>
                    <ol>
                        <li><a href="http://127.0.0.1:8000/transaction">Add Information</a></li>
                        <li><a href="httP://127.0.0.1:8000/mine">Attach the information to the Blockchain</a></li>
                        <li><a href="httP://127.0.0.1:8000/blockchain">Check the Blockchain for the new block</a></li>
                    </ol>
                </ul>

                </body>
                </html> """
    return base_output

@app.route('/blockchain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
        }
    return jsonify(response), 200

@app.route('/mine', methods=['GET'])
def mine_block():
    last_block_hash = blockchain.Block_Hash(blockchain.last_block)
    index = len(blockchain.chain)
    nonce = blockchain.PoW(index,last_block_hash,blockchain.current_transaction)
    block = blockchain.append_block(nonce,last_block_hash)
    response = {
        'difficulty_level':blockchain.difficulty_level,
        'message': "new block has been added (mined)",
        'index': block['index'],
        'hash_of_previous_block': block['Previous_block_hash'],
        'nonce':block['nonce'],
        'transaction':block['transactions']
        }
    return jsonify(response), 200

@app.route('/transaction', methods=('GET','POST'))
def new_transactions():
    transaction_output = """
        <!DOCTYPE html>
        <html>
        <head>
        <title>Identity Management</title>
        </head>
        <h1>Please add your informations for the Identity Management!</h1>
        <body>
            <form method="post">
                <label for="uname">Username</label>
                    <br>
                    <input type="text" name="uname" placeholder="Username"></input>
                    <br>

                    <label for="pubkey">Public Key</label>
                    <br>
                    <textarea name="pubkey" placeholder="Public Key" rows="15" cols="60"></textarea>
                    <br>
                    <button type="submit">Submit</button>
            </form>
        </body>
        </html> 
    """ 
    if request.method == 'POST':
        uname = request.form['uname']
        pubkey = request.form['pubkey']

        blockchain.add_transaction(username = uname, publicKey = pubkey)
        
    return transaction_output

if __name__=='__main__':
    app.run(host='0.0.0.0', port=8000)
