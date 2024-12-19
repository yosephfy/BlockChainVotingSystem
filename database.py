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

# Database Utility Functions


def register_voter(voter_id, password):
    if Voter.query.filter_by(voter_id=voter_id).first():
        return False
    hashed_password = generate_password_hash(password)
    voter = Voter(voter_id=voter_id, password=hashed_password)
    db.session.add(voter)
    db.session.commit()
    return True


def authenticate_voter(voter_id, password):
    voter = Voter.query.filter_by(voter_id=voter_id).first()
    if voter and check_password_hash(voter.password, password):
        return True
    return False


def mark_voter_as_voted(voter_id):
    voter = Voter.query.filter_by(voter_id=voter_id).first()
    if voter:
        voter.voted = True
        db.session.commit()


def add_block_to_db(index, timestamp, data, previous_hash, hash, nonce):
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
    return Voter.query.all()


def fetch_all_blocks():
    return Block.query.all()
