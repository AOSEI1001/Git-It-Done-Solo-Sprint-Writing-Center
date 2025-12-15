from flask import Blueprint, render_template
from flask import request, flash, redirect, url_for, current_app, render_template, jsonify, send_from_directory
from models import db, TutorRequest, TutorProfile, TutorAssignment
from flask_login import current_user
from matching import generate_suggested_matches


main_blueprint = Blueprint('main', __name__)

def normalize_list(value):
    if not value:
        return []
    return [v.strip().lower() for v in value.split(",")]

@main_blueprint.route('/api/v1/admin-top-matches', methods=['GET'])
def admin_top_matches():
    requests = TutorRequest.query.filter_by(requestStatus="Open").all()
    response = []

    for tutor_request in requests:
        suggestions = generate_suggested_matches(tutor_request)
        suggestion_data = [{
            "tutorId": m["tutorId"],
            "tutorName": m["tutorName"],
            "score": m["score"],
            "reason": m["reason"]
        } for m in suggestions]


        response.append({
            "request_id": tutor_request.id,
            "courseName": tutor_request.courseName,
            "professorName": tutor_request.facultyName,
            "details": tutor_request.courseDescription,
            "suggestedTutors": suggestion_data
        })

    return jsonify(response), 200

@main_blueprint.route('/')
def home():
    tutors = TutorProfile.query.filter_by(active=True).order_by(TutorProfile.name).all()
    requests = TutorRequest.query.order_by(TutorRequest.created_at.desc()).all()
    return render_template('faculty-requests.html', tutors=tutors, requests=requests)


@main_blueprint.route('/new_tutor_request', methods=['POST'])
def create_tutor_request():

    new_request = TutorRequest(
        # professor_id=current_user.id,  # REQUIRED
        courseName=request.form['courseName'],
        facultyName=request.form['facultyName'],
        facultyEmail=request.form['facultyEmail'],
        requestedTutorId=request.form.get('requestedTutorId'),
        courseDescription=request.form['courseDescription'],
        requestStatus="Open",
        majors=request.form.get('majors')
    )

    db.session.add(new_request)
    db.session.commit()

    # flash("Tutor request created successfully!")

    return jsonify({
        "id": new_request.id,
        "courseName": new_request.courseName,
        "facultyName": new_request.facultyName,
        "requestStatus": new_request.requestStatus
    }), 201


@main_blueprint.route("/faculty-tutor-catalog", methods=["GET"])
def tutor_catalog():
    tutors = TutorProfile.query.all()
    
    return render_template('faculty-tutor-catalog.html', tutors=tutors)


@main_blueprint.route("/admin-dashboard")
def admin_dashboard():
    # tutors = TutorProfile.query.all()
    
    return render_template('admin-dashboard.html')

@main_blueprint.route("/admin-matching", methods=["GET"])
def admin_matching():
    # tutors = TutorProfile.query.all()
    
    return render_template('admin-matching.html')

@main_blueprint.route("/admin/match/<int:request_id>", methods=["GET"])
def match_request(request_id):
    tutor_request = TutorRequest.query.get(request_id)
    matches = generate_suggested_matches(tutor_request)

    # Convert to JSON
    data = [
        {"tutorName": m["tutorName"], "score": m["score"]}
        for m in matches
    ]
    return jsonify(data)


@main_blueprint.route("/messages", methods=["GET"])
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
