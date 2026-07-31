from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='customer')  # customer, agent, admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    policies = db.relationship('Policy', backref='owner', lazy=True)


class Policy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    coverage_type = db.Column(db.String(50), nullable=False)  # e.g. auto, home, life
    coverage_amount = db.Column(db.Float, nullable=False)
    premium = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='active')  # active, cancelled, expired

    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=True)

    claims = db.relationship('Claim', backref='policy', lazy=True)


class Claim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    policy_id = db.Column(db.Integer, db.ForeignKey('policy.id'), nullable=False)

    description = db.Column(db.Text, nullable=False)
    amount_requested = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, under_review, approved, denied
    triage_result = db.Column(db.String(50), nullable=True)  # for the AI triage feature later

    filed_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime, nullable=True)


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    policy_id = db.Column(db.Integer, db.ForeignKey('policy.id'), nullable=False)
    claim_id = db.Column(db.Integer, db.ForeignKey('claim.id'), nullable=True)  # null if it's a premium payment

    amount = db.Column(db.Float, nullable=False)
    payment_type = db.Column(db.String(20), nullable=False)  # premium, payout
    status = db.Column(db.String(20), default='completed')  # pending, completed, failed

    created_at = db.Column(db.DateTime, default=datetime.utcnow)