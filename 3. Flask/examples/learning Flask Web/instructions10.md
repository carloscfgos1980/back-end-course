# Add functionality for the notes in views.py

1. Import modules:
from flask import Blueprint, render_template, request, flash, jsonify
from .models import Note
from . import db
import json

2. Add new note
2.1 Add method to home page: 
@views.route('/', methods=['GET', 'POST'])

2.2 Make home page required to be logged in:
@login_required

2.3 Get the note from the form:
    if request.method == 'POST':
        note = request.form.get('note')
* I can access the content in the text area by the id (note)

2.4 that there is some input text:
        if len(note) < 1:
            flash('Note is too short!', category='error')

2.5 Add the note:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

* The whole thing looks like this:
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

3. DELETE note
3.1 Create the route, just with post method:
@views.route('/delete-note', methods=['POST'])

3.2 Create the delete function:
def delete_note():

3.3 load the note and get the note:
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)

3.4 If the note exists, the DELETE:
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

3.5 Return and empty object
    return jsonify({})

* The whole thing looks like this:
@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


## THE END
