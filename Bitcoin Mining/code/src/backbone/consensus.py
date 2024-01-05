# backbone/consensus.py
from utils.flask_utils import flask_call
import rsa
from server import REQUEST_TXS, GET_BLOCKCHAIN, DIFFICULTY, SELF
from abstractions.transaction import Transaction
import json
from abstractions.block import Block,Blockchain
from datetime import datetime
from utils.cryptographic import double_hash
import itertools


# TODO: Implement Proof of Work
def proofOfWork():
    myBlock = createBlock()
    for nonce in itertools.count():
        myBlock.nonce = nonce
        myBlock.time = datetime.now().timestamp()
        hash_try=double_hash(str(myBlock.prev)+str(myBlock.time)+str(myBlock.merkle_root)+str(myBlock.nonce))
        if hash_try.startswith('0' * DIFFICULTY):
            myBlock.creation_time = datetime.now().timestamp() - myBlock.creation_time
            myBlock.mined_by = SELF
            myBlock.hash= hash_try
            f = open('../vis/users/zal004_pvk.pem')
            privateKey= f.read()
            myKey= rsa.PrivateKey.load_pkcs1(privateKey,'PEM')
            blockHashed=bytes(myBlock.hash,'utf-8')
            myBlock.signature = rsa.sign(blockHashed,myKey,'SHA-1')
            return myBlock


# TODO: Build a block

def createBlock():  
  _, trans, code = flask_call('GET', REQUEST_TXS)
  transactions=[]
  if trans:
    for t in trans:
      transactions.append(Transaction.load_json(json.dumps(t)))
    _, blockchain, code = flask_call('GET', GET_BLOCKCHAIN)
    chain = Blockchain.load_json(json.dumps(blockchain))

    if blockchain:
       block = Block(transactions=transactions, nonce=0, hash= "", creation_time=datetime.now().timestamp(), height=chain.block_list[-1].height+1, previous_block=chain.block_list[-1].hash, time=datetime.now().timestamp())
       return block
