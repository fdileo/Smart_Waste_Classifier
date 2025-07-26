import matplotlib.pyplot as plt
from tensorflow import argmax 
from collections import Counter
import numpy as np

from load_data import load_dataset


# Visualizza 3 immagini campione con etichetta dal primo batch del dataset
def show_images(data, class_names, title):
    plt.figure( figsize = (7,4) )
    
    # data.take(1) --> contiene le immagini e le etichette del primo batch 
    for img, labels in data.take(1):
        
        for i in range(3):
            
            axis = plt.subplot(1,3, i+1)
            image = img[i].numpy()
            label = argmax(labels[i]).numpy() # Decodifica da one-hot
            plt.imshow(image)
            plt.title(class_names[label], fontsize = 15)
            plt.axis('off')
        
        plt.suptitle(title, fontsize = 24, color = "#2343f8") 
        plt.show()

# Mostra la distribuzione delle classi per training e test set
def class_distribution(train, test, class_names):
 
    def count_labels(dataset):
        label_counter = Counter()
        for _, labels in dataset:
            label_id = argmax(labels, axis=1).numpy() # Da one-hot a indice
            label_counter.update(label_id)
        return label_counter

    # Conta le etichette nei due set
    train_counts = count_labels(train)
    test_counts = count_labels(test)

    x = np.arange(len(class_names))
    train_values = [train_counts.get(i, 0) for i in range(len(class_names))]
    test_values = [test_counts.get(i, 0) for i in range(len(class_names))]

    # Visualizzazione a barre affiancate
    plt.figure(figsize=(10, 6))
    plt.bar(x - 0.65/2, train_values, 0.65, label='Train', color='skyblue')
    plt.bar(x + 0.65/2, test_values, 0.65, label='Test', color='salmon')

    plt.xticks(x, class_names, rotation=45)
    plt.xlabel("Classi", fontsize = 15)
    plt.ylabel("Numero di immagini")
    plt.title("Distribuzione delle classi: Train vs Test", fontsize = 30)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
'''    
if __name__ == "__main__":
    train, test, class_names = load_dataset()

    show_images(train, class_names, title = 'TRAIN IMAGES')
    show_images(test, class_names, title = 'TEST IMAGES')
    
    class_distribution(train, test, class_names)
'''
    