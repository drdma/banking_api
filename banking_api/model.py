"""Script contains data models used in API database."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Customer(db.Model):
    """Create Customer class data model."""

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    identification = db.Column(db.String(20), nullable=False)
    account = db.relationship('Account', backref='customer', lazy=True)


class Account(db.Model):
    """Create Account class data model."""

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    balance = db.Column(db.Float, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'),
                            nullable=False)


class Transaction(db.Model):
    """Create Transaction class data model."""

    uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    account_id_from = db.Column(db.Integer, nullable=False)
    account_id_to = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    transaction_timestamp = db.Column(db.String(50), nullable=False)
