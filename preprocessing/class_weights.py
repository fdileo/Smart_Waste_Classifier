from tensorflow import argmax
from collections import Counter

# Calcola i pesi per ciascuna classe in base alla loro frequenza nel dataset
# Utile per compensare squilibri durante l'addestramento (es. con class_weight in model.fit)
def compute_class_weight(dataset, class_names):
    
    total = 0
    counter = Counter()
    
    for _, labels in dataset:
        class_id = argmax(labels, axis = 1).numpy() # Estrai indici da one-hot
        counter.update(class_id)
        total += len(class_id) # Conta le immagini totali da utilizzare nella formula dei pesi
        
    weights = dict()
    len_class = len(class_names)
    
    for i, name in enumerate(class_names):
        c = counter[i]
        
        #Formula per il calcolo dei pesi: inversamente proporzionale alla loro frequenza del dataset.
        weights[i] =  total / (len_class*c)
        
    
    return weights

'''
if __name__ == '__main__':
    
    from load_data import load_dataset
    
    test, _, class_names = load_dataset()
    compute_class_weight(dataset=test, class_names = class_names)
'''