from unicodedata import category
from flask import Blueprint, render_template, request, flash, redirect, url_for
from website.models.tables import User
from werkzeug.security import generate_password_hash, check_password_hash
from website import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST']) 
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('senha')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logado com sucesso!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Senha incorreta, tente novamente!', category='error')
        else:
            flash('Email inexistente', category='error')
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        primeiro_nome = request.form.get('primeiroNome')
        senha1 = request.form.get('senha1')
        senha2 = request.form.get('senha2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email já existente', category='error')
        elif len(email) < 4:
            flash('Email tem que ter 4 letras ou mais', category='error')
        elif len(primeiro_nome) < 2:
            flash('Primeiro nome tem que ter 2 letras ou mais', category='error')
        elif senha1 != senha2:
            flash('Senhas diferentes', category='error')
        elif len(senha1) < 4:
            flash('Senha tem que ter 4 letras ou mais', category='error')
        else:
            new_user = User(email=email, primeiro_nome=primeiro_nome, password=generate_password_hash(senha1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Conta criada', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)