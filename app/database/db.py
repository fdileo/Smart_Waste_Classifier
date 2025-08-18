from pymongo import MongoClient

# Variabili globali per gestire la connessione e le collection del database
mongo = None
db = None
users_collection = None
images_collection = None

def init_db(app):

    """
    Inizializza la connessione al database MongoDB utilizzando la MONGO_URI
    definita nelle configurazioni Flask.
    Imposta variabili globali per accedere facilmente al database e alle collection.
    """
    
    global mongo, db, users_collection, images_collection
    
    # Crea il client MongoDB utilizzando la URI salvata nella config dell'app Flask
    mongo = MongoClient(app.config['MONGO_URI'])
    db = mongo['my_Mongodb']            # Accede al database
    users_collection = db['users']      # Accede alla collection users
    images_collection = db['images']    # Accede alla collection images