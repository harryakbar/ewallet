from app import db

class User(db.Model):
    user_id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False)
    saldo = db.Column(db.Integer, index=True, unique=False)
 
    def __repr__(self):
        return '<User {}, {}, {}>'.format(self.user_id, self.name, self.saldo)
