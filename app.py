from flask import Flask, render_template, request, jsonify, send_from_directory
from voting_system import VotingSystem

app = Flask(__name__, static_url_path='',
            static_folder='static', template_folder='templates')
voting_system = VotingSystem()


@app.route("/")
def home():
    return render_template("home.html")


@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)


# Voter Section
@app.route("/voter-section")
def voter_section():
    return render_template("voter.html")


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

# Admin Section


@app.route("/admin-section")
def admin_section():
    return render_template("admin.html")


@app.route("/admin/voters", methods=["GET"])
def view_registered_voters():
    return jsonify(voting_system.registered_voters), 200


@app.route("/admin/audit", methods=["GET"])
def audit_blockchain():
    is_valid = voting_system.blockchain.is_chain_valid()
    return jsonify({"blockchain_valid": is_valid}), 200


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/help")
def help_page():
    return render_template("help.html")


@app.route("/contact")
def contact_page():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
