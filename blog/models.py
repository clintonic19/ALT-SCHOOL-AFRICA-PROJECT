from blog import database, login_manager, app
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))


#users table 
class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(20), unique=True, nullable=False)
    email = database.Column(database.String(50), unique=True, nullable=False)
    image_file = database.Column(database.String(20), nullable=False, default='default.jpg')
    password = database.Column(database.String(60), nullable=False)
    posts = database.relationship('Post', backref='author', lazy=True)
    
    
    #token to reset password authentication
    def get_reset_token(self, expires_sec=1800):
        s_serializer = Serializer(app.config['SECRET_KEY'], expires_sec )
        return s_serializer.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod
    def reset_verified_token(token):
        s_serializer = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s_serializer.load(token)['user_id']
        except:
            return None
        return User.query.get(user_id )
    
    def __ref__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


#post into the database
class Post(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String(100), nullable=False)
    date_posted = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    content = database.Column(database.Text, nullable=False)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)
       
    def __ref__(self):
        return f"User('{self.title}', '{self.date_posted}')"

