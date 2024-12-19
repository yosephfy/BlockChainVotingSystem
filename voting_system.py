import hashlib

import cryptography
from database import register_voter, authenticate_voter, mark_voter_as_voted, add_block_to_db, fetch_all_blocks, get_election_status, update_election_status
from cryptography.fernet import Fernet
import time
import json
import os


class Block:
    def __init__(self, index, timestamp, data, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
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
        genesis_block = Block(0, str(time.time()), "Genesis Block", "0")
        self.chain.append(genesis_block)

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, data):
        last_block = self.get_last_block()
        new_block = Block(
            index=last_block.index + 1,
            timestamp=str(time.time()),
            data=json.dumps(data),
            previous_hash=last_block.hash
        )
        self.proof_of_work(new_block)
        self.chain.append(new_block)
        add_block_to_db(new_block.index, new_block.timestamp, new_block.data,
                        new_block.previous_hash, new_block.hash, new_block.nonce)

    def proof_of_work(self, block):
        while not block.hash.startswith("0" * self.difficulty):
            block.nonce += 1
            block.hash = block.compute_hash()

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.compute_hash() or current_block.previous_hash != previous_block.hash:
                return False
        return True


class VotingSystem:
    def __init__(self):
        self.encryption_key = self.load_or_generate_key()
        self.cipher = Fernet(self.encryption_key)
        self.blockchain = Blockchain()

    def load_or_generate_key(self):
        key_file = "fernet_key.key"
        if os.path.exists(key_file):
            with open(key_file, "rb") as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, "wb") as f:
                f.write(key)
            return key

    def get_election_status(self):
        return get_election_status()

    def start_election(self):
        if self.get_election_status() == "not_started":
            update_election_status("ongoing")
            return True
        return False

    def end_election(self):
        if self.get_election_status() == "ongoing":
            update_election_status("ended")
            return True
        return False

    def reset_election(self):
        self.blockchain = Blockchain()
        update_election_status("not_started")
        return True

    def can_vote(self):
        return self.get_election_status() == "ongoing"

    def can_view_results(self):
        return self.get_election_status() == "ended"

    def register_voter(self, voter_id, password):
        return register_voter(voter_id, password)

    def authenticate_voter(self, voter_id, password):
        return authenticate_voter(voter_id, password)

    def cast_vote(self, voter_id, candidate):
        if not self.can_vote():
            return False
        encrypted_vote = self.cipher.encrypt(candidate.encode()).decode()
        vote_data = {"voter_id": voter_id, "vote": encrypted_vote}
        self.blockchain.add_block(vote_data)
        mark_voter_as_voted(voter_id)
        return True

    def tally_votes(self):
        results = {}
        blocks = fetch_all_blocks()
        for block in blocks:
            try:
                data = json.loads(block.data)
                candidate = self.cipher.decrypt(data["vote"].encode()).decode()
                results[candidate] = results.get(candidate, 0) + 1
            except (json.JSONDecodeError, cryptography.fernet.InvalidToken):
                # Log and skip invalid votes
                continue
        # Remove "Invalid Encrypted Data" from results if present
        if "Invalid Encrypted Data" in results:
            del results["Invalid Encrypted Data"]
        return results

    def decrypt_vote(self, encrypted_vote):
        try:
            return self.cipher.decrypt(encrypted_vote.encode()).decode()
        except cryptography.fernet.InvalidToken:
            return "Invalid Encrypted Data"
