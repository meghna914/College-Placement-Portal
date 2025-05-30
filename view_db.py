from app import app, db, User, Student, Company
import os

def view_database():
    """View database tables and their contents"""
    print("\n=== DATABASE EXPLORER ===")
    print("Database location:", os.path.join(app.root_path, 'instance', 'placement_portal.db'))
    print("\n=== TABLES ===")
    for table_name in db.metadata.tables.keys():
        print(f"- {table_name}")
    
    print("\n=== USERS ===")
    users = User.query.all()
    print(f"Total users: {len(users)}")
    for i, user in enumerate(users[:5], 1):  # Show first 5 users
        print(f"{i}. {user.username} ({user.email}) - Role: {user.role} - Approved: {user.is_approved}")
    
    if len(users) > 5:
        print(f"... and {len(users) - 5} more users")
    
    # Check if there are any students
    print("\n=== STUDENTS ===")
    students = Student.query.all()
    print(f"Total students: {len(students)}")
    for i, student in enumerate(students[:5], 1):  # Show first 5 students
        print(f"{i}. ID: {student.student_id}, Name: {student.full_name}")
        print(f"   Course: {student.course}, Branch: {student.branch}, CGPA: {student.cgpa}")
    
    if len(students) > 5:
        print(f"... and {len(students) - 5} more students")
    
    # Check if there are any companies
    print("\n=== COMPANIES ===")
    companies = Company.query.all()
    print(f"Total companies: {len(companies)}")
    for i, company in enumerate(companies[:5], 1):  # Show first 5 companies
        print(f"{i}. {company.name}")
        print(f"   Industry: {company.industry}, Location: {company.location}")
    
    if len(companies) > 5:
        print(f"... and {len(companies) - 5} more companies")

if __name__ == "__main__":
    with app.app_context():
        view_database()
