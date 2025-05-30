"""
Database Initialization Script for College Placement Portal
This script populates the database with test data for development and testing
"""
from app import app, db, User, Student, Company, Job, Skill, StudentSkill, JobSkill, Application, Notification
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random

# Sample data
STUDENT_NAMES = [
    "Priya Sharma", "Rahul Mehra", "Ananya Singh", "Vikram Patel", 
    "Neha Gupta", "Arjun Kumar", "Divya Reddy", "Karthik Iyer", 
    "Sanya Malhotra", "Akash Verma"
]

COURSES = [
    "B.Tech", "M.Tech", "BBA", "MBA", "B.Sc", "M.Sc"
]

BRANCHES = [
    "Computer Science", "Information Technology", "Electronics", "Mechanical",
    "Civil", "Electrical", "Finance", "Marketing", "Operations", "Physics", "Chemistry"
]

COMPANY_NAMES = [
    "TechSolutions Inc.", "GlobalFinance Corp", "InnovateSoft", "WebDev Experts",
    "DataAnalytics Pro", "CloudTech Systems", "ConsultPro Services", "MobileSoft Inc.",
    "SecurityTech", "EcomGiant"
]

INDUSTRIES = [
    "Information Technology", "Finance & Banking", "Consulting", "E-commerce", 
    "Healthcare", "Education", "Manufacturing", "Telecommunications"
]

LOCATIONS = [
    "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", 
    "Pune", "Kolkata", "Ahmedabad", "Jaipur"
]

JOB_TITLES = [
    "Software Engineer", "Data Scientist", "Web Developer", "Product Manager",
    "UI/UX Designer", "System Administrator", "Network Engineer", "Business Analyst",
    "Marketing Specialist", "HR Manager", "Financial Analyst"
]

SKILLS = [
    "Python", "Java", "JavaScript", "HTML/CSS", "React", "Angular", "Node.js", 
    "SQL", "MongoDB", "Docker", "AWS", "Machine Learning", "Data Analysis", 
    "Project Management", "Communication", "Leadership", "Problem Solving"
]

def create_admin():
    """Create admin user if it doesn't exist"""
    admin = User.query.filter_by(username='admin@example.com').first()
    if not admin:
        new_admin = User(
            username='admin@example.com',
            email='admin@example.com',
            password=generate_password_hash('admin123'),
            role='admin',
            is_approved=True
        )
        db.session.add(new_admin)
        print("Admin user created: admin@example.com / admin123")
    else:
        print("Admin user already exists")
        
def create_students(count=5):
    """Create student users and profiles"""
    print(f"Creating {count} student users...")
    for i in range(count):
        # Generate student data
        name = random.choice(STUDENT_NAMES)
        email = f"student{i+1}@example.com"
        student_id = f"S{2023000 + i+1}"
        course = random.choice(COURSES)
        branch = random.choice(BRANCHES)
        cgpa = round(random.uniform(6.0, 10.0), 2)
        graduation_year = random.randint(2023, 2027)
        phone = f"+91-{random.randint(7000000000, 9999999999)}"
        
        # Create user
        user = User(
            username=email,
            email=email,
            password=generate_password_hash(f"student{i+1}"),
            role='student',
            is_approved=True
        )
        db.session.add(user)
        db.session.flush()  # Get the user ID
        
        # Create student profile
        student = Student(
            user_id=user.id,
            full_name=name,
            student_id=student_id,
            course=course,
            branch=branch,
            cgpa=cgpa,
            graduation_year=graduation_year,
            phone=phone,
            bio=f"I am a {course} student with interests in {branch}. Looking for opportunities to grow my career."
        )
        db.session.add(student)
        db.session.flush()
        
        # Add skills to student
        skills_count = random.randint(3, 7)
        selected_skills = random.sample(SKILLS, skills_count)
        for skill_name in selected_skills:
            # Find or create skill
            skill = Skill.query.filter_by(name=skill_name).first()
            if not skill:
                skill = Skill(name=skill_name)
                db.session.add(skill)
                db.session.flush()
            
            # Link skill to student
            student_skill = StudentSkill(student_id=student.id, skill_id=skill.id)
            db.session.add(student_skill)
        
        print(f"  - Created student: {name} ({email})")
    
    db.session.commit()

def create_companies(count=3):
    """Create company users and profiles"""
    print(f"Creating {count} company users...")
    for i in range(count):
        # Generate company data
        name = random.choice(COMPANY_NAMES)
        email = f"company{i+1}@example.com"
        industry = random.choice(INDUSTRIES)
        location = random.choice(LOCATIONS)
        phone = f"+91-{random.randint(7000000000, 9999999999)}"
        hr_name = random.choice(STUDENT_NAMES)  # Reusing student names for HR
        
        # Create user
        user = User(
            username=email,
            email=email,
            password=generate_password_hash(f"company{i+1}"),
            role='company',
            is_approved=True
        )
        db.session.add(user)
        db.session.flush()  # Get the user ID
        
        # Create company profile
        company = Company(
            user_id=user.id,
            company_name=name,
            industry=industry,
            location=location,
            website=f"https://www.{name.lower().replace(' ', '').replace('.', '')}.com",
            phone=phone,
            description=f"{name} is a leading company in the {industry} industry. We are looking for talented professionals to join our team.",
            hr_name=hr_name
        )
        db.session.add(company)
        
        print(f"  - Created company: {name} ({email})")
    
    db.session.commit()
    
def create_jobs(count_per_company=2):
    """Create job postings for companies"""
    print("Creating job postings...")
    companies = Company.query.all()
    
    for company in companies:
        for i in range(count_per_company):
            # Generate job data
            title = random.choice(JOB_TITLES)
            job_type = random.choice(["full-time", "internship", "contract"])
            location = company.location
            compensation = f"₹{random.randint(500000, 2000000)}/year"
            cgpa_cutoff = round(random.uniform(6.0, 8.5), 1)
            positions = random.randint(1, 10)
            deadline = datetime.utcnow() + timedelta(days=random.randint(30, 90))
            
            # Create job
            job = Job(
                company_id=company.id,
                title=title,
                job_type=job_type,
                location=location,
                compensation=compensation,
                description=f"We are looking for a talented {title} to join our team. This is a {job_type} position based in {location}.",
                requirements=f"- Minimum {cgpa_cutoff} CGPA\n- Strong communication skills\n- Relevant experience in {company.industry}",
                cgpa_cutoff=cgpa_cutoff,
                positions=positions,
                deadline=deadline,
                is_active=True,
                is_approved=True
            )
            db.session.add(job)
            db.session.flush()
            
            # Add required skills to job
            skills_count = random.randint(3, 5)
            selected_skills = random.sample(SKILLS, skills_count)
            for skill_name in selected_skills:
                # Find or create skill
                skill = Skill.query.filter_by(name=skill_name).first()
                if not skill:
                    skill = Skill(name=skill_name)
                    db.session.add(skill)
                    db.session.flush()
                
                # Link skill to job
                job_skill = JobSkill(job_id=job.id, skill_id=skill.id)
                db.session.add(job_skill)
            
            print(f"  - Created job: {title} at {company.company_name}")
    
    db.session.commit()

def create_applications():
    """Create job applications for students"""
    print("Creating job applications...")
    students = Student.query.all()
    jobs = Job.query.all()
    
    if not students or not jobs:
        print("No students or jobs available to create applications.")
        return
    
    statuses = ["pending", "shortlisted", "interviewed", "offered", "rejected"]
    
    for student in students:
        # Each student applies to 1-3 jobs
        applied_jobs = random.sample(jobs, min(random.randint(1, 3), len(jobs)))
        
        for job in applied_jobs:
            # Check if student meets CGPA requirement
            if student.cgpa >= job.cgpa_cutoff:
                # Create application with random status
                status = random.choice(statuses)
                application = Application(
                    student_id=student.id,
                    job_id=job.id,
                    applied_at=datetime.utcnow() - timedelta(days=random.randint(1, 30)),
                    status=status
                )
                db.session.add(application)
                
                # Create notifications
                if status != "pending":
                    notification = Notification(
                        user_id=student.user_id,
                        message=f"Your application for {job.title} at {job.company.company_name} has been updated to: {status}",
                        created_at=datetime.utcnow() - timedelta(days=random.randint(1, 10)),
                        is_read=random.choice([True, False])
                    )
                    db.session.add(notification)
                
                print(f"  - Created application: {student.full_name} applied to {job.title} at {job.company.company_name} (Status: {status})")
    
    db.session.commit()

def initialize_database():
    """Initialize the database with test data"""
    print("\n=== Initializing College Placement Portal Database ===\n")
    
    # Create admin user
    create_admin()
    
    # Create students
    create_students(count=10)
    
    # Create companies
    create_companies(count=5)
    
    # Create jobs
    create_jobs(count_per_company=3)
    
    # Create applications
    create_applications()
    
    print("\n=== Database initialization complete! ===\n")
    print("You can now log in with the following accounts:")
    print("  - Admin: admin@example.com / admin123")
    print("  - Students: student1@example.com, student2@example.com, etc. (Password matches username without @example.com)")
    print("  - Companies: company1@example.com, company2@example.com, etc. (Password matches username without @example.com)")

if __name__ == "__main__":
    with app.app_context():
        initialize_database()
