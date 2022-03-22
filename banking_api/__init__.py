"""Script containing Flask app to create banking API."""

from flask import Flask
from flask_restful import Api
import os
import markdown


def create_app(config_filename):
    """Create flask app from config and blueprints."""
    # create Flask instance
    app = Flask(__name__)

    app.config.from_pyfile(config_filename)

    from banking_api.model import db
    db.init_app(app)

    @app.route("/")
    def index():
        """Show API documentation on homepage."""
        with open(os.path.dirname(app.instance_path) + '/README.md', 'r') as md_file:

            content = md_file.read()

            return markdown.markdown(content)

    from banking_api.routes import (api_bp, Customers, Accounts, Account_id,
                                    Transactions, AccountTransactions)

    api = Api(api_bp)
    api.add_resource(Customers, '/customers')
    api.add_resource(Accounts, '/accounts')
    api.add_resource(Account_id, '/account/<int:account_id>')
    api.add_resource(Transactions, '/transactions')
    api.add_resource(AccountTransactions, '/account/<int:account_id>/transactions')

    app.register_blueprint(api_bp)

    return app
