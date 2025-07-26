from keras import layers, Sequential

# Restituisce uno strato di data augmentation da inserire nel modello
# Parametri personalizzabili: rotazione, zoom, contrasto, traslazione
def data_augmentation(value_rotation = 0.1, value_zoom = 0.1, 
                      value_contrast = 0.1, value_translation = 0.1):
    
    return Sequential([
        layers.RandomFlip("horizontal"),    # Flip orizzontale casuale
        layers.RandomRotation(value_rotation),    # Rotazione casuale      
        layers.RandomZoom(value_zoom),    # Zoom casuale
        layers.RandomContrast(value_contrast),   # Variazione constrasto
        layers.RandomTranslation(value_translation, value_translation),    # Spostamento (x,y)
        layers.RandomBrightness(0.2),    # Luminosità casuale
        layers.GaussianNoise(0.05)     # Rumore gaussiano
    ])