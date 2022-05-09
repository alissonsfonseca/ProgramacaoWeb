import json
from flask import Blueprint, flash, jsonify, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from website.models.tables import Note
from website import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Nota muito curta', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Nota adicionada', category= 'success')

    return render_template("home.html", user=current_user)

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

@views.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    nota_editar = Note.query.get(id)
    if request.method == 'POST':
        nota_editar.data = request.form['nota']
        try:
            db.session.commit()
            return redirect(url_for('views.home'))
        except:
            return "Ocorreu um erro ao editar"
    else:
        return render_template("editar.html", user=current_user, nota_editar = nota_editar)
