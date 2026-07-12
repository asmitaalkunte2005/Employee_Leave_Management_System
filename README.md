# Employee Leave Management System

Django project for managing employees and leave requests.

## Project Overview

The Employee Leave Management System is a web application developed using Django and Django REST Framework. It helps organizations manage employee records and leave requests digitally. Employees can apply for leave, and HR can manage employee details and review leave applications.

---

## Technologies Used

- Python 3
- Django
- Django REST Framework
- MySQL
- HTML
- CSS
- Bootstrap 5
- JavaScript
- Git
- GitHub

---

## Features

### Employee Management

- Add Employee
- View Employees
- Update Employee
- Delete Employee
- Search Employee by Name
- Search Employee by Employee ID

### Leave Management

- Apply Leave
- View Leave History
- Update Leave
- Delete Leave
- Filter Leave by Status
- Filter Leave by Leave Type

### Dashboard

- Total Employees
- Total Leave Applications
- Pending Leave Requests
- Approved Leave Requests
- Rejected Leave Requests

### REST APIs

#### Employee APIs

- GET All Employees
- GET Employee by ID
- POST Employee
- PUT Employee
- DELETE Employee

#### Leave APIs

- GET All Leave Records
- GET Leave by ID
- POST Leave
- PUT Leave
- DELETE Leave

---

## Project Structure

```
Employee_Leave_Management_System/
│
├── employee/
├── leave_management/
├── templates/
├── static/
├── manage.py
├── requirements.txt
└── README.md
```

---

## Database

- MySQL
- Foreign Key Relationship between Employee and Leave

---

## Installation

1. Clone the repository

```bash
git clone <repository_url>
```

2. Open the project

```bash
cd Employee_Leave_Management_System
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Configure MySQL in `settings.py`

5. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create Superuser

```bash
python manage.py createsuperuser
```

7. Run the project

```bash
python manage.py runserver
```

---

## API Endpoints

### Employee

- GET `/api/employees/`
- GET `/api/employees/<id>/`
- POST `/api/employees/create/`
- PUT `/api/employees/update/<id>/`
- DELETE `/api/employees/delete/<id>/`

### Leave

- GET `/leave/api/leaves/`
- GET `/leave/api/leaves/<id>/`
- POST `/leave/api/leaves/create/`
- PUT `/leave/api/leaves/update/<id>/`
- DELETE `/leave/api/leaves/delete/<id>/`

---

## Validation

- Required Fields
- Email Validation
- Mobile Number Validation
- Date Validation (From Date should not be greater than To Date)

---

## Future Enhancements

- Login & Logout
- Pagination
- API Authentication
- AJAX Search
- Email Notifications
- Deployment

---

## Author

**Name:** Asmita Alkunte

Python Full Stack Development Project

The Kiran Academy