from sqlalchemy import extract
from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from .models import Doctor, db, Patient, Examination
from sqlalchemy import text, func
import datetime
from datetime import date
from chat import get_response

views = Blueprint('views', __name__)


#------------------------------- Home Page -------------------------------
@views.route('/home', methods=['GET'])
def home():
    # if current_user.is_authenticated:
    #     if current_user.role == 1:
    #         return redirect(url_for('views.home1', user_id=current_user.user_id))
    #     elif current_user.role == 2:
    #         return redirect(url_for('views.home2', user_id=current_user.user_id))
    return render_template('home.html')

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
    

#------------------------------- Patient -------------------------------    
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


#------------------------------- Doctors -------------------------------
@views.route('/calendar/', methods=['GET'])
@login_required
def calendar():
    if current_user.role != 2:  # Assuming role 2 is for doctors
        return redirect(url_for('views.home'))
    
    today = datetime.date.today()
    month = today.strftime('%m')  # Định dạng tháng hiện tại
    year = today.strftime('%Y')   # Định dạng năm hiện tại

    # Truy vấn lịch khám của bác sĩ theo ngày trong tháng hiện tại
    query = text('''
        SELECT examination_id, user_id AS patient_id, date, doctor_id
        FROM examination
        WHERE strftime('%m', date) = :month
        AND strftime('%Y', date) = :year
        AND doctor_id = :doctor_id
    ''')

    appointments = db.session.execute(query, {'month': month, 'year': year, 'doctor_id': current_user.user_id}).fetchall()

    # Chuyển dữ liệu thành danh sách từ điển
    appointment_objects = []
    for appt in appointments:
        appointment = {
            'examination_id': appt[0],
            'patient_id': appt[1],
            'date': appt[2],  # Ngày đã là chuỗi, không cần định dạng lại
            'doctor_id': appt[3]  # Thêm ID của bác sĩ
        }
        appointment_objects.append(appointment)

    return render_template('lichkham.html', appointments=appointment_objects, user=current_user)


#------------------------------- Admin -------------------------------
@views.route('/admin/<int:user_id>', methods=['GET'])
@login_required
def admin(user_id):
    # Fetch all examination records using raw SQL wrapped in the text() function
    query = text('SELECT * FROM examination')
    result = db.session.execute(query)
    examinations = result.fetchall()

    # Count the number of doctors
    total_doctors = db.session.query(func.count(Doctor.user_id)).scalar()

    # Count the number of patients
    total_patients = db.session.query(func.count(Patient.user_id)).scalar()

    # Count the total number of examinations
    total_examinations = db.session.query(func.count(Examination.examination_id)).scalar()

    # Count the number of active patients (patients with examinations today)
    today = date.today()
    active_patients = db.session.query(func.count(func.distinct(Examination.user_id))).filter(
        Examination.date == today
    ).scalar()

    # Count the number of examinations per month for the current year
    current_year = today.year
    examinations_by_month = db.session.query(
        extract('month', Examination.date).label('month'),
        func.count(Examination.examination_id).label('count')
    ).filter(
        extract('year', Examination.date) == current_year
    ).group_by(
        extract('month', Examination.date)
    ).order_by('month').all()

    # Convert the query results into a format suitable for the frontend
    monthly_examinations_data = {month: count for month, count in examinations_by_month}

    return render_template(
        "admin.html",
        user=current_user,
        total_doctors=total_doctors,
        total_patients=total_patients,
        total_examinations=total_examinations,
        active_patients=active_patients,
        examinations=examinations,
        monthly_examinations_data=monthly_examinations_data,
        today=today  # Pass today's date to the template
    )

@views.route('/check-doc', methods=['GET'])
@login_required
def check_doc():
    # Execute direct SQL query  
    result = db.session.execute(text(
        """
        SELECT 
            user.user_id, 
            user.name, 
            user.dob, 
            user.sex, 
            user.phone, 
            user.address, 
            doctor.department_id, 
            department.department_name
        FROM 
            user 
        JOIN 
            doctor ON user.user_id = doctor.user_id 
        JOIN 
            department ON doctor.department_id = department.department_id
        """
    ))

    # Convert result to list of dictionaries
    columns = result.keys()  # Get column names
    rows = result.fetchall()
    doctors = [dict(zip(columns, row)) for row in rows]

    return render_template(
        "checkDoc.html",
        doctors=doctors,
        today=date.today()  # Pass today's date to the template
    )


@views.route('/check-patient', methods=['GET'])
@login_required
def check_patient():
    # Execute direct SQL query
    result = db.session.execute(text(
        """
        SELECT 
            user.user_id, 
            user.name, 
            user.dob, 
            user.sex, 
            user.phone, 
            user.address 
        FROM 
            user 
        JOIN 
            patient ON user.user_id = patient.user_id 
        """
    ))

    # Convert result to list of dictionaries
    columns = result.keys()  # Get column names
    rows = result.fetchall()
    patients = [dict(zip(columns, row)) for row in rows]

    return render_template(
        "checkPatient.html",
        patients=patients,
        today=date.today()  # Pass today's date to the template
    )

@views.route('/payment', methods=['GET'])
@login_required
def payment():
    # Đặt năm cần tính toán là 2022
    target_year = 2022

    # Danh sách các tháng trong năm
    months = [f"{i:02d}" for i in range(1, 13)]

    # Khởi tạo dict để lưu tổng lương và doanh thu cho từng tháng
    salary_dict = {month: 0 for month in months}
    revenue_dict = {month: 0 for month in months}

    for month in months:
        # Tính tổng lương cho các bác sĩ có ít nhất một đơn khám trong tháng hiện tại
        doctors_in_month = db.session.query(Examination.doctor_id).filter(
            func.strftime('%Y-%m', Examination.date) == f'{target_year}-{month}'
        ).distinct().subquery()

        monthly_salary = db.session.query(
            func.sum(Doctor.salary).label('monthly_salary')
        ).filter(
            Doctor.user_id.in_(doctors_in_month)
        ).scalar() or 0

        # Chia tổng lương cho 10
        salary_dict[month] = monthly_salary / 10

        # Tính tổng doanh thu trong tháng hiện tại
        monthly_revenue = db.session.query(
            func.sum(Examination.fee).label('monthly_revenue')
        ).filter(
            func.strftime('%Y-%m', Examination.date) == f'{target_year}-{month}'
        ).scalar() or 0

        revenue_dict[month] = monthly_revenue

    # Tính tiền lời/lỗ theo từng tháng
    profit_loss_data = [
        revenue_dict[month] - salary_dict[month] for month in months
    ]

    # Truyền dữ liệu sang template
    return render_template(
        "payment.html",
        today=date.today(),  # Vẫn giữ ngày hôm nay trong template
        total_salary=sum(salary_dict.values()) or 0,
        total_revenue=sum(revenue_dict.values()) or 0,
        months=months,
        salary_data=[salary_dict[month] for month in months],
        revenue_data=[revenue_dict[month] for month in months],
        profit_loss_data=profit_loss_data
    )


#------------------------CHAT BOT----------------------------
@views.post("/predict")
def predict():
    text = request.get_json().get("message")
    # TODO: check if valid
    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)
