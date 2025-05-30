# College Placement Portal

A modern web application for managing college placement activities. The portal connects students with companies for campus recruitment.

## Features

### For Students
- Create and manage professional profiles
- Upload resumes and showcase skills
- Apply to job openings from registered companies
- Track application status
- Receive notifications about job opportunities and application updates

### For Companies
- Create company profiles with details and branding
- Post job opportunities with requirements and qualifications
- Review and filter student applications
- Manage the recruitment workflow
- Track hiring progress and statistics

### For Administrators
- Approve student and company registrations
- Monitor placement activities
- Generate reports and analytics
- Manage the entire placement process
- Access and manage database records

## Database Information

### Database Location
The SQLite database file is located at:
```
instance/placement_portal.db
```

### Database Tables
The database consists of the following tables:
- `user` - User accounts (students, companies, admins)
- `student` - Student profiles with academic details
- `company` - Company profiles with industry information
- `job` - Job postings with requirements and details
- `application` - Student applications for jobs
- `skill` - Available skills in the system
- `student_skill` - Skills associated with students
- `job_skill` - Skills required for jobs
- `notification` - System notifications for users

### Accessing the Database

#### Through Admin Dashboard
1. Log in as an administrator (admin@example.com / admin123)
2. Navigate to the "Database" tab in the admin dashboard
3. View and explore the database tables

#### Using Database Initialization Script
To populate the database with test data, run:
```bash
python init_db.py
```

#### Using External Tools
For more advanced database management, you can use tools like:
- DB Browser for SQLite (https://sqlitebrowser.org/dl/)
- SQLite command-line tools
- Approve student and company registrations
- Monitor placement activities
- Generate reports and analytics
- Manage the entire placement process

## Technology Stack

### Frontend
- HTML5, CSS3, JavaScript
- Modern responsive design with animations
- Custom CSS for styling

### Backend
- Python with Flask framework
- SQLAlchemy ORM for database operations
- Werkzeug for security and utilities

### Database
- SQLite for development (can be upgraded to PostgreSQL/MySQL for production)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/college-placement-portal.git
cd college-placement-portal
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and go to:
```
http://127.0.0.1:5000
```

## Installation and Setup

1. Clone the repository:
```
git clone <repository-url>
cd college-placement-portal
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Set up the environment variables (create a .env file):
```
SECRET_KEY=your_secret_key_here
FLASK_APP=app.py
FLASK_ENV=development
```

4. Initialize the database:
```
flask shell
>>> from app import db
>>> db.create_all()
>>> exit()
```

5. Run the application:
```
flask run
```

6. Access the application:
Open your browser and navigate to `http://127.0.0.1:5000`

## Project Structure

```
college-placement-portal/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── static/                # Static files (CSS, JS, uploads)
│   ├── css/
│   │   └── styles.css     # Main stylesheet
│   ├── js/                # JavaScript files
│   └── uploads/           # User uploads (resumes, logos)
│       ├── resumes/
│       └── logos/
└── templates/             # HTML templates
    ├── base.html          # Base template with common elements
    ├── index.html         # Homepage
    ├── login.html         # Login page
    ├── register.html      # Registration page
    ├── student-dashboard.html
    ├── company-dashboard.html
    └── admin-dashboard.html
```

## User Roles

1. **Student**: Can create profiles, apply to jobs, and track applications
2. **Company**: Can post jobs, review applications, and manage recruitment
3. **Admin**: Has full access to manage the portal, approve registrations, and generate reports

## Future Enhancements

- Advanced search and filtering for jobs and candidates
- Integration with email notifications
- Online assessment and interview scheduling
- Data visualization for placement statistics
- Mobile app integration

## License

This project is licensed under the MIT License - see the LICENSE file for details.
