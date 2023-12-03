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

