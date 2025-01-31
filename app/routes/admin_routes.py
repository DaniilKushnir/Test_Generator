from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app , abort
from werkzeug.security import generate_password_hash
import json
from bson.objectid import ObjectId

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


@admin_bp.route('/upload_tests', methods=['GET', 'POST'])
def add_tests():
    if request.method == 'POST':
        uploaded_file = request.files.get('test_file')

        if uploaded_file and uploaded_file.filename.endswith('.json'):
            try:
                file = uploaded_file.stream.read().decode('utf-8')
                tests = json.loads(file)

                 
                if isinstance(tests, list):
                    current_app.db["tests"].insert_many(tests)
                elif isinstance(tests, dict):
                    current_app.db["tests"].insert_one(tests)
                else:
                    raise ValueError("Invalid JSON structure. Must be an object or an array of objects.")
                    

                flash("Tests uploaded successfully!", "success")
                return redirect(url_for('admin.view_tests'))

            except json.JSONDecodeError:
                flash("Invalid JSON file. Please upload a valid JSON.", "danger")
            except Exception as e:
                flash(f"An error occurred: {e}", "danger")
        else:
            flash("Please upload a valid JSON file.", "danger")
            
    return render_template('add_tests.html')   




@admin_bp.route('/view_tests', methods=['GET'])
def view_tests():
    tests = list(current_app.db["tests"].find())  
    return render_template('view_tests.html', tests=tests)




