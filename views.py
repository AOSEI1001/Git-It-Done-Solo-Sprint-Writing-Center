from flask import Blueprint, render_template
from flask import request, redirect, url_for, current_app, render_template, jsonify, send_from_directory


main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/')
def home():
    return render_template('faculty-requests.html')