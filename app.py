from flask import Flask, render_template
from flask_cors import CORS
from flask_migrate import Migrate

from models import db  # Import your database setup from models.py
from note_routes import note_bp  # Import your note routes blueprint
from user_routes import user_bp  # Import your user routes blueprint

app = Flask(__name__)
# Allow CORS for all routes
CORS(app)

# Set the secret key for the Flask app
app.secret_key = 'username'

# Configure your database - Replace with your database configuration
# app.config['SQLALCHEMY_DATABASE_URI'] = ('postgresql://iwahvsqk:mhm8Bk6vYQISTqIvsu8KczV45JE-2Fqp@mel.db.elephantsql'
#                                          '.com/iwahvsqk')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:3000/Note+'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)
migrate = Migrate(app, db)

# Register blueprints for user and note routes
app.register_blueprint(user_bp)
app.register_blueprint(note_bp)


@app.route('/')
def index():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
