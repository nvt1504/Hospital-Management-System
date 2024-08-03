from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import CheckConstraint

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(255), nullable=True)
    name = db.Column(db.String(255), nullable=True)
    dob = db.Column(db.Date, nullable=True)
    sex = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(255), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    role = db.Column(db.Integer, nullable=True)

    # Constraints
    __table_args__ = (
        CheckConstraint(sex.in_(['Male', 'Female']), name='check_sex'),
        CheckConstraint(role.in_([1, 2]), name='check_user_role')
    )

    # Relationships
    patient = db.relationship('Patient', backref='user', uselist=False)
    doctor = db.relationship('Doctor', backref='user', uselist=False)


class Patient(db.Model):
    __tablename__ = 'patient'
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    blood_type = db.Column(db.String(255), nullable=True)

    # Constraints
    __table_args__ = (
        CheckConstraint(blood_type.in_(['A', 'B', 'AB', 'O']), name='check_blood_type'),
    )

class Department(db.Model):
    __tablename__ = 'department'
    department_id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(255), nullable=False)

class Doctor(db.Model):
    __tablename__ = 'doctor'
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey('department.department_id'), nullable=True)
    salary = db.Column(db.Numeric(precision=10, scale=2), nullable=True)

    # Constraints
    __table_args__ = (
        CheckConstraint(salary > 0, name='check_salary'),
    )

    # Relationships
    department = db.relationship('Department', backref='doctors', uselist=False)

class Symptom(db.Model):
    __tablename__ = 'symptom'
    symptom_id = db.Column(db.Integer, primary_key=True)
    symptom_name = db.Column(db.String(255), nullable=True)
    department_id = db.Column(db.Integer, db.ForeignKey('department.department_id'), nullable=True)

    # Relationships
    department = db.relationship('Department', backref='symptoms', uselist=False)

class Test(db.Model):
    __tablename__ = 'test'
    test_id = db.Column(db.Integer, primary_key=True)
    test_name = db.Column(db.String(255), nullable=True)
    fee = db.Column(db.Numeric(precision=10, scale=2), nullable=True)

    # Constraints
    __table_args__ = (
        CheckConstraint(fee >= 0, name='check_fee'),
    )

class Examination(db.Model):
    __tablename__ = 'examination'
    examination_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('patient.user_id'), nullable=True)
    date = db.Column(db.Date, nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.user_id'), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    height = db.Column(db.Numeric(precision=5, scale=2), nullable=True)
    weight = db.Column(db.Numeric(precision=5, scale=2), nullable=True)
    blood_pressure_S = db.Column(db.Integer, nullable=True)
    blood_pressure_D = db.Column(db.Integer, nullable=True)
    heart_rate = db.Column(db.Integer, nullable=True)
    fee = db.Column(db.Numeric(precision=10, scale=2), nullable=True)
    conclusion = db.Column(db.String(255), nullable=True)
    time_arranged = db.Column(db.Time, nullable=True)

    # Constraints
    __table_args__ = (
        CheckConstraint(height > 0, name='check_height'),
        CheckConstraint(weight > 0, name='check_weight'),
        CheckConstraint(blood_pressure_S > 0, name='check_blood_pressure_S'),
        CheckConstraint(blood_pressure_D > 0, name='check_blood_pressure_D'),
        CheckConstraint(heart_rate > 0, name='check_heart_rate'),
    )

    # Relationships
    patient = db.relationship('Patient', backref='examinations')
    doctor = db.relationship('Doctor', backref='examinations')

from sqlalchemy import CheckConstraint

class TestJoin(db.Model):
    __tablename__ = 'test_join'
    examination_id = db.Column(db.Integer, db.ForeignKey('examination.examination_id'), primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('test.test_id'), primary_key=True)
    result = db.Column(db.String(255), nullable=True)

    # Relationships
    examination = db.relationship('Examination', backref='tests')
    test = db.relationship('Test', backref='examinations')

    # Define composite primary key
    __table_args__ = (
        db.PrimaryKeyConstraint('examination_id', 'test_id'),
    )

class SymptomJoin(db.Model):
    __tablename__ = 'symptom_join'
    examination_id = db.Column(db.Integer, db.ForeignKey('examination.examination_id'), primary_key=True)
    symptom_id = db.Column(db.Integer, db.ForeignKey('symptom.symptom_id'), primary_key=True)

    # Relationships
    examination = db.relationship('Examination', backref='symptoms')
    symptom = db.relationship('Symptom', backref='examinations')

    # Define composite primary key
    __table_args__ = (
        db.PrimaryKeyConstraint('examination_id', 'symptom_id'),
    )

class Medicine(db.Model):
    __tablename__ = 'medicine'
    medicine_id = db.Column(db.Integer, primary_key=True)
    medicine_name = db.Column(db.String(255), nullable=True)
    number_left = db.Column(db.Integer, nullable=True)
    cost_per = db.Column(db.Numeric(precision=10, scale=2), nullable=True)

    # Constraints
    __table_args__ = (
        CheckConstraint(number_left >= 0, name='check_number_left'),
        CheckConstraint(cost_per >= 0, name='check_cost_per'),
    )
    
class MedicinePrescription(db.Model):
    __tablename__ = 'medicine_prescription'
    examination_id = db.Column(db.Integer, db.ForeignKey('examination.examination_id'), primary_key=True)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicine.medicine_id'), primary_key=True)
    number = db.Column(db.Integer, nullable=True)
    cost = db.Column(db.Numeric(precision=10, scale=2), nullable=True)

    # Constraints
    __table_args__ = (
        db.PrimaryKeyConstraint('examination_id', 'medicine_id'),
        CheckConstraint('number >= 0', name='check_number'),
        CheckConstraint('cost >= 0', name='check_cost'),
    )



    # Relationships
    examination = db.relationship('Examination', backref='medicines')
    medicine = db.relationship('Medicine', backref='prescriptions')
