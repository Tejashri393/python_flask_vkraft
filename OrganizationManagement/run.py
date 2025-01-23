
from flask import Flask
from app.Model.org import db
from app.controller.org import org_bp
from app.Model.emp import db
from app.controller.emp import employee_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/postgres'
app.config['SECRET_KEY'] = 'tejashri'

db.init_app(app)
app.register_blueprint(org_bp)
app.register_blueprint(employee_bp)

@app.route('/')
def index():
    return "Welcome to Organization management API!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)

