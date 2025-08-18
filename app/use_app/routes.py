from flask import Blueprint, render_template, request, flash
from flask_login import current_user
from predict_image import model, predict
from app.database.db import images_collection

from datetime import datetime
from PIL import Image       # Libreria PIL ottima per lavorare con le immagini
import os


# Crea un blueprint chiamato application che gestisce le funzionalità dell'applicazione
# per un utente loggato
application = Blueprint('application', __name__)


def check_image(file):
    
    """
    Verifica che il file in input sia effettivamente un'immagine.
    Utilizza la libreria PIL per tentare di aprirlo e validarlo.
    Restituisce True se è valido, False altrimenti.
    """
    
    try:
        img = Image.open(file)
        img.verify() 
        return True
    except (IOError, SyntaxError):
        return False
    

# Crea, se non esiste, la cartella uploads all'interno di app/static
upload_dir = os.path.join('app', 'static', 'uploads')
os.makedirs(upload_dir, exist_ok=True) 


# Endopoint per l'APP
@application.route('/app', methods = ['GET', 'POST'])
def use_app():
    
    prediction = None
    confidence = None
    
    if request.method == 'POST':
        
        # Controlla che sia stato inviato un file
        if 'image' not in request.files:
            flash("Nessun file selezionato", category="error")
            return render_template("application.html", user=current_user)
        
        # Recupera il file inviati dal form HTML
        image = request.files['image']
        
        if image.filename == '':    # Controlla che il file non sia vuoto
            flash("File vuoto", category = "error")
        elif not check_image(image):    # Controlla che il file inserito sia un'immagine
            flash("Il file inserito non è un'immagine", category = "error")
        
        # Evita di caricare due volte la stessa immagine per lo stesso utente
        elif images_collection.find_one( {"user_id": current_user.id, "filename" : image.filename} ):
            flash("Immagine inserita precedentemente: vedere lo storico", category = "error")
        else:
            image.seek(0) 
            pil_image = Image.open(image)       # Apre l'immagine con la libreria PIL
            
            # Predizione tramite il modello di deep learning
            prediction, confidence = predict(image = pil_image, model = model)
            
            confidence = round(confidence*100, 2)
            
            # Salva i metadati dell'immagine e la predizione nel database
            images_collection.insert_one({
                "user_id": current_user.id,
                "filename": image.filename,
                "prediction": prediction,
                "confidence" : confidence,
                "timestamp" : datetime.now().strftime('%d/%b/%Y')
            })
            
            # Salva l'immagine inserita nella cartella uploads
            upload_path = os.path.join(upload_dir, image.filename)
            pil_image.save(upload_path)  
            
    
    # Recupera lo storico delle immagini caricate dall'utent
    history = list(images_collection.find({"user_id": current_user.id}).sort("timestamp", -1)) 

     
    
    return render_template("application.html", 
                           user = current_user, 
                           prediction = prediction, 
                           confidence = confidence,
                           history = history)
    
    
# Endopoint per visualizzare il MODELLO DI DEEP LEARNING
@application.route('/cnn', methods = ['GET'])
def cnn_model_insight():
    
    return render_template('cnn.html', user = current_user)