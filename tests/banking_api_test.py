"""Unit tests for banking app classes and methods."""
import pytest
from banking_api import create_app
from banking_api.model import db


@pytest.fixture(scope='session')
def app():
    """Create app and database for testing."""
    app = create_app('conftest.py')

    # with app.app_context():
    app.app_context().push()
    db.create_all()
    yield app
    db.session.remove()
    db.drop_all()


@pytest.fixture(scope='session')
def client(app):
    """Set up client fixture for testing."""
    return app.test_client()


class TestCustomers():
    """Unit tests for Customers class."""

    @staticmethod
    def test_get(client):
        """Test get method for retreiving all customers."""
        response = client.get("/customers")

        assert 200 == response.status_code

    @staticmethod
    def test_post_customer(client):
        """Test post method for adding a new customer."""
        input_json = {
            "first_name": "thomas",
            "surname": "anderson",
            "identification": "abc"
        }
        response = client.post("/customers", json=input_json)

        assert 201 == response.status_code

    @staticmethod
    def test_post_exist_customer(client):
        """Test post method for adding a customer who already exists."""
        input_json = {
            "first_name": "thomas",
            "surname": "anderson",
            "identification": "abc"
        }

        response = client.post("/customers", json=input_json)
        assert 400 == response.status_code
        assert 'customer already exists' == response.json['FAILED']['message']

    @staticmethod
    def test_post_missing_surname(client):
        """Test post method for adding an account with missing argument."""
        input_json = {
            "first_name": "thomas",
            # "surname": "anderson",
            "identification": "abc"
        }

        response = client.post("/customers", json=input_json)
        assert 400 == response.status_code
        assert ("must provide ['surname'] parameters to "
                "add new customer" == response.json['message'])


class TestAccounts():
    """Unit tests for Accounts class."""

    @staticmethod
    def test_post_account(client):
        """Test post method for adding an account for an existing customer."""
        input_json = {
            "first_name": "thomas",
            "surname": "anderson",
            "identification": "abc",
            "deposit": 200
        }

        response = client.post("/accounts", json=input_json)

        assert 201 == response.status_code

    @staticmethod
    def test_post_no_customer(client):
        """Test post method for adding an account for a non-existent customer."""
        input_json = {
            "first_name": "not",
            "surname": "exist",
            "identification": "abc",
            "deposit": 200
        }

        response = client.post("/accounts", json=input_json)
        assert 400 == response.status_code
        assert ('customer does not exist in database, '
                'add customer first' == response.json['message'])

    @staticmethod
    def test_post_missing_surname_deposit(client):
        """Test post method for adding an account with arguements missing."""
        input_json = {
            "first_name": "not",
            # "surname": "exist"
            "identification": "abc",
            # "deposit": 200
        }

        response = client.post("/accounts", json=input_json)
        assert 400 == response.status_code
        assert ("must provide ['surname', 'deposit'] parameters to "
                "add new account" == response.json['message'])


class TestAccountId():
    """Unit tests for Account class."""

    @staticmethod
    def test_get_exist(client):
        """Test get method for retrieving single account."""
        response = client.get("/account/1")

        assert 200 == response.status_code

    @staticmethod
    def test_get_not_exist(client):
        """Test get method for retrieving a non-existent account."""
        response = client.get("/account/100")

        assert 404 == response.status_code


class TestTransactions():
    """Unit tests for Transactions class."""

    @staticmethod
    def test_post_success(client):
        """Test post method for transferring an amount between accounts."""
        input_json1 = {
            "first_name": "keanu",
            "surname": "reeves",
            "identification": "efg"
        }
        client.post("/customers", json=input_json1)
        input_json2 = {
            "first_name": "keanu",
            "surname": "reeves",
            "identification": "efg",
            "deposit": 200
        }
        client.post("/accounts", json=input_json2)

        response_acc1_before = client.get("/account/1")
        response_acc2_before = client.get("/account/2")
        response = client.post("/transactions", json={"account_id_from": 1,
                                                      "account_id_to": 2,
                                                      "amount": 10})
        response_acc1_after = client.get("/account/1")
        response_acc2_after = client.get("/account/2")

        assert 201 == response.status_code
        assert 'Transaction processed' == response.json['SUCCESS']['message']
        assert 10 == (response_acc1_before.json['SUCCESS']['balance']
                      - response_acc1_after.json['SUCCESS']['balance'])
        assert -10 == (response_acc2_before.json['SUCCESS']['balance']
                       - response_acc2_after.json['SUCCESS']['balance'])

    @staticmethod
    def test_post_nonexistent_account(client):
        """Test post method for transaction with non-existent accounts."""
        response = client.post("/transactions", json={"account_id_from": 101,
                                                      "account_id_to": 102,
                                                      "amount": 10})

        assert 400 == response.status_code
        assert 'Check account id' == response.json['message']

    @staticmethod
    def test_post_amount_negative(client):
        """Test post method for transaction with negative amount."""
        response = client.post("/transactions", json={"account_id_from": 1,
                                                      "account_id_to": 2,
                                                      "amount": -10})

        assert 400 == response.status_code
        assert 'amount must be positive and not zero' == response.json['message']

    @staticmethod
    def test_post_missing_arg(client):
        """Test post method for transaction with missing argument."""
        response = client.post("/transactions", json={"account_id_from": 1,
                                                      "amount": 10})

        assert 400 == response.status_code
        assert ("must provide ['account_id_to'] parameters to "
                "process transaction" == response.json['message'])


class TestAccountTransactions():
    """Unit tests for AccountTransactions class."""

    @staticmethod
    def test_get_exist(client):
        """Test get method for retrieving transation history for a single account."""
        response = client.get("/account/1")

        assert 200 == response.status_code

    @staticmethod
    def test_get_not_exist(client):
        """Test get method for retrieving transation history for non-existent account."""
        response = client.get("/account/100")

        assert 404 == response.status_code
