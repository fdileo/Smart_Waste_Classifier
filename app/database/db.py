from pymongo import MongoClient

mongo = None
db = None
users_collection = None
images_collection = None

def init_db(app):
    global mongo, db, users_collection, images_collection
    
    mongo = MongoClient(app.config['MONGO_URI'])
    db = mongo['my_Mongodb']
    users_collection = db['users']
    images_collection = db['images'] 