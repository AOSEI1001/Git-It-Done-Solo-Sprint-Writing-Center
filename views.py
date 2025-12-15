import flash
from flask import Blueprint, render_template
from flask import request, redirect, url_for, current_app, render_template, jsonify, send_from_directory

from models import db, TutorRequest, TutorProfile


main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/')
def home():
    return render_template('faculty-requests.html')


@main_blueprint.route('/new_tutor_request', methods=['POST'])
def create_tutor_request():
    
    ## auth
    
    new_request = TutorRequest(
        professor_id=request.form['professor_id'],
        
        courseName=request.form['courseName'],
        facultyName=request.form['facultyName'],
        facultyEmail=request.form['facultyEmail'],
        requestedTutor=request.form['requestedTutor'],
        courseDescription=request.form['courseDescription'],
        requestStatus="Open"
    )
        
    
    flash('Tutor request created successfully!')
    
    db.session.add(new_request)
    db.session.commit()
    return redirect(url_for('main.home'))


@main_blueprint.route("/faculty-tutor-catalog")
def tutor_catalog():
    tutors = TutorProfile.query.all()
    
    return render_template('faculty-tutor-catalog.html', tutors=tutors)


@main_blueprint.route("/admin-dashboard")
def admin_dashboard():
    # tutors = TutorProfile.query.all()
    
    return render_template('admin-dashboard.html')

@main_blueprint.route("/admin-matching")
def admin_matching():
    # tutors = TutorProfile.query.all()
    
    return render_template('admin-matching.html')

@main_blueprint.route("/messages")
def admin_messages():
    # tutors = TutorProfile.query.all()
    
    return render_template('messages.html')