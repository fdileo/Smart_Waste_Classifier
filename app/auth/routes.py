from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from app.database.db import users_collection
from app.database.users import User
from flask_login import login_user, login_required, logout_user, current_user

import time

auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        
        # Recupero i diversi valori dei campi inviati dal form HTML
        email = request.form["email"]
        password = request.form["password"]
        
        # Controllo se esiste un utente con le credenziali inserite
        user = users_collection.find_one({"email" : email})
        if user is None or not check_password_hash(user["password"], password):
            flash("Email o password errati. Riprovare", category = "error")
        else:
            flash("Autenticazione completata.", category = "success")
            login_user(User(user), remember = True)
            return redirect(url_for('main.home'))
            
            
            
    return render_template("login.html", user = current_user)

@auth.route('/logout')
@login_required
def logout():
    
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods = ['GET', 'POST'])
def sign_up():
    
    if request.method == 'POST':
        
        # Recupero i diversi valori dei campi inviati dal form HTML
        email = request.form['email']
        name = request.form['name']
        passw1 = request.form['password_insert']
        passw2 = request.form['password_ver']
        
        # Controllo che l'indirizzo email inserito non sia già presente nel database
        if users_collection.find_one({"email": email}):
            flash("Indirizzo email già presente, prova un altro.", category = "error")
            
        # Controlli sui vari campi: in caso di errore, lancia un messaccio con flash
        elif len(email) < 4:
            flash("L'email deve contenere almeno 4 caratteri.", category = "error")
        elif len(name) < 2:
            flash("Nome troppo corto.", category = "error")
        elif len(passw1) < 7:
            flash("La password utilizzata deve contenere almeno 7 caratteri", category = "error")
        elif passw1 != passw2:
            flash("Le passwords non corrispondono!", category = "error")  
        else:
            flash("Account creato con successo.", category = "success")
            # La password viene criptata per motivi di sicurezza
            hashed_password = generate_password_hash(passw1)
            # Inserisco i dati nella collection users
            users_collection.insert_one({"email" : email,
                                         "nome": name,
                                         "password" : hashed_password})
            
            new_user = users_collection.find_one({"email" : email})
            login_user(User(new_user), remember = True)
            return redirect(url_for('auth.login'))
        
    
    return render_template("sign_up.html", user = current_user)