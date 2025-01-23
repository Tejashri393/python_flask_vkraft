

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Organisation(db.Model):
    __tablename__ = 'organisations'
    code = db.Column(db.Integer, primary_key=True)
    org_name = db.Column(db.String(20), nullable=False)
    details = db.Column(db.String(20))

    def to_dict(self):
        return {
            "code": self.code,
            "org_name": self.org_name,
            "details": self.details,
        }



