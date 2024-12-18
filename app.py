from flask import Flask, request, jsonify
from voting_system import VotingSystem

app = Flask(__name__)
voting_system = VotingSystem()


@app.route("/")
def home():
    return "Blockchain Voting System is running!"


@app.route("/register-voter", methods=["POST"])
def register_voter():
    data = request.json
    voter_id = data.get("voter_id")
    if not voter_id:
        return jsonify({"error": "Voter ID is required"}), 400
    if voting_system.register_voter(voter_id):
        return jsonify({"message": f"Voter {voter_id} registered successfully"}), 200
    return jsonify({"error": "Voter already registered"}), 400


@app.route("/cast-vote", methods=["POST"])
def cast_vote():
    data = request.json
    voter_id = data.get("voter_id")
    candidate = data.get("candidate")
    if not voter_id or not candidate:
        return jsonify({"error": "Voter ID and candidate are required"}), 400
    if voting_system.cast_vote(voter_id, candidate):
        return jsonify({"message": f"Vote cast by {voter_id} for {candidate}"}), 200
    return jsonify({"error": "Failed to cast vote"}), 400


@app.route("/results", methods=["GET"])
def get_results():
    results = voting_system.tally_votes()
    return jsonify(results), 200


if __name__ == "__main__":
    app.run(debug=True)
