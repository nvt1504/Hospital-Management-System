from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from .models import Doctor, db
from sqlalchemy import text

views = Blueprint('views', __name__)

@views.route('/', methods=['GET'])
def home():
    # if current_user.is_authenticated:
    #     if current_user.role == 1:
    #         return redirect(url_for('views.home1', user_id=current_user.user_id))
    #     elif current_user.role == 2:
    #         return redirect(url_for('views.home2', user_id=current_user.user_id))
    return render_template('homepage.html')

@views.route('/', methods=['GET'])
def homepage():
    return render_template('homepage.html')

@views.route('/home1/<int:user_id>', methods=['GET'])
@login_required
def home1(user_id):
    if current_user.role == 1:
        return render_template("home1.html", user=current_user)
    else:
        return redirect(url_for('views.home'))

@views.route('/home2/<int:user_id>', methods=['GET'])
@login_required
def home2(user_id):
    if current_user.role == 2:
        # Lấy thông tin bác sĩ
        doctor = Doctor.query.filter_by(user_id=user_id).first()
        if doctor and doctor.department:
            department_name = doctor.department.department_name
        else:
            department_name = 'Không có thông tin'
        
        # Render template với thông tin bác sĩ
        return render_template("home2.html", user=current_user, department_name=department_name)
    else:
        return redirect(url_for('views.home'))
    
@views.route('/examination_history/<int:user_id>', methods=['GET'])
@login_required
def examination_history(user_id):
    if current_user.user_id != user_id:
        return redirect(url_for('views.home'))
    
    if current_user.role == 1:  # Assuming role 1 is for patients
        query = text('SELECT * FROM examination WHERE user_id = :user_id')
    elif current_user.role == 2:  # Assuming role 2 is for doctors
        query = text('SELECT * FROM examination WHERE doctor_id = :user_id')
    else:
        return redirect(url_for('views.home'))
    
    examinations = db.session.execute(query, {'user_id': user_id}).fetchall()

    examination_objects = []
    for exam in examinations:
        examination = {
            'examination_id': exam[0],
            'user_id': exam[1],
            'date': exam[2],
            'doctor_id': exam[3],
            'age': exam[4],
            'height': exam[5],
            'weight': exam[6],
            'blood_pressure_S': exam[7],
            'blood_pressure_D': exam[8],
            'heart_rate': exam[9],
            'fee': round(exam[10], 2) if isinstance(exam[10], float) else exam[10],
            'conclusion': exam[11],
            'time_arranged': exam[12]
        }
        examination_objects.append(examination)

    return render_template('examination_history.html', user=current_user, examinations=examination_objects)