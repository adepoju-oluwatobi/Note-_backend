from flask import Blueprint, jsonify, request

from models import db, Note

note_bp = Blueprint('note_bp', __name__, url_prefix='/user')


@note_bp.route('/notes/add', methods=['POST'])
def add_note():
    if request.method == 'POST':
        data = request.json  # Assuming JSON data from the React component

        # Check if the required fields are present in the request
        if 'title' not in data or 'content' not in data or 'user_id' not in data:
            return jsonify({'error': 'Please provide title, content, and user_id'}), 400

        user_id = data['user_id']  # Get the user ID from the request
        print(user_id)

        # Create a new Note object
        new_note = Note(
            title=data['title'],
            content=data['content'],
            user_id=user_id  # Assign the user ID to the note
        )

        # Add the new note to the database
        db.session.add(new_note)
        db.session.commit()

        return jsonify({'message': 'Note added successfully'}), 200

    return jsonify({'error': 'Method not allowed'}), 405  # Handling other HTTP methods
