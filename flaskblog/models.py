from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flaskblog import db, login_manager, app
from flask_login import UserMixin

# this decorator is used to reload the user object from the user ID stored in the session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    """
    This class will create a table in the database for users.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg') # by default: image_file
    password = db.Column(db.String(60), nullable=False)
    trainings = db.relationship('Training', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        """
        This function will create a token.
        """
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        # creating a token
        return s.dumps({'user_id': self.id}).decode('utf-8')
    

    @staticmethod # not expect self argument
    def verify_reset_token(token):
        """
        This function will verify the token.
        """
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        # get the user with the id
        return User.query.get(user_id)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Training(db.Model):
    """
    This class will create a table in the database for trainings.
    """
    id = db.Column(db.Integer, primary_key=True)
    trainer = db.Column(db.String(100))
    date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Training('{self.trainer}', '{self.date}')"
