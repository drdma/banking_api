"""Run file for flask app."""
from banking_api import create_app
from banking_api.model import db

app = create_app('config.py')

# initialise database
app.app_context().push()
db.create_all()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=False)
