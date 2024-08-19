# Hospital Management System

## Overview

The **Hospital Management System** is a web-based application built using the Flask framework. This system aims to streamline the operations of small private clinics by providing tools to manage patient records, doctors, appointments, and other crucial hospital functions. 

### What is Flask?

[Flask](https://flask.palletsprojects.com/) is a lightweight and flexible web framework for Python, designed to be simple and easy to get started with while allowing for scalability and flexibility. Flask is widely used in developing small to medium-sized web applications due to its simplicity and extensive support for extensions, making it ideal for projects that require rapid development and customization.

## Project Description

### 1.1 Introduction

#### Project Objective:
Managing information related to medical services is critical for both clinics and patients. Inefficient management can lead to inconveniences, such as patients having to repeatedly provide the same personal information during multiple visits, or doctors being unable to track patient medical history effectively. These issues can cause frustration for both medical staff and patients.

To address these challenges, our team aims to develop a system that efficiently manages medical services for clinics, including patient records, medical history, doctor management, and pharmacy and laboratory services.

#### Scope:
- **Target Audience:** Small private clinics providing daily consultation services.
- **System Capabilities:**
  - Manage patient records and medical history.
  - Manage the clinic's pharmacy inventory.
  - Manage the clinic's doctors.
  - Generate reports and statistics on clinic activities, such as revenue, lab tests, prescriptions, etc.
  - Add, edit, and delete data related to patients, doctors, prescriptions, lab tests, and more.

### 1.2 System Requirements

The system should fulfill the following requirements:
- **User Management:** Handle user information and roles (admin, doctor, patient).
- **Patient Management:** Maintain patient details and medical history.
- **Doctor Management:** Manage doctor profiles and specializations.
- **Department Management:** Organize departments within the clinic (e.g., cardiology, pediatrics).
- **Examination Management:** Track patient visits and consultations.
- **Symptom Management:** Record and manage patient symptoms during consultations.
- **Medicine Management:** Maintain and manage the clinic's pharmacy stock.
- **Test Management:** Organize and manage medical tests and their results.

## Features

- **User Authentication:**
  - Role-based access control with secure login and registration.
  
- **Admin Dashboard:**
  - Manage doctors, patients, and clinic staff.
  - View and manage appointments.
  - Generate reports and view statistics.
  
- **Doctor Dashboard:**
  - Access and update patient records.
  - Schedule and manage appointments.
  - Update patient medical history and prescriptions.
  
- **Patient Portal:**
  - Book appointments online.
  - View medical records and consultation history.
  - Access prescriptions and test results.
  
- **Appointment Management:**
  - Schedule, reschedule, or cancel appointments.
  - Notifications for upcoming appointments.
  
- **Pharmacy and Test Management:**
  - Maintain detailed records of medicines and lab tests.
  - Update stock levels and test results.

## Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Database:** SQLite (scalable to MySQL/PostgreSQL)
- **Authentication:** Flask-Login
- **Deployment:** PythonAnywhere/Heroku (or your preferred hosting service)

## Usage

- **Admin:** Manage hospital operations, including doctors, patients, and appointments.
- **Doctor:** Access patient records, manage appointments, and update medical histories.
- **Patient:** Book appointments, view medical records, and manage personal information.

## Contributing

Contributions are welcome! Please fork this repository, create a new branch, and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For any questions or feedback, please reach out to [nvt220104@gmail.com]
