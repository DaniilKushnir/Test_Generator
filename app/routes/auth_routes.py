from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

       
        if username == "admin" and password == "admin123":
            session['username'] = username
            session['role'] = 'admin'  
            return redirect(url_for('admin.dashboard'))  

       
        student = current_app.db["students"].find_one({"email": username})
        if student and check_password_hash(student['password'], password):  
            session['username'] = username
            session['role'] = 'student'  
            session['student_id'] = student['_id']  
            return redirect(url_for('student.dashboard'))  
        
    
        flash("Invalid credentials", "danger")
        return redirect(url_for('auth.login'))  

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()  
    flash("You have been logged out.", "success")
    return redirect(url_for('auth.login')) 
