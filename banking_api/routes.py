"""Script contains all the routes of banking API."""
from flask import Blueprint, request
from banking_api.model import db, Customer, Account, Transaction
from flask_restful import Resource
import uuid
from datetime import datetime

api_bp = Blueprint('routes', __name__)


class Customers(Resource):
    """Create Customers class."""

    def get(self):
        """Retreive customers from customers database and display all."""
        customers = Customer.query.all()

        output = []
        for c in customers:
            customer_data = {
                'id': c.id,
                'name': c.name,
                'identification': c.identification}

            output.append(customer_data)

        return {'customers': output}, 200

    def post(self):
        """Register new customer to database by name."""
        try:
            # get request inputs
            name = f"{request.json['first_name'].strip()} "\
                   f"{request.json['surname'].strip()}"

            new_customer = Customer(
                name=name.title(),
                identification=request.json['identification'])

            # check if customer already exists
            customer_exist = db.session.query(Customer).\
                filter(Customer.name == new_customer.name).\
                filter(Customer.identification == new_customer.identification).\
                first()

            # add to database if doesn't exists
            if not customer_exist:
                db.session.add(new_customer)
                db.session.commit()

                return {
                    'SUCCESS': {
                        'message': 'customer added',
                        'id': new_customer.id,
                        'name': new_customer.name,
                        'identification': new_customer.identification
                    }
                }, 201
            else:
                return {
                    'FAILED': {
                        'message': 'customer already exists',
                        'id': customer_exist.id,
                        'name': customer_exist.name,
                        'identification': customer_exist.identification
                    }
                }, 400

        except Exception:
            # create custom error messages
            content = request.get_json()

            required_args = ['first_name', 'surname', 'identification']
            missing_args = [x for x in required_args if content.get(x) is None]

            if missing_args:
                return {'message': f'must provide {missing_args} '
                        'parameters to add new customer'}, 400

            else:
                return {'message': 'Unknown error'}, 400


class Accounts(Resource):
    """Create Accounts class for creating a new account."""

    def post(self):
        """Create new account with customer's name, identification and initial deposit."""
        try:
            # get request inputs
            name = f"{request.json['first_name'].strip()} "\
                   f"{request.json['surname'].strip()}"

            iden = f"{request.json['identification'].strip()}"
            deposit = request.json['deposit']

            # check if customer already exists
            customer_exist = db.session.query(Customer).\
                filter(Customer.name == name.title()).\
                filter(Customer.identification == iden).\
                first()

            # create new account if customer exists
            if customer_exist:

                new_account = Account(
                    balance=deposit,
                    customer_id=customer_exist.id
                )

                db.session.add(new_account)
                db.session.commit()

                return {'SUCCESS': {
                    'message': 'New account added',
                    'id': new_account.id,
                    'balance': new_account.balance,
                    'customer_id': new_account.customer_id,
                    'name': customer_exist.name
                }}, 201

            elif not customer_exist:
                return {'message': 'customer does not exist in database, '
                        'add customer first'}, 400

        except Exception:
            # create custom error messages
            content = request.get_json()

            required_args = ['first_name', 'surname', 'identification', 'deposit']
            missing_args = [x for x in required_args if content.get(x) is None]

            if missing_args:
                return {'message': f'must provide {missing_args} '
                        'parameters to add new account'}, 400

            else:
                return {'message': 'Uknown error'}, 400


class Account_id(Resource):
    """Create Account class for getting individual accounts."""

    def get(self, account_id):
        """Retreive single account balance by its id."""
        account = Account.query.get_or_404(account_id)

        return {'SUCCESS': {
                'message': f'account {account.id} retreived',
                'balance': account.balance}}


class Transactions(Resource):
    """Create Transaction class for transferring between accounts."""

    def post(self):
        """Create new transaction."""
        try:
            # get request inputs
            account_id_from = request.json['account_id_from']
            account_id_to = request.json['account_id_to']
            amount = request.json['amount']
            transaction_uuid = str(uuid.uuid4())
            transaction_timestamp = str(datetime.now())

            # process transaction if amount is not zero or negative
            if amount <= 0:
                return {'message': 'amount must be positive and not zero'}, 400
            else:
                account_from_exist = Account.query.get(account_id_from)
                account_to_exist = Account.query.get(account_id_to)

                # update account records if both accounts exists,
                # and add transaction to database
                if account_from_exist and account_to_exist:

                    account_from_exist.balance = account_from_exist.balance - amount
                    account_to_exist.balance = account_to_exist.balance + amount
                    db.session.commit()

                    new_transaction = Transaction(
                        uuid=transaction_uuid,
                        account_id_from=account_id_from,
                        account_id_to=account_id_to,
                        amount=amount,
                        transaction_timestamp=transaction_timestamp
                    )

                    db.session.add(new_transaction)
                    db.session.commit()

                    return {'SUCCESS': {
                            'message': 'Transaction processed',
                            'uuid': new_transaction.uuid,
                            'account_id_from': new_transaction.account_id_from,
                            'account_id_to': new_transaction.account_id_to,
                            'amount': new_transaction.amount,
                            'transaction_timestamp': new_transaction.transaction_timestamp
                            }}, 201
                else:
                    return {'message': 'Check account id'}, 400

        except Exception:
            # create custom error messages
            content = request.get_json()

            required_args = ['account_id_from', 'account_id_to', 'amount']
            missing_args = [x for x in required_args if content.get(x) is None]

            if missing_args:
                return {'message': f'must provide {missing_args} '
                        'parameters to process transaction'}, 400

            else:
                return {'message': 'Uknown error'}, 400


class AccountTransactions(Resource):
    """Create AccountTransactions class for getting transaction history for an account."""

    def get(self, account_id):
        """Retreive transaction history for a given account."""
        account_exist = Account.query.get(account_id)

        # if account exists, filter transaction database by the account id
        if account_exist:

            transaction_history = Transaction.query.filter(
                (Transaction.account_id_from == account_id)
                | (Transaction.account_id_to == account_id))

            output = []
            for t in transaction_history:
                transaction_data = {
                    'uuid': t.uuid,
                    'account_id_from': t.account_id_from,
                    'account_id_to': t.account_id_to,
                    'amount': t.amount,
                    'transaction_timestamp': t.transaction_timestamp
                }

                output.append(transaction_data)

            return {'transactions': output}, 200
        else:
            return {'message': 'Check account id'}, 404
