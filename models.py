from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash  # <-- add this

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    position = db.Column(db.String(200), nullable=False, default="Admin")

    password_hash = db.Column(db.String(200))
    google_id = db.Column(db.String(200))

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)
    
    requests = db.relationship("TutorRequest", backref="Professor", lazy=True)


class TutorProfile(db.Model):
    __tablename__ = "tutorProfile"
    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    interests = db.Column(db.String(200), nullable=False)
    classYear =  db.Column(db.String(200), nullable=False)
    pronouns = db.Column(db.String(200), nullable=False)
    hometown = db.Column(db.String(200), nullable=False)
    majors = db.Column(db.String(200), nullable=False)
    minors = db.Column(db.String(200), nullable=False)
    image_address = db.Column(db.String(200), nullable=False)
    languages = db.Column(db.String(200), nullable=False)
    active = db.Column(db.Boolean, default=True)

class TutorRequest(db.Model):
    __tablename__ = "tutorRequest"
    id = db.Column(db.Integer, primary_key=True)
    
    professor_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    courseName = db.Column(db.String(200), nullable=False)
    facultyName = db.Column(db.String(200), nullable=False)
    facultyEmail = db.Column(db.String(200), nullable=False)
    requestedTutor = db.Column(db.String(200), nullable=True)
    courseDescription = db.Column(db.String(200), nullable=False)
    requestStatus = db.Column(db.String(200), nullable=False, default="Open")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class TutorAssignment(db.Model, UserMixin):
    __tablename__ = "tutorAssignment"
    
    id = db.Column(db.Integer, primary_key=True)
    
    tutor_id = db.Column(db.Integer, db.ForeignKey("tutorProfile.id"), nullable=False)
    request_id = db.Column(db.Integer, db.ForeignKey("tutorRequest.id"), nullable=False)
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow)