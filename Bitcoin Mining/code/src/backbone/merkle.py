# TODO: Make Merkle tree structure

from utils.cryptographic import hash_function


class MerkleTree:
    def __init__(self, txs):
        # Initialize MerkleTree instance.
        self.data = txs
        self.leaf_nodes = []
        self.tree = self.build_tree()

    def build_tree(self):
        # Build the Merkle tree from the transactions.
        for trans in self.data:
            self.leaf_nodes.append(hash_function(trans))
       
        while len(self.leaf_nodes) > 1:
            if len(self.leaf_nodes) % 2 != 0:
                self.leaf_nodes.append(self.leaf_nodes[-1])
            tem = []
            for i in range(0, len(self.leaf_nodes), 2):
                tx1 = self.leaf_nodes[i]
                tx2 = self.leaf_nodes[i+1]
                node = hash_function(tx1 + tx2)
                tem.append(node)
            self.leaf_nodes = tem
        # Return dictionary containing the root hash of the Merkle tree.
        return  {'hash': self.leaf_nodes[0]}

    def get_root(self):
        # Get the root hash of the Merkle tree.
        return self.tree
