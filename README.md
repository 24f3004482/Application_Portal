# Placement Portal

A comprehensive web application for managing campus placement drives, built with Flask. This portal facilitates the entire placement process by connecting students, companies, and administrators in a streamlined workflow.

## Features

### For Students
- **Registration & Profile Management**: Create accounts and manage personal profiles including resume uploads
- **Browse Placement Drives**: View approved placement drives from registered companies
- **Apply to Drives**: Submit applications to eligible placement opportunities
- **Application History**: Track all submitted applications and their current status

### For Companies
- **Company Registration**: Register and get approval from administrators
- **Profile Management**: Maintain company information, HR contacts, and descriptions
- **Drive Creation**: Post new placement drives with job details, eligibility criteria, and deadlines
- **Application Management**: Review student applications and update their status (Shortlisted, Selected, Rejected)

### For Administrators
- **User Management**: Approve/reject company registrations and manage user accounts
- **Drive Oversight**: Review and approve placement drives before they become visible to students
- **System Monitoring**: View statistics on students, companies, drives, and applications
- **Blacklist Management**: Control access by blacklisting problematic users

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Flask-Login for session management
- **Security**: Werkzeug for password hashing and file security
- **Frontend**: HTML templates with Jinja2 templating

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or download the project**
   ```bash
   cd /path/to/project
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   - Copy `.env` file and update the values:
   ```bash
   copy .env .env.local  # Edit .env.local with your settings
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   - Open your browser and go to `http://localhost:5000`
   - Default admin credentials: `admin@institute.edu` / `adminpassword`

## Configuration

The application uses environment variables for configuration. Key settings in `.env`:

- `PLACEMENT_SECRET_KEY`: Flask secret key for session security
- `DATABASE_URI`: Database connection string (default: SQLite)
- `ADMIN_EMAIL`: Default admin email address
- `ADMIN_PASSWORD`: Default admin password
- `FLASK_ENV`: Environment mode (development/production)
- `FLASK_DEBUG`: Enable/disable debug mode

## Project Structure

```
placement-portal/
├── app.py                 # Main Flask route wrapper and app startup
├── auth/                  # Authentication routes and admin setup
│   ├── login.py
│   ├── register.py
│   ├── logout.py
│   └── admin_setup.py
├── admin/                 # Admin dashboards and management actions
│   ├── dashboard.py
│   ├── companies.py
│   ├── students.py
│   ├── drives.py
│   └── applications.py
├── company/               # Company dashboards and drive management
│   ├── dashboard.py
│   ├── profile.py
│   ├── drives.py
│   └── applications.py
├── student/               # Student dashboards and application flows
│   ├── dashboard.py
│   ├── profile.py
│   ├── drives.py
│   └── history.py
├── utils/                 # Shared helpers and database initialization
│   ├── database.py
│   └── helpers.py
├── models.py              # SQLAlchemy database models
├── requirements.txt       # Python dependencies
├── .env                   # Environment configuration template
├── .env.local             # Local environment overrides (ignored)
├── .gitignore             # Git ignore rules
├── placement_portal.db    # Local SQLite database file
├── static/                # Static assets
│   └── uploads/
│       └── resumes/       # Student resume uploads
└── templates/             # Jinja2 HTML templates
    ├── base.html
    ├── login.html
    ├── register.html
    ├── admin_*.html
    ├── company_*.html
    └── student_*.html
```

## Usage

### First Time Setup
1. Run the application - it will automatically create the database and default admin user
2. Log in as admin to approve companies and drives

### Workflow
1. **Companies** register and wait for admin approval
2. **Approved companies** can create placement drives
3. **Admins** review and approve placement drives
4. **Students** can browse approved drives and submit applications
5. **Companies** review applications and update statuses
6. **Students** can track their application history

## Security Features

- Password hashing using Werkzeug
- Session-based authentication
- Role-based access control
- File upload restrictions (PDF, DOC, DOCX only)
- SQL injection protection via SQLAlchemy
- CSRF protection via Flask-WTF (forms)

## Development

### Running in Debug Mode
Set `FLASK_DEBUG=True` in your `.env` file for development features like auto-reload.

### Database Migrations
The application uses SQLAlchemy with automatic table creation. For production deployments, consider using Flask-Migrate for proper migration management.

### Adding New Features
- Models are defined in `models.py`
- Routes are organized by user role in `app.py`
- Templates follow the naming convention: `{role}_{feature}.html`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source. Please check the license file for details.

## Support

For issues or questions, please check the code comments or create an issue in the repository.