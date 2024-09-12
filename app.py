from flask import Flask, render_template, request, redirect, url_for, session, flash
import firebase_admin
from firebase_admin import credentials, firestore, auth
import logging

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a real secret key for production

# Load the service account key JSON file
cred = credentials.Certificate('firebase_admin_config.json')
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

# Logging setup
logging.basicConfig(filename='app.log', level=logging.INFO)

# Route for Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Admin Dashboard
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user_id' in session and session['role'] == 'admin':
        return render_template('admin_dashboard.html')
    else:
        return redirect(url_for('login'))

# Teacher Dashboard
@app.route('/teacher_dashboard')
def teacher_dashboard():
    if 'user_id' in session and session['role'] == 'teacher':
        return render_template('teacher_dashboard.html')
    else:
        return redirect(url_for('login'))

# Student Dashboard
@app.route('/student_dashboard')
def student_dashboard():
    if 'user_id' in session and session['role'] == 'student':
        return render_template('student_dashboard.html')
    else:
        return redirect(url_for('login'))

# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']
            role = request.form['role']
            user = auth.create_user(email=email, password=password)
            db.collection('users').document(user.uid).set({
                'email': email,
                'role': role  # student, teacher, or admin
            })
            logging.info(f"New user registered: {email}")
            flash('Registration successful', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            logging.error(f"Error registering user: {e}")
            flash('Registration failed', 'danger')
            return redirect(url_for('register'))
    return render_template('register.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.get_user_by_email(email)
            # Simulate password check (use Firebase authentication for actual projects)
            if user and password == 'testpassword':  # Replace with actual authentication
                session['user_id'] = user.uid
                session['role'] = db.collection('users').document(user.uid).get().to_dict()['role']
                logging.info(f"User logged in: {email}")
                if session['role'] == 'admin':
                    return redirect(url_for('admin_dashboard'))
                elif session['role'] == 'teacher':
                    return redirect(url_for('teacher_dashboard'))
                else:
                    return redirect(url_for('student_dashboard'))
            else:
                flash('Invalid credentials', 'danger')
                return redirect(url_for('login'))
        except Exception as e:
            logging.error(f"Error logging in: {e}")
            flash('Login failed', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

# Add Teacher Route
@app.route('/add_teacher', methods=['GET', 'POST'])
def add_teacher():
    if request.method == 'POST' and 'user_id' in session and session['role'] == 'admin':
        try:
            name = request.form['name']
            department = request.form['department']
            subject = request.form['subject']
            db.collection('teachers').add({
                'name': name,
                'department': department,
                'subject': subject
            })
            logging.info(f"New teacher added: {name}")
            flash('Teacher added successfully', 'success')
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            logging.error(f"Error adding teacher: {e}")
            flash('Failed to add teacher', 'danger')
            return redirect(url_for('add_teacher'))
    return render_template('add_teacher.html')

# Book Appointment Route
@app.route('/book_appointment', methods=['GET', 'POST'])
def book_appointment():
    if request.method == 'POST' and 'user_id' in session and session['role'] == 'student':
        try:
            teacher_name = request.form['teacher_name']
            appointment_date = request.form['appointment_date']
            db.collection('appointments').add({
                'student_id': session['user_id'],
                'teacher_name': teacher_name,
                'appointment_date': appointment_date,
                'status': 'Pending'
            })
            logging.info(f"Appointment booked with {teacher_name} on {appointment_date}")
            flash('Appointment booked successfully', 'success')
            return redirect(url_for('student_dashboard'))
        except Exception as e:
            logging.error(f"Error booking appointment: {e}")
            flash('Failed to book appointment', 'danger')
            return redirect(url_for('book_appointment'))
    return render_template('book_appointment.html')

# View Appointments Route
@app.route('/view_appointments')
def view_appointments():
    if 'user_id' in session:
        user_role = session['role']
        appointments = []
        try:
            if user_role == 'student':
                appointments = db.collection('appointments').where('student_id', '==', session['user_id']).get()
            elif user_role == 'teacher':
                appointments = db.collection('appointments').where('teacher_name', '==', session['user_id']).get()
            elif user_role == 'admin':
                appointments = db.collection('appointments').get()
            appointment_list = [appointment.to_dict() for appointment in appointments]
            return render_template('view_appointments.html', appointments=appointment_list)
        except Exception as e:
            logging.error(f"Error viewing appointments: {e}")
            flash('Failed to retrieve appointments', 'danger')
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))

# View Messages Route
@app.route('/view_messages')
def view_messages():
    if 'user_id' in session and session['role'] == 'teacher':
        try:
            messages = db.collection('messages').where('teacher_id', '==', session['user_id']).get()
            message_list = [message.to_dict() for message in messages]
            return render_template('view_messages.html', messages=message_list)
        except Exception as e:
            logging.error(f"Error viewing messages: {e}")
            flash('Failed to retrieve messages', 'danger')
            return redirect(url_for('teacher_dashboard'))
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
