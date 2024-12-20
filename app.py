import json
import os
import time
from random import choice
from functools import wraps

from flask import Flask, redirect, render_template, request, jsonify, session, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from voting_system import VotingSystem
from database import Block, Voter, db, get_election_status, register_voter, authenticate_voter, fetch_all_voters, fetch_all_blocks, remove_all_voters

# App Configuration
app = Flask(__name__, static_url_path='',
            static_folder='static', template_folder='templates')
# Replace with environment variable
app.secret_key = os.getenv("APP_SECRET_KEY", "fallback_secret_key")

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///election.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

voting_system = VotingSystem()

# Decorator for role-based login checks


def login_required(role):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if role == "admin" and "admin" not in session:
                return jsonify({"status": "error", "message": "Unauthorized"}), 403
            if role == "voter" and "voter_id" not in session:
                return jsonify({"status": "error", "message": "Unauthorized"}), 403
            return f(*args, **kwargs)
        return wrapped
    return decorator

# Response utilities


def success_response(message, data=None):
    return jsonify({"status": "success", "message": message, "data": data}), 200


def error_response(message, status_code=400):
    return jsonify({"status": "error", "message": message}), status_code

# Initialize database


@app.cli.command('init-db')
def init_db():
    """Initialize the database."""
    try:
        print("Initializing database...")
        db.create_all()
        print("Database initialized.")
    except Exception as e:
        print(f"Database initialization failed: {e}")

# Serve Static Files


@app.route('/static/<path:filename>')
def static_files(filename):
    return app.send_static_file(filename)

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
@login_required("voter")
def voter_section():
    voter_id = session["voter_id"]
    return render_template("voter.html", voter_id=voter_id)

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
        return error_response("Voter ID and password are required")
    if register_voter(voter_id, password):
        return success_response("Registration successful")
    return error_response("Voter ID must be unique.")

# Voter Login API


@app.route("/login", methods=["POST"])
def login_voter():
    data = request.json
    voter_id = data.get("voter_id")
    password = data.get("password")
    if authenticate_voter(voter_id, password):
        session["voter_id"] = voter_id
        return success_response("Login successful")
    return error_response("Invalid voter ID or password", 401)

# Cast Vote


@app.route("/cast-vote", methods=["POST"])
@login_required("voter")
def cast_vote():
    data = request.json
    candidate = data.get("candidate")
    voter_id = session["voter_id"]
    if not candidate:
        return error_response("Candidate name is required")
    if not voting_system.can_vote():
        return error_response("Voting is not currently ongoing.")
    if voting_system.cast_vote(voter_id, candidate):
        return success_response(f"Vote cast for {candidate}")
    return error_response("You have already voted or invalid voter")

# View Results


@app.route("/results", methods=["GET"])
def get_results():
    if not voting_system.can_view_results():
        return error_response("Results are only available after the election ends.", 403)
    try:
        results = voting_system.tally_votes()
        return success_response("Results fetched successfully", results)
    except json.JSONDecodeError as e:
        return error_response(f"Invalid JSON format in block data: {str(e)}", 500)

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
        return success_response("Login successful")
    return error_response("Invalid credentials", 401)

# Admin Dashboard


@app.route("/admin-dashboard")
@login_required("admin")
def admin_dashboard():
    return render_template("admin_dashboard.html")

# View Registered Voters


@app.route("/admin/voters", methods=["GET"])
@login_required("admin")
def view_registered_voters():
    voters = fetch_all_voters()
    return success_response("Fetched registered voters", [{"voter_id": voter.voter_id, "voted": voter.voted} for voter in voters])

# View Election Statistics


@app.route("/admin/statistics", methods=["GET"])
@login_required("admin")
def view_statistics():
    blocks = fetch_all_blocks()
    election_stat = get_election_status()
    results = {}
    try:
        for block in blocks:
            data = json.loads(block.data.replace("'", '"'))
            candidate = voting_system.decrypt_vote(data["vote"])
            results[candidate] = results.get(candidate, 0) + 1
        total_votes = sum(results.values())
        return success_response("Election statistics fetched successfully", {
            "results": results,
            "total_votes": total_votes,
            "election_status": election_stat
        })
    except json.JSONDecodeError as e:
        return error_response(f"Invalid JSON format in block data: {str(e)}", 500)

# Reset Election Results


@app.route("/admin/reset-results", methods=["GET"])
@login_required("admin")
def reset_results():
    voting_system.reset_election()
    db.session.query(Block).delete()
    for voter in Voter.query.all():
        voter.voted = False
    db.session.commit()
    return success_response("Election reset successfully")

# Remove All Voters


@app.route("/admin/remove-voters", methods=["DELETE"])
@login_required("admin")
def remove_all_voters_api():
    remove_all_voters()
    return success_response("All voters removed successfully")

# Audit Blockchain


@app.route("/admin/audit")
@login_required("admin")
def audit_blockchain():
    is_valid = voting_system.blockchain.is_chain_valid()
    message = "Blockchain is valid" if is_valid else "Blockchain is corrupted"
    return success_response(message)

# Start/End Election


@app.route("/admin/start-election", methods=["GET"])
@login_required("admin")
def start_election():
    if voting_system.start_election():
        return success_response("Election started successfully")
    return error_response("Election already ongoing", 400)


@app.route("/admin/end-election", methods=["GET"])
@login_required("admin")
def end_election():
    if voting_system.end_election():
        return success_response("Election ended successfully")
    return error_response("No election is currently ongoing", 400)

# Generate Random Votes


@app.route("/admin/generate-random-votes", methods=["POST"])
@login_required("admin")
def generate_random_votes():
    data = request.json
    num_votes = data.get("numVotes")
    if not num_votes or not str(num_votes).isdigit() or int(num_votes) <= 0:
        return error_response("Invalid number of votes")
    candidates = ["Candidate A", "Candidate B", "Candidate C"]
    for _ in range(int(num_votes)):
        voter_id = f"debug_{int(time.time() * 1000)}"
        password = "debug_password"
        if not register_voter(voter_id, password):
            continue
        candidate = choice(candidates)
        encrypted_vote = voting_system.cipher.encrypt(
            candidate.encode()).decode()
        voting_system.blockchain.add_block(
            {"voter_id": voter_id, "vote": encrypted_vote})
    return success_response(f"{num_votes} random votes generated and voters registered successfully")


if __name__ == "__main__":
    app.run(debug=True)
