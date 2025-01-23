from flask import Flask
from app.Model.user import db                                       #object handles database interactions.
from app.controller.user import user_bp                             # A Flask blueprint imported from app.controller.user

# app = Flask(__name__, static_folder='static', template_folder='templates')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/postgres'
app.config['SECRET_KEY'] = 'tejashri'

db.init_app(app)

# Register blueprint
app.register_blueprint(user_bp)

@app.route('/')
def index():
    return "Welcome to User Manager API!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)
