""" 
A hashcash-based proof of work simulation
Author: Rox Avinante, UP EEEI

Proof-of-Work is a consensus algorithm that is used to validate transactions 
and broadcast new blocks to the blockchain. Block validators or often called 
miners in the network will compete against each other in solving complex computational 
puzzles. These puzzles are difficult to solve but the correct solution is easy to verify. 
Once a miner has found the solution to the puzzle, they will be able to broadcast 
the block to the network where all the other block validators will then verify that 
the solution is correct.

How to run the script
python proof_of_work.py <difficulty level> - number of leading zeros
e.g.
$ python proof_of_work.py 3 or
$ ./proof_of_work.py 3
"""

import hashlib
import sys
import urllib2
import random
import time

if __name__ == '__main__':

    # The blockchain network sets the difficulty level of the target
    # Mining is essentially finding a hash having a specific number of leading zeros
    difficulty = int(sys.argv[1])
    print("Difficulty: {0}".format(difficulty))
    print("Mining...")
    start_time = time.time();
    # A block consists of the hash of the blockheader (prevblockhash, merkle tree, and nonce)
    # We just assume that we have the value of the the prevblockhash

    prev_block_hash = hashlib.sha256(b'{0}'.format(random.random())).hexdigest()

    # We use a hypothetical personal identity record as data/transactions in the proposed block.
    raw_records = urllib2.urlopen("https://raw.githubusercontent.com/roxavinante/blockchain/master/records.json")
    transactions = raw_records.read()
    print(transactions)
    
    # Transactions in a block are tamper-proof and immutable. Merkle root is the hash of all the transactions in a block.
    # We assume that the data are stored in a Merkle tree
    merkle_root = hashlib.sha256(b'{0}'.format(transactions)).hexdigest()
    print("Merkle Root: {0}".format(merkle_root))

    block_header = prev_block_hash + merkle_root

    # Next, we will look for the valid nonce that will suffice to find the target (hash value of the new block) using brute force

    nonce = 0
    while True:
        hash_value = hashlib.sha256(b'{0}{1}'.format(block_header, nonce)).hexdigest()
        print("Try Nonce: {0} => Hash Result: {1}".format(nonce, hash_value))
        nonce += 1

        # Hash difficulty - hash having specific number of leading zeros.
        # The hash value is the fingerprint of the current block and will then be linked to the succeeding blocks.
        target = hash_value[0:difficulty]
        if target == ('0' * difficulty):
            break;

    end_time = time.time();
    mining_time = end_time - start_time

    print("\n")
    print("Difficulty/Number of Leading Zeros: {0}".format(difficulty))
    print("Final Nonce: {0}".format(nonce))
    print("New Block Signature: {0}".format(hash_value))
    print("Mining Time: {0} seconds".format(mining_time))