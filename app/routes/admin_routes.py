from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.security import generate_password_hash

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin_dashboard')
def dashboard():
    students = current_app.db["students"].find()  
    return render_template('admin_dashboard.html', students=students)


@admin_bp.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        student_data = {
            "name": request.form['name'],
            "surname": request.form['surname'],
            "middle_name": request.form['middle_name'],
            "group": request.form['group'],
            "subject": request.form['subject'],
            "email": request.form['email'],
            "password": generate_password_hash(request.form['password'])
        }


        try:
            current_app.db["students"].insert_one(student_data)
            flash("Student added successfully!", "success")
        except Exception as e:
            flash(f"An error occurred: {e}", "danger")
        
        return redirect(url_for('admin.dashboard'))

    return render_template('add_student.html')
