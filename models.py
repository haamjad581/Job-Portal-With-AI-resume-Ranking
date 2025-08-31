# models.py
from datetime import datetime
from extensions import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.username}>"

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# -------------------------
# User Model
# -------------------------
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # store hashed password
    role = db.Column(db.String(50), nullable=False)  # job_seeker, recruiter, admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    resumes = db.relationship("Resume", backref="user", lazy=True)
    jobs = db.relationship("Job", backref="recruiter", lazy=True)
    applications = db.relationship("Application", backref="seeker", lazy=True)


# -------------------------
# Resume Model
# -------------------------
class Resume(db.Model):
    __tablename__ = 'resumes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)  # path to uploaded file
    parsed_data = db.Column(db.JSON, nullable=True)  # extracted info from resume
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)


# -------------------------
# Job Model
# -------------------------
class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    recruiter_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    skills_required = db.Column(db.String(300), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    applications = db.relationship("Application", backref="job", lazy=True)


# -------------------------
# Application Model
# -------------------------
class Application(db.Model):
    __tablename__ = 'applications'
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), nullable=False)
    seeker_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    status = db.Column(db.String(50), default="applied")  # applied, shortlisted, rejected, hired
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
