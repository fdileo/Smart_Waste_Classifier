from flask import Flask
from .config import Configuration
from app.database import db
from flask_login import LoginManager
from bson import ObjectId


def create_app():
    
    # Crea un'istanza dell'applicazione Flask e carica le configurazioni
    # (es. SECRET_KEY, URI del database, ecc.) dalla classe Configuration
    app = Flask(__name__)
    app.config.from_object(Configuration)
    
    # Inizializzo il database attraverso la funzione init_db nella cartella database/db.py
    db.init_db(app)
    
    # Importazione dei blueprint
    from .auth.routes import auth
    from .main.routes import main
    from .use_app.routes import application
    
    # Collega i blueprint all'app principale
    app.register_blueprint(main, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')
    app.register_blueprint(application, url_prefix = '/')
    
    # Importa la classe User, necessaria per gestire gli utenti
    from app.database.users import User
    
    # Crea un'istanza di LoginManager che gestisce l'autenticazione degli utenti
    login_manager = LoginManager()
    # Indica quale "view" usare quando un utente non autenticato tenta di accedere ad una pagina protetta
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)    # Collega il LoginManager all'app Flask
    
    # Funzione che Flask-Login userà per caricare un utente dal database
    # a partire dal suo ID salvato nella sessione  
    @login_manager.user_loader
    def load_user(user_id):
        
        # Cerca nel database l'utente con l'_id corrispondente
        user_data = db.users_collection.find_one({"_id": ObjectId(user_id)})
        
         # Se l'utente esiste, crea e restituisce un oggetto User
        if user_data:
            return User(user_data)
        
         # Altrimenti, ritorna None (utente non trovato)
        return None
    
    
    return app 