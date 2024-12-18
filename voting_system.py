import hashlib
import time


class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data  # List of transactions (votes)
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = f"{self.index}{self.timestamp}{
            self.data}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = []
        self.difficulty = 2
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, time.time(), "Genesis Block", "0")
        self.chain.append(genesis_block)

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, data):
        last_block = self.get_last_block()
        new_block = Block(
            index=last_block.index + 1,
            timestamp=time.time(),
            data=data,
            previous_hash=last_block.hash
        )
        self.proof_of_work(new_block)
        self.chain.append(new_block)

    def proof_of_work(self, block):
        while not block.hash.startswith("0" * self.difficulty):
            block.nonce += 1
            block.hash = block.compute_hash()

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.compute_hash() or \
               current_block.previous_hash != previous_block.hash:
                return False
        return True


class VotingSystem:
    def __init__(self):
        self.blockchain = Blockchain()
        self.registered_voters = {}

    def register_voter(self, voter_id):
        if voter_id in self.registered_voters:
            return False
        self.registered_voters[voter_id] = False
        return True

    def cast_vote(self, voter_id, candidate):
        if voter_id not in self.registered_voters or self.registered_voters[voter_id]:
            return False
        vote_data = {"voter_id": voter_id, "vote": candidate}
        self.blockchain.add_block(vote_data)
        self.registered_voters[voter_id] = True
        return True

    def tally_votes(self):
        results = {}
        for block in self.blockchain.chain[1:]:
            vote = block.data.get("vote")
            if vote:
                results[vote] = results.get(vote, 0) + 1
        return results
