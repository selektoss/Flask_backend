
class Config:
    
    SECRET_KEY = 'sdg34tksdfu944dskfjhse'
    CORS_ALLOWED_ORIGINS = ['http://localhost:8080']
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = "mysql://kikerzzz:tara190387@192.168.0.105/medic"
    JSON_AS_ASCII = False
    UPLOAD_FOLDER = '/path/user/the/uploads'
    ALLOWED_EXTENSIONS = {'png'}
    
    
