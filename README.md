# Hospital Management System

## Overview

The **Hospital Management System** is a web-based application designed to streamline the operations of small private clinics. Built using the Flask framework, this system provides tools to manage patient records, doctors, appointments, and other crucial hospital functions. An AI chatbot is integrated to enhance user interaction and provide instant support.

### What is Flask?

[Flask](https://flask.palletsprojects.com/) is a lightweight and flexible web framework for Python, designed to be simple and easy to get started with while allowing for scalability and flexibility. Flask is widely used in developing small to medium-sized web applications due to its simplicity and extensive support for extensions, making it ideal for projects that require rapid development and customization.

## Project Description

### 1.1 Introduction

#### Project Objective:
Managing information related to medical services is critical for both clinics and patients. Inefficient management can lead to inconveniences, such as patients having to repeatedly provide the same personal information during multiple visits, or doctors being unable to track patient medical history effectively. These issues can cause frustration for both medical staff and patients.

To address these challenges, our team aims to develop a system that efficiently manages medical services for clinics, including patient records, medical history, doctor management, and pharmacy and laboratory services. Additionally, we have integrated an AI chatbot to enhance user interaction and provide instant support.

#### Scope:
- **Target Audience:** Small private clinics providing daily consultation services.
- **System Capabilities:**
  - Manage patient records and medical history.
  - Manage the clinic's pharmacy inventory.
  - Manage the clinic's doctors.
  - Generate reports and statistics on clinic activities, such as revenue, lab tests, prescriptions, etc.
  - Add, edit, and delete data related to patients, doctors, prescriptions, lab tests, and more.
  - Provide AI chatbot support for patient inquiries and assistance.

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
- **AI Chatbot Integration:** Provide an intelligent chatbot for real-time support and query resolution.

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
  - Interact with the AI chatbot for assistance and information.
  
- **Appointment Management:**
  - Schedule, reschedule, or cancel appointments.
  - Notifications for upcoming appointments.
  
- **Pharmacy and Test Management:**
  - Maintain detailed records of medicines and lab tests.
  - Update stock levels and test results.

## Techniques Used

### 1. **Tokenization and Stemming**
   - **Tokenization:** Splitting text into individual words or tokens.
   - **Stemming:** Reducing words to their root form to normalize the vocabulary.

### 2. **Bag of Words Model**
   - **Bag of Words (BoW):** Representing text data in a vectorized form where each word in the vocabulary is a feature. This approach is used to convert user input into a format suitable for machine learning.

### 3. **Neural Network for Classification**
   - **Feedforward Neural Network:** Utilized for classifying user inputs into predefined intents.
   - **Activation Functions:** Applied to introduce non-linearity into the model.

### 4. **Cross-Entropy Loss**
   - **Cross-Entropy Loss:** A loss function used for classification tasks to measure the difference between predicted probabilities and true labels.

### 5. **Adam Optimizer**
   - **Adam Optimizer:** An optimization algorithm that adjusts learning rates and adapts based on training progress.

### 6. **DataLoader and Custom Dataset**
   - **DataLoader:** Efficiently loads data in batches and shuffles it for training.
   - **Custom Dataset:** A `ChatDataset` class that manages the format and indexing of the data.

### 7. **Model Saving**
   - **Model State Dictionary:** Saves the trained model’s weights and parameters for future use.

## Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Database:** SQLite (scalable to MySQL/PostgreSQL)
- **Authentication:** Flask-Login
- **AI Chatbot:** Integration with an AI chatbot platform
- **Deployment:** PythonAnywhere/Heroku (or your preferred hosting service)

## Usage

- **Admin:** Manage hospital operations, including doctors, patients, and appointments.
- **Doctor:** Access patient records, manage appointments, and update medical histories.
- **Patient:** Book appointments, view medical records, manage personal information, and interact with the AI chatbot for support.

## Model Training

The chatbot model is trained using the following approach:

1. **Data Preparation:**
   - Tokenization and stemming are applied to user input patterns.
   - A Bag of Words model is used to convert text data into numerical format.
   
2. **Model Definition:**
   - A simple feedforward neural network is trained to classify user inputs into intents.
   
3. **Training:**
   - The model is trained using cross-entropy loss and the Adam optimizer.
   - Data is loaded in batches using PyTorch’s DataLoader.

4. **Saving the Model:**
   - The trained model’s state dictionary and other metadata are saved to a file for future use.

## Contributing

Contributions are welcome! Please fork this repository, create a new branch, and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For any questions or feedback, please reach out to [nvt220104@gmail.com]
