from Website.models import Note, Url
from Website.auth import login
from flask import Blueprint, redirect, render_template, request, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from .models import Note, db
import json
import random
import string

views = Blueprint("views", __name__)

@views.route('/home', methods=["GET", "POST"])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash("Note is too short", category="error")
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note Added!", category="success")
        

    return render_template("home.html", user=current_user)

@views.route('/', methods=["GET", "POST"])
def home_page():
    if request.method == 'POST':
        def generate_url():
            random_string = ''.join(random.choice(string.ascii_letters) for i in range(10))
            if not Url.query.get(random_string):
                return random_string
        tinyurl = generate_url()
        data = request.form.get('data')

        if len(str(data)) < 1:
            flash('Link is too short', category='error')
        else:
            try:
                new_link = Url(data=data, converted_link=tinyurl)
                db.session.add(new_link)
                db.session.commit()
            except:
                flash('Attempt failed. Please try again', category='error')
            flash("It worked", category='success')

    return render_template('shortener.html', user=current_user)

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