from flask import Blueprint, render_template, request, redirect, url_for

student_bp = Blueprint('student', __name__)

@student_bp.route('/dashboard')
def dashboard():
    return render_template('student_dashboard.html')

