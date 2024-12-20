from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# Voter Model


class Voter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    voter_id = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    voted = db.Column(db.Boolean, default=False)

# Block Model


class Block(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.String(100), nullable=False)
    data = db.Column(db.Text, nullable=False)
    previous_hash = db.Column(db.String(64), nullable=False)
    hash = db.Column(db.String(64), nullable=False)
    nonce = db.Column(db.Integer, nullable=False)

# Election Status Model


class ElectionStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # "not_started", "ongoing", "ended"
    status = db.Column(db.String(20), nullable=False)

# Database Utility Functions


def get_election_status():
    """
    Retrieves the current election status from the database.
    Initializes with 'not_started' if no record exists.
    """
    status_record = ElectionStatus.query.first()
    if not status_record:
        status_record = ElectionStatus(status="not_started")
        db.session.add(status_record)
        db.session.commit()
    return status_record.status


def update_election_status(new_status):
    """
    Updates the election status in the database.
    Creates a new status record if none exists.
    """
    status_record = ElectionStatus.query.first()
    if not status_record:
        status_record = ElectionStatus(status=new_status)
        db.session.add(status_record)
    else:
        status_record.status = new_status
    db.session.commit()


def register_voter(voter_id, password):
    """
    Registers a new voter with a hashed password.
    Returns False if the voter ID is not unique.
    """
    if Voter.query.filter_by(voter_id=voter_id).first():
        return False
    hashed_password = generate_password_hash(password)
    voter = Voter(voter_id=voter_id, password=hashed_password)
    db.session.add(voter)
    db.session.commit()
    return True


def authenticate_voter(voter_id, password):
    """
    Authenticates a voter by verifying the hashed password.
    Returns True if authentication is successful, False otherwise.
    """
    voter = Voter.query.filter_by(voter_id=voter_id).first()
    return voter and check_password_hash(voter.password, password)


def mark_voter_as_voted(voter_id):
    """
    Marks a voter as having voted.
    """
    voter = Voter.query.filter_by(voter_id=voter_id).first()
    if voter:
        voter.voted = True
        db.session.commit()


def add_block_to_db(index, timestamp, data, previous_hash, hash, nonce):
    """
    Adds a new block to the database.
    """
    block = Block(
        index=index,
        timestamp=timestamp,
        data=data,
        previous_hash=previous_hash,
        hash=hash,
        nonce=nonce
    )
    db.session.add(block)
    db.session.commit()


def fetch_all_voters():
    """
    Fetches all voters from the database.
    """
    return Voter.query.all()


def fetch_all_blocks():
    """
    Fetches all blocks from the database.
    """
    return Block.query.all()


def reset_votes():
    """
    Resets all voters' voted status and deletes all blocks from the database.
    """
    voters = Voter.query.all()
    for voter in voters:
        voter.voted = False
    db.session.query(Block).delete()
    db.session.commit()


def remove_all_voters():
    """
    Deletes all voters from the database.
    """
    db.session.query(Voter).delete()
    db.session.commit()


def get_voter_by_id(voter_id):
    """
    Retrieves a voter by their voter ID.
    Returns a dictionary containing voter details or None if the voter doesn't exist.
    """
    voter = Voter.query.filter_by(voter_id=voter_id).first()
    if voter:
        return {"voter_id": voter.voter_id, "voted": voter.voted}
    return None
