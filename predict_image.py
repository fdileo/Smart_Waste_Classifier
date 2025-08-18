from keras.models import load_model
import numpy as np

model = load_model('best_model.h5') # Carico il modello migliore di CNN per la classificazione di rifiuti
class_names = ['vetro', 'organico', 'carta', 'plastica', 'indifferenziata']

def predict(image, model):
    
    '''
    
    INPUT
    - **image**: immagine PIL da classificare
    - **model**: modello di deep_learning addestrato
    
    OUTPUT
    - **class_hat**: etichetta della classe predetta
    - **confidence**: probabilità associata alla classe predetta con 2 cifre decimali
    
    '''
    
    
    image = image.convert('RGB')    # Conversione in scala RGB
    img = image.resize( (224,224) )     # Ridimensiona a 224 x 224 pixel
    img_array = np.array(img) / 255.0  # Converte l'immagine in array NumPy e normalizza i valori [0,255] → [0,1]
    
    # Aggiunge dimensione per essere compatibile con il modello 'best_model.h5'
    # (224, 224, 3) --> (1, 224, 224, 3) per rappresentare il batch
    img_array = np.expand_dims(img_array, axis = 0)     
    
    # Predizione e probabilità di classificazione
    y_hat_prob = model.predict(img_array)
    y_hat = np.argmax(y_hat_prob)
    class_hat = class_names[y_hat]
    
    return class_hat, float(np.max(y_hat_prob))
    
    