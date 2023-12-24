from flask import Blueprint, request, jsonify, session

from models import User, Note, db

user_bp = Blueprint('user_bp', __name__, url_prefix='/user')


@user_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json  # Assuming JSON data from the frontend

    # Check if username, email, and password are provided
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Please provide username, email, and password'}), 400

    username = data['username']
    email = data['email']
    password = data['password']

    # Check if the username already exists in the database
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'error': 'Username already exists'}), 409  # HTTP 409 Conflict

    # Create a new user
    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Signup successful'}), 200


@user_bp.route('/login', methods=['POST'])
def login():
    data = request.json  # Assuming JSON data from the frontend

    # Check if username and password are provided
    if 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Please provide username and password'}), 400

    username = data['username']
    password = data['password']

    # Query the database for the user
    user = User.query.filter_by(username=username).first()

    if user and user.password == password:
        # User exists and password matches
        session['user_id'] = int(user.id)  # Set the user ID in the session
        print(user.id)
        return jsonify({'user_id': user.id, 'message': 'Login successful'}), 200
    else:
        # Invalid credentials
        return jsonify({'error': 'Invalid username or password'}), 401


@user_bp.route('/dashboard', methods=['GET'])
def user_dashboard():
    user_id = request.headers.get('User-Id')  # Retrieve user_id from headers
    print(user_id)  # For debugging purposes

    if user_id:
        # Proceed with fetching notes or other user-specific data using user_id
        user_notes = Note.query.filter_by(user_id=user_id).all()

        # Construct a list of note data
        notes_data = [{
            'id': note.id,
            'title': note.title,
            'content': note.content,
            'user_id': note.user_id
            # Add more fields as needed
        } for note in user_notes]

        return jsonify({'notes': notes_data}), 200
    else:
        return jsonify({'error': 'Unauthorized'}), 401
