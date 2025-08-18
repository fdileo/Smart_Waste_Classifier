from flask import Blueprint, render_template
from flask_login import current_user

# Crea un blueprint chiamato main che gestirà l'homepage dell'applicazione per utenti non loggati
main = Blueprint('main', __name__)     

@main.route('/')
def home():
    return render_template("home.html", user = current_user)