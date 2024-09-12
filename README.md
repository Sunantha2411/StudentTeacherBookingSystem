# Teacher-Student Appointment Management System

This is a web-based appointment management system built using Flask and Firebase Firestore. The system is designed for educational institutions, allowing students to book appointments with teachers, and administrators to manage teachers and appointments. The app includes role-based dashboards for **admin**, **teacher**, and **student** users.

## Features
- **User Registration**: Users can register with email, password, and a selected role (student, teacher, or admin).
- **User Login**: Users can log in and are redirected to their respective dashboards based on their role.
  - **Admin Dashboard**: Admins can add teachers, view appointments, and manage the system.
  - **Teacher Dashboard**: Teachers can view appointments and receive messages.
  - **Student Dashboard**: Students can book appointments with teachers and view their scheduled appointments.
- **Book Appointment**: Students can book appointments with available teachers.
- **View Appointments**: Users can view appointments, with customized views based on their role.
- **View Messages**: Teachers can view messages from students.

## Technology Stack
- **Backend**: Flask (Python)
- **Database**: Firebase Firestore
- **Authentication**: Firebase Authentication
- **Frontend**: HTML, CSS (Flask templates)
- **Logging**: Python's built-in logging module

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/teacher-student-appointment-system.git
    cd teacher-student-appointment-system
    ```

2. Set up a virtual environment (optional but recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # For Linux/macOS
    venv\Scripts\activate  # For Windows
    ```

3. Install required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up Firebase:
    - Create a Firebase project at [Firebase Console](https://console.firebase.google.com/).
    - Enable Firebase Authentication and Firestore in the project.
    - Download the `firebase_admin_config.json` service account key file and place it in the root directory of the project.

5. Set a secret key for Flask in the `app.py` file:
    ```python
    app.secret_key = 'your_secret_key'
    ```

6. Run the Flask application:
    ```bash
    python app.py
    ```

7. Access the app in your browser at `http://127.0.0.1:5000`.

## File Structure
```bash
├── app.py                  # Main Flask app
├── templates/
│   ├── index.html           # Home page template
│   ├── admin_dashboard.html # Admin dashboard template
│   ├── teacher_dashboard.html # Teacher dashboard template
│   ├── student_dashboard.html # Student dashboard template
│   ├── register.html        # User registration page template
│   ├── login.html           # User login page template
│   ├── add_teacher.html     # Admin page for adding teachers
│   ├── book_appointment.html# Student appointment booking page
│   ├── view_appointments.html # View appointments page for all roles
│   ├── view_messages.html   # Teacher page to view messages from students
├── firebase_admin_config.json # Firebase service account key (not included in repo)
├── requirements.txt         # Project dependencies
├── README.md                # Project documentation (this file)
└── app.log                  # Log file for application
