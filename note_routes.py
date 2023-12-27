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


@note_bp.route('/notes/edit/<int:note_id>', methods=['GET', 'PUT'])
def edit_note(note_id):
    if request.method == 'PUT':
        data = request.json  # Assuming JSON data from the React component

        # Check if the required fields are present in the request
        if 'title' not in data or 'content' not in data or 'user_id' not in data:
            return jsonify({'error': 'Please provide title, content, and user_id'}), 400

        user_id = data['user_id']  # Get the user ID from the request

        # Get the existing note from the database using the note_id
        note = Note.query.filter_by(id=note_id).first()

        # Check if the note exists
        if not note:
            return jsonify({'error': 'Note not found'}), 404

        # Update the note details
        note.title = data['title']
        note.content = data['content']
        note.user_id = user_id  # Update the user ID if needed

        # Commit changes to the database
        db.session.commit()

        return jsonify({'message': 'Note updated successfully'}), 200

    elif request.method == 'GET':  # Handle GET request separately
        note = Note.query.filter_by(id=note_id).first()

        if note:
            # Prepare the note data to be sent back as a response
            note_data = {
                'id': note.id,
                'title': note.title,
                'content': note.content,
                'user_id': note.user_id
                # Include more fields as needed
            }
            return jsonify({'note': note_data}), 200
        else:
            return jsonify({'error': 'Note not found'}), 404

    return jsonify({'error': 'Method not allowed'}), 405  # Handling other HTTP methods


@note_bp.route('/notes/delete/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    if request.method == 'DELETE':
        # Get the note by ID
        note = Note.query.get(note_id)

        if not note:
            return jsonify({'error': 'Note not found'}), 404

        # Delete the note from the database
        db.session.delete(note)
        db.session.commit()

        return jsonify({'message': 'Note deleted successfully'}), 200

    return jsonify({'error': 'Method not allowed'}), 405
