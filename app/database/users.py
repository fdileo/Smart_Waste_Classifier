from flask_login import UserMixin

class User(UserMixin):
    
    '''
    Classe User compatibile con Flask-Login. 
    Rappresenta un utente autenticato nella nostra applicazione Flask
    '''
    
    def __init__(self,user_data):
        self.id = str(user_data['_id'])
        self.email = user_data['email']
        self.password_hash = user_data['password']
        
    def get_id(self):
        return self.id