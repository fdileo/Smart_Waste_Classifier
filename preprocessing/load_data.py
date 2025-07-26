from keras.utils import image_dataset_from_directory
from keras.layers import Rescaling

# Dimensioni target delle immagini
img_height = 224
img_width = 224


# Carica il dataset dei rifiuti, lo divide in train/test, normalizza i pixel
# Se verbose=True, stampa statistiche utili
def load_dataset(verbose = False):
    
    # 80% delle immagini nel training set
    train = image_dataset_from_directory('data/raw',
                                         validation_split = 0.2,
                                         subset = "training",
                                         seed = 42,
                                         image_size = (img_height, img_width),
                                         batch_size = 64, 
                                         label_mode = "categorical")
    
    # 20% delle immagini nel test set
    test = image_dataset_from_directory('data/raw',
                                        validation_split = 0.2,
                                        subset = "validation",
                                        seed = 42,
                                        image_size = (img_height, img_width),
                                        batch_size = 64,
                                        label_mode = "categorical")
    
    # Etichette di classe in ordine alfabetico
    class_names = train.class_names
    print(f"Classi --> {class_names}")
    
    # Normalizzazione: pixel da [0,255] a [0,1]
    normalization = Rescaling(1./255)
    
    # Applica la normalizzazione ai dati
    train = train.map(lambda x,y: (normalization(x),y) )
    test = test.map(lambda x,y: (normalization(x),y) )
    
    if verbose:
        print("\n📊 Summary Dataset:\n")
        
        total_train_images = sum([images.shape[0] for images, _ in train])
        total_test_images = sum([images.shape[0] for images, _ in test])

        print(f"  Dimensioni immagine: ({img_height}, {img_width}, 3)")
        print( "  Batch size: 64")
        print(f"  Numero classi: {len(class_names)}")
        print(f"  Immagini totali: {total_train_images + total_test_images}")
        print(f"  Immagini di training: {total_train_images}")
        print(f"  Immagini di test: {total_test_images}")
    
    return train, test, class_names 