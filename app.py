from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import os
from datetime import datetime

# Initialize Flask app
app = Flask(__name__, 
           static_folder='static',
           template_folder='templates')
app.secret_key = 'your_secret_key_here'  # Change this to a random string in production

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///placement_portal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# File upload configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'student', 'company', 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_approved = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    course = db.Column(db.String(50), nullable=False)
    branch = db.Column(db.String(50), nullable=False)
    cgpa = db.Column(db.Float, nullable=True)
    graduation_year = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String(15), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    resume_path = db.Column(db.String(255), nullable=True)
    
    user = db.relationship('User', backref=db.backref('student', uselist=False))
    
    def __repr__(self):
        return f'<Student {self.full_name}>'

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    industry = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    website = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(15), nullable=False)
    description = db.Column(db.Text, nullable=True)
    hr_name = db.Column(db.String(100), nullable=False)
    logo_path = db.Column(db.String(255), nullable=True)
    
    user = db.relationship('User', backref=db.backref('company', uselist=False))
    
    def __repr__(self):
        return f'<Company {self.company_name}>'

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    job_type = db.Column(db.String(20), nullable=False)  # 'full-time', 'internship', 'contract'
    location = db.Column(db.String(100), nullable=False)
    compensation = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text, nullable=False)
    cgpa_cutoff = db.Column(db.Float, nullable=False)
    positions = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deadline = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    is_approved = db.Column(db.Boolean, default=True)
    
    company = db.relationship('Company', backref=db.backref('jobs', lazy=True))
    
    def __repr__(self):
        return f'<Job {self.title} by {self.company.company_name}>'

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # 'pending', 'shortlisted', 'interviewed', 'offered', 'rejected'
    
    student = db.relationship('Student', backref=db.backref('applications', lazy=True))
    job = db.relationship('Job', backref=db.backref('applications', lazy=True))
    
    def __repr__(self):
        return f'<Application {self.student.full_name} for {self.job.title}>'

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    def __repr__(self):
        return f'<Skill {self.name}>'

class StudentSkill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'), nullable=False)
    
    student = db.relationship('Student', backref=db.backref('skills', lazy=True))
    skill = db.relationship('Skill', backref=db.backref('students', lazy=True))
    
    def __repr__(self):
        return f'<StudentSkill {self.student.full_name} - {self.skill.name}>'

class JobSkill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'), nullable=False)
    
    job = db.relationship('Job', backref=db.backref('required_skills', lazy=True))
    skill = db.relationship('Skill', backref=db.backref('jobs', lazy=True))
    
    def __repr__(self):
        return f'<JobSkill {self.job.title} - {self.skill.name}>'

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)
    
    user = db.relationship('User', backref=db.backref('notifications', lazy=True))
    
    def __repr__(self):
        return f'<Notification for {self.user.username}>'

# Create the database tables
with app.app_context():
    db.create_all()
    
    # Create default admin user if it doesn't exist
    admin = User.query.filter_by(username='admin@example.com').first()
    if not admin:
        admin_user = User(
            username='admin@example.com',
            email='admin@example.com',
            password=generate_password_hash('admin123'),
            role='admin',
            is_approved=True
        )
        db.session.add(admin_user)
        db.session.commit()
        print('Default admin user created: admin@example.com / admin123')

# Login decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('login'))
            
            user = User.query.filter_by(id=session['user_id']).first()
            if user.role not in roles:
                flash('Access denied: You do not have permission to access this page.')
                return redirect(url_for('index'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.args.get('role', 'student')
        
        user = User.query.filter_by(username=username, role=role).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            
            if user.role == 'student':
                return redirect(url_for('student_dashboard'))
            elif user.role == 'company':
                return redirect(url_for('company_dashboard'))
            elif user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password')
    
    role = request.args.get('role', 'student')
    return render_template('login.html', role=role)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        role = request.args.get('role', 'student')
        
        # Create user account
        username = request.form['email']  # Using email as username
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        
        # Check if user already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Email already registered')
            return redirect(url_for('register', role=role))
        
        # Create new user (automatically approved)
        new_user = User(username=username, email=email, password=password, role=role, is_approved=True)
        db.session.add(new_user)
        db.session.flush()  # Get the user ID
        
        if role == 'student':
            # Create student profile
            new_student = Student(
                user_id=new_user.id,
                full_name=request.form['student-name'],
                student_id=request.form['student-id'],
                course=request.form['student-course'],
                branch=request.form['student-branch'],
                graduation_year=request.form['student-graduation-year'],
                phone=request.form['student-phone'],
                bio=request.form.get('student-bio', '')
            )
            db.session.add(new_student)
            
        elif role == 'company':
            # Create company profile
            new_company = Company(
                user_id=new_user.id,
                company_name=request.form['company-name'],
                industry=request.form['company-industry'],
                location=request.form['company-location'],
                website=request.form.get('company-website', ''),
                phone=request.form['company-phone'],
                description=request.form['company-description'],
                hr_name=request.form['hr-name']
            )
            db.session.add(new_company)
        
        db.session.commit()

        flash('Registration successful! You can now login to your account.')
        return redirect(url_for('login', role=role))
    
    role = request.args.get('role', 'student')
    return render_template('register.html', role=role)

@app.route('/student-dashboard')
@login_required
@role_required(['student'])
def student_dashboard():
    user_id = session['user_id']
    student = Student.query.filter_by(user_id=user_id).first()
    
    if not student:
        return redirect(url_for('logout'))
    
    # Get student's applications
    applications = Application.query.filter_by(student_id=student.id).all()
    
    # Get eligible jobs (based on CGPA and other criteria)
    eligible_jobs = []
    if student.cgpa:
        eligible_jobs = Job.query.filter(
            Job.cgpa_cutoff <= student.cgpa,
            Job.is_active == True
        ).all()
    
    # Get student skills
    student_skills = StudentSkill.query.filter_by(student_id=student.id).all()
    skills = [skill.skill for skill in student_skills]
    
    # Get notifications
    notifications = Notification.query.filter_by(user_id=user_id).order_by(Notification.created_at.desc()).limit(10).all()
    
    return render_template(
        'student-dashboard.html', 
        student=student, 
        applications=applications, 
        eligible_jobs=eligible_jobs,
        skills=skills,
        notifications=notifications
    )

@app.route('/company-dashboard')
@login_required
@role_required(['company'])
def company_dashboard():
    user_id = session['user_id']
    company = Company.query.filter_by(user_id=user_id).first()
    
    if not company:
        return redirect(url_for('logout'))
    
    # Get company's job postings
    jobs = Job.query.filter_by(company_id=company.id).all()
    
    # Get notifications
    notifications = Notification.query.filter_by(user_id=user_id).order_by(Notification.created_at.desc()).limit(10).all()
    
    return render_template(
        'company-dashboard.html', 
        company=company, 
        jobs=jobs, 
        notifications=notifications
    )

@app.route('/admin-dashboard')
@login_required
@role_required(['admin'])
def admin_dashboard():
    # Get counts for dashboard
    student_count = Student.query.count()
    company_count = Company.query.count()
    job_count = Job.query.count()
    placed_count = Application.query.filter_by(status='offered').count()
    
    # Get all students, companies, and jobs for admin management
    all_students = Student.query.join(User).all()
    all_companies = Company.query.join(User).all()
    all_jobs = Job.query.all()

    return render_template(
        'admin-dashboard.html',
        student_count=student_count,
        company_count=company_count,
        job_count=job_count,
        placed_count=placed_count,
        all_students=all_students,
        all_companies=all_companies,
        all_jobs=all_jobs
    )

# API routes for AJAX calls
@app.route('/api/jobs')
@login_required
@role_required(['student'])
def get_jobs():
    jobs = Job.query.filter_by(is_active=True).all()
    result = []
    
    for job in jobs:
        company = Company.query.get(job.company_id)
        result.append({
            'id': job.id,
            'title': job.title,
            'company': company.company_name,
            'location': job.location,
            'compensation': job.compensation,
            'job_type': job.job_type,
            'deadline': job.deadline.strftime('%Y-%m-%d') if job.deadline else None
        })
    
    return jsonify(result)

@app.route('/api/apply/<int:job_id>', methods=['POST'])
@login_required
@role_required(['student'])
def apply_job(job_id):
    user_id = session['user_id']
    student = Student.query.filter_by(user_id=user_id).first()
    
    if not student:
        return jsonify({'success': False, 'message': 'Student profile not found'})
    
    job = Job.query.get(job_id)
    if not job:
        return jsonify({'success': False, 'message': 'Job not found'})
    
    # Check if already applied
    existing_application = Application.query.filter_by(student_id=student.id, job_id=job_id).first()
    if existing_application:
        return jsonify({'success': False, 'message': 'Already applied for this job'})
    
    # Check eligibility
    if job.cgpa_cutoff > student.cgpa:
        return jsonify({'success': False, 'message': 'You do not meet the CGPA requirement for this job'})
    
    # Create application
    new_application = Application(student_id=student.id, job_id=job_id)
    db.session.add(new_application)
    
    # Create notification for company
    company = Company.query.get(job.company_id)
    notification = Notification(
        user_id=company.user_id,
        message=f"New application received for {job.title} from {student.full_name}"
    )
    db.session.add(notification)
    
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Application submitted successfully'})

@app.route('/api/post-job', methods=['POST'])
@login_required
@role_required(['company'])
def post_job():
    user_id = session['user_id']
    company = Company.query.filter_by(user_id=user_id).first()
    
    if not company:
        return jsonify({'success': False, 'message': 'Company profile not found'})
    
    data = request.form
    
    new_job = Job(
        company_id=company.id,
        title=data['title'],
        job_type=data['job_type'],
        location=data['location'],
        compensation=data['compensation'],
        description=data['description'],
        requirements=data['requirements'],
        cgpa_cutoff=float(data['cgpa_cutoff']),
        positions=int(data['positions']),
        deadline=datetime.strptime(data['deadline'], '%Y-%m-%d') if data.get('deadline') else None,
        is_approved=True  # Automatically approve new jobs
    )
    db.session.add(new_job)
    
    # Add required skills
    if 'skills' in data:
        skills = data['skills'].split(',')
        for skill_name in skills:
            skill_name = skill_name.strip()
            if skill_name:
                # Find or create skill
                skill = Skill.query.filter_by(name=skill_name).first()
                if not skill:
                    skill = Skill(name=skill_name)
                    db.session.add(skill)
                    db.session.flush()
                
                # Link skill to job
                job_skill = JobSkill(job_id=new_job.id, skill_id=skill.id)
                db.session.add(job_skill)
    
    db.session.commit()

    return jsonify({'success': True, 'message': 'Job posted successfully and is now live!'})

@app.route('/api/update-profile', methods=['POST'])
@login_required
def update_profile():
    user_id = session['user_id']
    user = db.session.get(User, user_id)
    
    if not user:
        return jsonify({'success': False, 'message': 'User not found'})
    
    data = request.form
    
    if user.role == 'student':
        student = Student.query.filter_by(user_id=user_id).first()
        if not student:
            return jsonify({'success': False, 'message': 'Student profile not found'})
        
        student.full_name = data.get('full_name', student.full_name)
        student.cgpa = float(data.get('cgpa', student.cgpa))
        student.graduation_year = int(data.get('graduation_year', student.graduation_year))
        student.phone = data.get('phone', student.phone)
        student.bio = data.get('bio', student.bio)
        
        # Handle resume upload
        if 'resume' in request.files:
            resume_file = request.files['resume']
            if resume_file.filename != '':
                filename = f"resume_{user_id}_{int(datetime.now(datetime.timezone.utc).timestamp())}.pdf"
                resume_path = os.path.join(app.root_path, 'static', 'uploads', 'resumes', filename)
                os.makedirs(os.path.dirname(resume_path), exist_ok=True)
                resume_file.save(resume_path)
                student.resume_path = f"/static/uploads/resumes/{filename}"
        
        # Update skills
        if 'skills' in data:
            # Clear existing skills
            StudentSkill.query.filter_by(student_id=student.id).delete()
            
            # Add new skills
            skills = data['skills'].split(',')
            for skill_name in skills:
                skill_name = skill_name.strip()
                if skill_name:
                    # Find or create skill
                    skill = Skill.query.filter_by(name=skill_name).first()
                    if not skill:
                        skill = Skill(name=skill_name)
                        db.session.add(skill)
                        db.session.flush()
                    
                    # Link skill to student
                    student_skill = StudentSkill(student_id=student.id, skill_id=skill.id)
                    db.session.add(student_skill)
    
    elif user.role == 'company':
        company = Company.query.filter_by(user_id=user_id).first()
        if not company:
            return jsonify({'success': False, 'message': 'Company profile not found'})
        
        company.company_name = data.get('company_name', company.company_name)
        company.industry = data.get('industry', company.industry)
        company.location = data.get('location', company.location)
        company.website = data.get('website', company.website)
        company.phone = data.get('phone', company.phone)
        company.description = data.get('description', company.description)
        company.hr_name = data.get('hr_name', company.hr_name)
        
        # Handle logo upload
        if 'logo' in request.files:
            logo_file = request.files['logo']
            if logo_file.filename != '':
                filename = f"logo_{user_id}_{int(datetime.now(datetime.timezone.utc).timestamp())}.png"
                logo_path = os.path.join(app.root_path, 'static', 'uploads', 'logos', filename)
                os.makedirs(os.path.dirname(logo_path), exist_ok=True)
                logo_file.save(logo_path)
                company.logo_path = f"/static/uploads/logos/{filename}"
    
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Profile updated successfully'})

# Admin API routes
# Removed approval routes - users and jobs are now automatically approved

# Company application management
@app.route('/api/company/update-application-status', methods=['POST'])
@login_required
@role_required(['company'])
def update_application_status():
    data = request.json
    application_id = data.get('application_id')
    new_status = data.get('status')
    
    application = Application.query.get(application_id)
    
    if not application:
        return jsonify({'success': False, 'message': 'Application not found'})
    
    # Ensure company can only update their own job applications
    user_id = session['user_id']
    company = Company.query.filter_by(user_id=user_id).first()
    
    if application.job.company_id != company.id:
        return jsonify({'success': False, 'message': 'Not authorized to update this application'})
    
    valid_statuses = ['pending', 'shortlisted', 'interviewed', 'offered', 'rejected']
    if new_status not in valid_statuses:
        return jsonify({'success': False, 'message': 'Invalid status'})
    
    application.status = new_status
    
    # Create notification for student
    notification = Notification(
        user_id=application.student.user_id,
        message=f"Your application for '{application.job.title}' has been updated to: {new_status}"
    )
    db.session.add(notification)
    
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Application status updated successfully'})

@app.route('/api/notifications/read/<int:notification_id>', methods=['POST'])
@login_required
def mark_notification_read(notification_id):
    user_id = session['user_id']
    notification = Notification.query.get(notification_id)
    
    if not notification:
        return jsonify({'success': False, 'message': 'Notification not found'})
    
    # Ensure user can only mark their own notifications
    if notification.user_id != user_id:
        return jsonify({'success': False, 'message': 'Not authorized to update this notification'})
    
    notification.is_read = True
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Notification marked as read'})

@app.route('/api/student-profile/<int:student_id>')
@login_required
@role_required(['company', 'admin'])
def get_student_profile(student_id):
    student = Student.query.get(student_id)
    
    if not student:
        return jsonify({'success': False, 'message': 'Student not found'})
    
    # Get student's skills
    skills = []
    student_skills = StudentSkill.query.filter_by(student_id=student.id).all()
    for student_skill in student_skills:
        skills.append(student_skill.skill.name)
    
    return jsonify({
        'success': True,
        'student': {
            'id': student.id,
            'full_name': student.full_name,
            'student_id': student.student_id,
            'course': student.course,
            'branch': student.branch,
            'cgpa': student.cgpa,
            'graduation_year': student.graduation_year,
            'phone': student.phone,
            'bio': student.bio,
            'skills': skills,
            'resume_path': student.resume_path
        }
    })

@app.route('/api/jobs/<int:job_id>/toggle-status', methods=['POST'])
@login_required
@role_required(['company'])
def toggle_job_status(job_id):
    user_id = session['user_id']
    company = Company.query.filter_by(user_id=user_id).first()
    
    if not company:
        return jsonify({'success': False, 'message': 'Company profile not found'})
    
    job = Job.query.get(job_id)
    if not job:
        return jsonify({'success': False, 'message': 'Job not found'})
    
    # Ensure company can only toggle their own jobs
    if job.company_id != company.id:
        return jsonify({'success': False, 'message': 'Not authorized to update this job'})
    
    job.is_active = not job.is_active
    db.session.commit()
    
    return jsonify({
        'success': True, 
        'message': 'Job status updated successfully',
        'is_active': job.is_active
    })

@app.route('/api/admin/reject-user/<int:user_id>', methods=['POST'])
@login_required
@role_required(['admin'])
def reject_user(user_id):
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'success': False, 'message': 'User not found'})
    
    # Create notification for user
    notification = Notification(
        user_id=user.id,
        message=f"Your registration has been rejected. Please contact the administrator for more information."
    )
    db.session.add(notification)
    
    # Delete user account
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'User rejected successfully'})

@app.route('/api/admin/reject-job/<int:job_id>', methods=['POST'])
@login_required
@role_required(['admin'])
def reject_job(job_id):
    job = Job.query.get(job_id)
    
    if not job:
        return jsonify({'success': False, 'message': 'Job not found'})
    
    # Create notification for company
    company = Company.query.get(job.company_id)
    notification = Notification(
        user_id=company.user_id,
        message=f"Your job posting '{job.title}' has been rejected. Please contact the administrator for more information."
    )
    db.session.add(notification)
    
    # Delete job posting
    db.session.delete(job)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Job rejected successfully'})

if __name__ == '__main__':
    app.run(debug=True)
