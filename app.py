from flask import Flask
from load_data import load_tutor_profiles
from views import main_blueprint
from models import TutorProfile, db
from auth import auth_blueprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    
    if TutorProfile.query.first() is None:
        load_tutor_profiles()
        print(TutorProfile.query.all())
    

app.register_blueprint(main_blueprint)
app.register_blueprint(auth_blueprint)

if __name__ == '__main__':
    app.run(debug=True)