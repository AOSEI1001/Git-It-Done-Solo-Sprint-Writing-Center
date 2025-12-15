import flash
from flask import Blueprint, render_template
from flask import request, redirect, url_for, current_app, render_template, jsonify, send_from_directory
from models import db, TutorRequest, TutorProfile, TutorAssignment


main_blueprint = Blueprint('main', __name__)

def normalize_list(value):
    if not value:
        return []
    return [v.strip().lower() for v in value.split(",")]


def find_suggested_tutors(tutor_request, limit=5):
    tutors = TutorProfile.query.filter_by(active=True).all()
    suggestions = []

    requested_name = tutor_request.requestedTutor.lower() if tutor_request.requestedTutor else None
    course_text = tutor_request.courseName.lower() + " " + tutor_request.courseDescription.lower()

    for tutor in tutors:
        score = 0
        reasons = []

        tutor_majors = normalize_list(tutor.majors)
        tutor_languages = normalize_list(tutor.languages)

        # Requested tutor match
        if requested_name and requested_name in tutor.name.lower():
            score += 100
            reasons.append("Requested tutor")

        # Major / discipline match
        for major in tutor_majors:
            if major in course_text:
                score += 50
                reasons.append("Major match")
                break

        # Language course match
        for lang in tutor_languages:
            if lang in course_text:
                score += 30
                reasons.append("Language match")
                break

        if score > 0:
            suggestions.append((tutor, score, ", ".join(reasons)))

    # sort by score
    suggestions.sort(key=lambda x: x[1], reverse=True)
    return suggestions[:limit]


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

@main_blueprint.route("/assign-tutor", methods=["POST"])
def assign_tutor():
    request_id = request.form["request_id"]
    tutor_id = request.form["tutor_id"]

    assignment = TutorAssignment(
        tutor_id=tutor_id,
        request_id=request_id
    )

    tutor_request = TutorRequest.query.get(request_id)
    tutor_request.requestStatus = "Assigned"

    db.session.add(assignment)
    db.session.commit()

    flash("Tutor assigned successfully")
    return redirect(url_for("main.admin_matching"))
