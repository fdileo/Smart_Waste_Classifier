from keras.models import load_model
import numpy as np

model = load_model('best_model.h5')
class_names = ['vetro', 'organico', 'carta', 'plastica', 'indifferenziata']

def predict(image, model):
    
    image = image.convert('RGB')
    
    img = image.resize( (224,224) )
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis = 0)
    
    y_hat_prob = model.predict(img_array)
    y_hat = np.argmax(y_hat_prob)
    class_hat = class_names[y_hat]
    
    return class_hat, float(np.max(y_hat_prob))
    
    