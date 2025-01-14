from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    gender = db.Column(db.String(30), nullable=True)
    contact_info = db.Column(db.String(30), nullable=True)
    address = db.Column(db.String(50), nullable=True)
    mobile_no = db.Column(db.String(10), unique=True, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "fname": self.fname,
            "lname": self.lname,
            "email": self.email,
            "gender": self.gender,
            "contact_info": self.contact_info,
            "address": self.address,
            "mobile_no": self.mobile_no,
        }
