# app.py
from random import choice
import time
from cryptography.fernet import Fernet
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, render_template, request, jsonify, session, url_for, send_from_directory
from voting_system import VotingSystem
from database import Block, Voter, db, register_voter, authenticate_voter, fetch_all_voters, fetch_all_blocks, remove_all_voters

import json

app = Flask(__name__, static_url_path='',
            static_folder='static', template_folder='templates')
app.secret_key = "supersecretkey"  # Replace with a secure key

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///election.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

voting_system = VotingSystem()

# Initialize database


@app.cli.command('init-db')
def init_db():
    """Initialize the database."""
    print("Initializing database...")
    db.create_all()
    print("Database initialized.")
# Serve Static Files


@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

# Home Page


@app.route("/")
def home():
    return render_template("home.html")

# Voter Login Page


@app.route("/login")
def login_page():
    return render_template("login.html")

# Voter Registration Page


@app.route("/register")
def register_page():
    return render_template("register.html")

# Voter Dashboard


@app.route("/voter-section")
def voter_section():
    if "voter_id" in session:
        voter_id = session["voter_id"]
        return render_template("voter.html", voter_id=voter_id)
    else:
        return redirect(url_for("login_page"))

# Logout


@app.route("/logout")
def logout():
    session.pop("voter_id", None)
    return redirect(url_for("home"))

# Voter Registration API


@app.route("/register", methods=["POST"])
def register_voter_api():
    data = request.json
    voter_id = data.get("voter_id")
    password = data.get("password")
    if not voter_id or not password:
        return jsonify({"error": "Voter ID and password are required"}), 400
    if register_voter(voter_id, password):
        return jsonify({"message": "Registration successful"}), 200
    return jsonify({"error": "Voter ID must be unique."}), 400

# Voter Login API


@app.route("/login", methods=["POST"])
def login_voter():
    data = request.json
    voter_id = data.get("voter_id")
    password = data.get("password")
    if authenticate_voter(voter_id, password):
        session["voter_id"] = voter_id
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"error": "Invalid voter ID or password"}), 401

# Cast Vote


@app.route("/cast-vote", methods=["POST"])
def cast_vote():
    if "voter_id" not in session:
        return jsonify({"error": "You must be logged in to vote"}), 403
    data = request.json
    candidate = data.get("candidate")
    voter_id = session["voter_id"]
    if not candidate:
        return jsonify({"error": "Candidate name is required"}), 400
    if not voting_system.can_vote():
        return jsonify({"error": "Voting is not currently ongoing."}), 400
    if voting_system.cast_vote(voter_id, candidate):
        return jsonify({"message": f"Vote cast for {candidate}"}), 200
    else:
        return jsonify({"error": "You have already voted or invalid voter"}), 400

# View Results


@app.route("/results", methods=["GET"])
def get_results():
    if not voting_system.can_view_results():
        return jsonify({"error": "Results are only available after the election ends."}), 403
    try:
        results = voting_system.tally_votes()
        return jsonify(results), 200
    except json.JSONDecodeError as e:
        return jsonify({"error": f"Invalid JSON format in block data: {str(e)}"}), 500

# Admin Login Page


@app.route("/admin-login")
def admin_login_page():
    return render_template("admin_login.html")

# Admin Login API


@app.route("/admin-login", methods=["POST"])
def admin_login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username == "admin" and password == "admin123":
        session["admin"] = True
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"error": "Invalid credentials"}), 401

# Admin Dashboard


@app.route("/admin-dashboard")
def admin_dashboard():
    if "admin" in session:
        return render_template("admin_dashboard.html")
    return redirect(url_for("admin_login_page"))

# View Registered Voters


@app.route("/admin/voters", methods=["GET"])
def view_registered_voters():
    if "admin" in session:
        voters = fetch_all_voters()
        return jsonify([{"voter_id": voter.voter_id, "voted": voter.voted} for voter in voters])
    return jsonify({"error": "Unauthorized"}), 403

# View Election Statistics


@app.route("/admin/statistics", methods=["GET"])
def view_statistics():
    if "admin" in session:
        blocks = fetch_all_blocks()
        results = {}
        for block in blocks:
            try:
                data = json.loads(block.data.replace("'", '"'))
                candidate = voting_system.decrypt_vote(data["vote"])
                results[candidate] = results.get(candidate, 0) + 1
            except json.JSONDecodeError as e:
                return jsonify({"error": f"Invalid JSON format in block data: {str(e)}"}), 500
        total_votes = sum(results.values())
        return jsonify({"results": results, "total_votes": total_votes}), 200
    return jsonify({"error": "Unauthorized"}), 403

# Reset Election Results


@app.route("/admin/reset-results", methods=["GET"])
def reset_results():
    if "admin" in session:
        # Reset the blockchain in memory
        voting_system.reset_election()

        # Reset the database: Clear blockchain data and reset voter statuses
        db.session.query(Block).delete()  # Clear the Block table
        for voter in Voter.query.all():  # Reset the voted status for all voters
            voter.voted = False
        db.session.commit()

        return jsonify({"message": "Election reset successfully"}), 200
    return jsonify({"error": "Unauthorized"}), 403

# Remove All Voters


@app.route("/admin/remove-voters", methods=["DELETE"])
def remove_all_voters_api():
    if "admin" in session:
        remove_all_voters()
        return jsonify({"message": "All voters removed successfully"}), 200
    return jsonify({"error": "Unauthorized"}), 403

# Audit Blockchain


@app.route("/admin/audit")
def audit_blockchain():
    if "admin" in session:
        is_valid = voting_system.blockchain.is_chain_valid()
        message = "Blockchain is valid" if is_valid else "Blockchain is corrupted"
        return jsonify({"message": message}), 200
    return jsonify({"error": "Unauthorized"}), 403

# Start/End Election


@app.route("/admin/start-election", methods=["GET"])
def start_election():
    if "admin" in session:
        if voting_system.start_election():
            return jsonify({"message": "Election started successfully"}), 200
        return jsonify({"error": "Election already ongoing or ended"}), 400
    return jsonify({"error": "Unauthorized"}), 403


@app.route("/admin/end-election", methods=["GET"])
def end_election():
    if "admin" in session:
        if voting_system.end_election():
            return jsonify({"message": "Election ended successfully"}), 200
        return jsonify({"error": "No election is currently ongoing"}), 400
    return jsonify({"error": "Unauthorized"}), 403


@app.route("/admin/generate-random-votes", methods=["POST"])
def generate_random_votes():
    if "admin" not in session:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.json
    num_votes = data.get("numVotes")
    if not num_votes or not str(num_votes).isdigit() or int(num_votes) <= 0:
        return jsonify({"error": "Invalid number of votes"}), 400

    candidates = ["Candidate A", "Candidate B", "Candidate C"]
    for _ in range(int(num_votes)):
        voter_id = f"debug_{int(time.time() * 1000)}"  # Unique voter ID
        password = "debug_password"  # Default password for debugging

        # Register the voter
        if not register_voter(voter_id, password):
            # Skip if voter ID already exists (though unlikely with unique IDs)
            continue

        # Assign a random vote
        candidate = choice(candidates)
        encrypted_vote = voting_system.cipher.encrypt(
            candidate.encode()).decode()
        voting_system.blockchain.add_block(
            {"voter_id": voter_id, "vote": encrypted_vote}
        )

    return jsonify({"message": f"{num_votes} random votes generated and voters registered successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True)
