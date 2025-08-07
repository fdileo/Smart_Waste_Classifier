from flask import Blueprint, render_template, request, flash
from flask_login import current_user
from predict_image import model, predict
from app.database.db import images_collection

from datetime import datetime
from PIL import Image
import os

application = Blueprint('application', __name__)

# Controlla che file sia un'immagine
def check_image(file):
    try:
        img = Image.open(file)
        img.verify() 
        return True
    except (IOError, SyntaxError):
        return False
    

upload_dir = os.path.join('app', 'static', 'uploads')
os.makedirs(upload_dir, exist_ok=True) 

@application.route('/app', methods = ['GET', 'POST'])
def use_app():
    
    prediction = None
    confidence = None
    
    if request.method == 'POST':
        
        if 'image' not in request.files:
            flash("Nessun file selezionato", category="error")
            return render_template("application.html", user=current_user)
        
        # Recupero il file inviati dal form HTML
        image = request.files['image']
        
        # Controllo che il file non sia vuoto
        if image.filename == '':
            flash("File vuoto", category = "error")
        elif not check_image(image):
            flash("Il file inserito non è un'immagine", category = "error")
        
        # Controllo che l'immagine non sia stata inserita in precedenza dallo stesso utente
        elif images_collection.find_one( {"user_id": current_user.id, "filename" : image.filename} ):
            flash("Immagine inserita precedentemente: vedere lo storico", category = "error")
        else:
            image.seek(0) 
            pil_image = Image.open(image)
            prediction, confidence = predict(image = pil_image, model = model)
            
            confidence = round(confidence*100, 2)
            
            images_collection.insert_one({
            "user_id": current_user.id,
            "filename": image.filename,
            "prediction": prediction,
            "confidence" : confidence,
            "timestamp" : datetime.now().strftime('%d/%b/%Y')
            })
            
            upload_path = os.path.join(upload_dir, image.filename)
            pil_image.save(upload_path)  
            
    
            
    history = list(images_collection.find({"user_id": current_user.id}).sort("timestamp", -1)) 

     
    
    return render_template("application.html", 
                           user = current_user, 
                           prediction = prediction, 
                           confidence = confidence,
                           history = history)
    
    
@application.route('/cnn', methods = ['GET'])
def cnn_model_insight():
    
    return render_template('cnn.html', user = current_user)