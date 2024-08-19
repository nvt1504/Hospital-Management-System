from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Doctor, Examination, Department
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import text
from datetime import datetime

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone = request.form.get('phone')
        password = request.form.get('password')

        user = User.query.filter_by(phone=phone).first()
        if user and user.password == password:
            flash('Logged in successfully!', category='success')
            login_user(user, remember=True)
            if user.name == 'Admin':
                return redirect(url_for('views.admin', user_id=user.user_id))
            # Kiểm tra giá trị của role và chuyển hướng đến trang tương ứng
            elif user.role == 1:
                return redirect(url_for('views.home1', user_id=user.user_id))
            elif user.role == 2:
                return redirect(url_for('views.home2', user_id=user.user_id))
            else:
                # Nếu role không phải 1 hoặc 2, chuyển đến trang mặc định
                return redirect(url_for('views.home'))

        elif user:
            flash('Incorrect password, try again.', category='error')
        else:
            flash('Phone number does not exist.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        phone = request.form.get('phone')
        name = request.form.get('name')
        dob_str = request.form.get('dob')
        sex = request.form.get('sex')
        address = request.form.get('address')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(phone=phone).first()

        if user:
            flash('Phone number already exists.', category='error')
        elif len(phone) < 10:
            flash('Phone number must be at least 10 characters.', category='error')
        elif len(name) < 2:
            flash('Name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            # Chuyển đổi chuỗi ngày thành đối tượng date
            try:
                dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Date of birth format is incorrect. Use YYYY-MM-DD.', category='error')
                return redirect(url_for('auth.sign_up'))

            # Lấy giá trị user_id lớn nhất hiện tại và tự động tăng lên 1
            result = db.session.execute(
                text("SELECT MAX(user_id) FROM user")
            ).fetchone()
            
            max_id = result[0]
            new_id = (max_id + 1) if max_id is not None else 1

            # Tạo người dùng mới với user_id thủ công
            new_user = User(
                user_id=new_id,
                password=password1,
                name=name,
                dob=dob,
                sex=sex,
                phone=phone,
                address=address,
                role=1  # Assuming default role for a new user is patient (role=1)
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            return redirect(url_for('views.home1', user_id=new_user.user_id))

    return render_template("sign_up.html", user=current_user)

@auth.route('/make_examination/<int:user_id>', methods=['GET', 'POST'])
@login_required
def make_examination(user_id):
    if request.method == 'POST':
        date_str = request.form.get('date')
        department_id = request.form.get('department_id')
        doctor_id = request.form.get('doctor_id')

        # Validation checks
        try:
            # Parse the date
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Date format is incorrect.', category='error')
            return redirect(url_for('auth.make_examination', user_id=user_id))

        try:
            # Get the next examination_id
            result = db.session.execute(text('SELECT COALESCE(MAX(examination_id), 1000) FROM examination'))
            next_id = result.scalar() + 1

            # Insert new examination record
            db.session.execute(text('''
                INSERT INTO examination (examination_id, user_id, date, doctor_id)
                VALUES (:examination_id, :user_id, :date, :doctor_id)
            '''), {
                'examination_id': next_id,
                'user_id': user_id,
                'date': date,
                'doctor_id': doctor_id
            })
            db.session.commit()

            flash('Examination created successfully!', category='success')
            return redirect(url_for('views.home2', user_id=user_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error occurred: {e}', category='error')
        return redirect(url_for('auth.make_examination', user_id=user_id))

    # Query list of departments and doctors
    departments = db.session.execute(text('SELECT department_id, department_name FROM department')).fetchall()
    doctors = db.session.execute(text('''
        SELECT d.user_id AS doctor_id, u.name, d.department_id
        FROM doctor d
        JOIN "user" u ON d.user_id = u.user_id
    ''')).fetchall()
    
    return render_template('make_examination.html', user=current_user, departments=departments, doctors=doctors)
