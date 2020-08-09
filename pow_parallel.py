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
$ mpirun.openmpi -np <number of nodes or processes> -machinefile <hosts> python pow_parallel.py <level of difficulty>
e.g.
$ mpirun.openmpi -np 3 -machinefile nodes python pow_parallel.py 3

Each of the processes is assigned a unique rank.
When an MPI program is run, each process consists of the same code and will be distributed across nodes.
"""

from mpi4py import MPI
import hashlib
import sys
import random
import time
from urllib.request import urlopen

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
name = MPI.Get_processor_name()

if __name__ == '__main__':

    # The blockchain network sets the difficulty level of the target
    # Mining is essentially finding a hash having a specific number of leading zeros
    difficulty = int(sys.argv[1])
    #print("Mining...")
    start_time = time.time();
    # A block consists of the hash of the blockheader (prevblockhash, merkle tree, and nonce)
    # We just assume that we have the value of the the prevblockhash

    prev_block_hash = hashlib.sha256('{0}'.format("prevblockhash").encode('utf-8')).hexdigest()

    # We use a hypothetical personal identity record as data/transactions in the proposed block.
    raw_records = urlopen("https://raw.githubusercontent.com/roxavinante/blockchain/master/records.json")
    transactions = raw_records.read()
    # print(transactions)

    # Transactions in a block are tamper-proof and immutable. Merkle root is the hash of all the transactions in a block.
    # We assume that the data are stored in a Merkle tree
    merkle_root = hashlib.sha256('{0}'.format(transactions).encode('utf-8')).hexdigest()
    # print("Merkle Root: {0}\n".format(merkle_root))
    block_header = prev_block_hash + merkle_root

    # Next, we will look for the valid nonce that will suffice to find the target (hash value of the new block) using brute force

    # print("Difficulty: {0}\n".format(difficulty))
    nonce = 0
    task_index = 0
    while True:
        if task_index%size!=rank:
            task_index +=1
            nonce += 1
            continue
        hash_value = hashlib.sha256('{0}{1}'.format(block_header, nonce).encode('utf-8')).hexdigest()
        print("Try Nonce: {0} => Hash Result: {1} | Rank: {2}, Size: {3}, Node: {4}".format(nonce, hash_value, rank, size, name))
        i += 1
        nonce += 1
        # Hash difficulty - hash having specific number of leading zeros.
        # The hash value is the fingerprint of the current block and will then be linked to the succeeding blocks.
        target = hash_value[0:difficulty]
        if target == ('0' * difficulty):
            end_time = time.time();
            mining_time = end_time - start_time

            print("\n")
            print("Difficulty/Number of Leading Zeros: {0}".format(difficulty))
            print("Final Nonce: {0}".format(nonce))
            print("New Block Signature: {0}".format(hash_value))
            print("Mining Time: {0} seconds".format(mining_time))
            break;
