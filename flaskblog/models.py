from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flaskblog import db, login_manager, app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg') # by default: image_file
    password = db.Column(db.String(60), nullable=False)
    trainings = db.relationship('Training', backref='author', lazy=True)
    group_trainings = db.relationship('GroupTraining', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        """
        """
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        # creating a token
        return s.dumps({'user_id': self.id}).decode('utf-8')
    

    @staticmethod # not excpect self argument
    def verify_reset_token(token):
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
    id = db.Column(db.Integer, primary_key=True)
    # type = db.Column(db.String(100))
    trainer = db.Column(db.String(100))
    date = db.Column(db.DateTime)
    # hour = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Training('{self.trainer}', '{self.date}')"
    
class GroupTraining(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Training('{self.title}', '{self.date}')"
