# 🏥 Healthcare Role-Based Access Control API

A **Django REST Framework** backend API for a healthcare management system featuring role-based access control (RBAC), custom permissions, token authentication, and Docker support.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Data Models](#data-models)
- [Custom Permissions](#custom-permissions)
- [API Endpoints](#api-endpoints)
- [Setup & Installation](#setup--installation)
  - [Local Setup](#local-setup)
  - [Docker Setup](#docker-setup)
- [Environment Variables](#environment-variables)
- [Authentication](#authentication)
- [Usage Examples](#usage-examples)

---

## 📖 Overview

This project demonstrates how to implement **custom rules and permissions** in Django REST Framework for a healthcare domain. It supports four distinct user roles — **Admin**, **Doctor**, **Patient**, and **Staff** — each with their own profile model, validation logic, and access restrictions.

---

## ✨ Features

- 🔐 **Token-Based Authentication** using DRF's `TokenAuthentication`
- 👥 **Role-Based Access Control** with custom permission classes
- 🏗️ **Automatic Profile Creation** on user registration (Admin, Doctor, Patient, Staff)
- 🩺 **Doctor-controlled Staff Management** — only doctors can create staff under them
- 🛡️ **Django Group & Permission System** integration
- 🐳 **Dockerized** with PostgreSQL support
- ☁️ **Heroku-ready** (`Procfile`, `runtime.txt` included)

---

## 🛠️ Tech Stack

| Technology        | Version / Purpose                  |
|-------------------|------------------------------------|
| Python            | 3.x                                |
| Django            | REST Framework backend             |
| Django REST Framework | API layer                      |
| PostgreSQL        | Production database (via Docker)   |
| SQLite            | Local/development database         |
| Docker & Docker Compose | Containerization             |
| Token Auth        | DRF built-in authentication        |

---

## 📁 Project Structure

```
project1/
├── app1/                        # Core application
│   ├── models.py                # User & profile models
│   ├── serializers.py           # Registration, login, staff serializers
│   ├── views.py                 # AuthView, DoctorView (ViewSets)
│   ├── permissions.py           # Custom permission classes
│   ├── admin.py                 # Django admin registration
│   └── migrations/              # Database migrations
├── project1/                    # Django project config
│   ├── settings.py              # Project settings
│   ├── urls.py                  # Root URL configuration
│   ├── wsgi.py
│   └── asgi.py
├── manage.py
├── requirements.txt
├── dockerfile
├── docker-compose.yml
├── Procfile                     # Heroku process definition
├── runtime.txt                  # Python runtime for Heroku
├── .env                         # Environment variables (not committed)
└── .gitignore
```

---

## 🗃️ Data Models

### `User` (extends `AbstractUser`)
| Field    | Type        | Description                          |
|----------|-------------|--------------------------------------|
| role     | CharField   | `admin`, `doctor`, `patient`, `staff`|

### `AdminProfile`
| Field       | Type      | Description              |
|-------------|-----------|--------------------------|
| user        | OneToOne  | Link to User             |
| admin_code  | CharField | Unique admin identifier  |

### `DoctorProfile`
| Field          | Type      | Description                  |
|----------------|-----------|------------------------------|
| user           | OneToOne  | Link to User                 |
| license_no     | CharField | Unique medical license number|
| specialization | CharField | Doctor's area of expertise   |
| hospital_name  | CharField | Affiliated hospital          |

### `PatientProfile`
| Field           | Type      | Description                     |
|-----------------|-----------|---------------------------------|
| user            | OneToOne  | Link to User                    |
| insurance_no    | CharField | Unique insurance number         |
| medical_history | TextField | Patient medical history         |

> **Custom Permissions:** `view_all_patients`, `edit_patient_records`

### `StaffProfile`
| Field       | Type       | Description                      |
|-------------|------------|----------------------------------|
| user        | OneToOne   | Link to User                     |
| doctor      | ForeignKey | Assigned doctor (supervisor)     |
| employee_id | CharField  | Unique employee identifier       |
| department  | CharField  | Staff department                 |

### `Appointment`
| Field               | Type        | Description                   |
|---------------------|-------------|-------------------------------|
| patient             | ForeignKey  | Patient booking the slot      |
| doctor              | ForeignKey  | Doctor for the appointment    |
| appointment_time    | DateTimeField | Scheduled date & time       |
| appointment_status  | CharField   | Current status                |
| remarks             | CharField   | Optional notes                |
| appointment_number  | CharField   | Auto-generated UUID-based ID  |

> **Custom Permissions:** `view_all_appointments`, `create_appointment`, `update_appointment`, `cancel_appointment`

---

## 🛡️ Custom Permissions

Defined in `app1/permissions.py`:

| Permission Class | Who Has Access                     |
|------------------|------------------------------------|
| `IsAdmin`        | Users with `role == 'admin'`       |
| `IsDoctor`       | Users with `role == 'doctor'` or `'staff'` |
| `IsPatient`      | Users with `role == 'patient'`     |

---

## 🌐 API Endpoints

Base URL: `http://localhost:8000/api/`

### Auth Endpoints
| Method | Endpoint              | Description               | Auth Required |
|--------|-----------------------|---------------------------|---------------|
| POST   | `api/auth/register/`  | Register a new user       | No            |
| POST   | `api/auth/login/`     | Login and get token       | No            |

### Doctor Endpoints
| Method | Endpoint                             | Description                        | Auth Required |
|--------|--------------------------------------|------------------------------------|---------------|
| GET    | `api/doctor/`                        | Get current doctor's profile       | Yes (Doctor)  |
| GET    | `api/doctor/get_staff_permissions/`  | View permissions for the staff group | Yes (Doctor) |
| POST   | `api/doctor/create_staff/`           | Create a staff member under doctor | Yes (Doctor)  |

---

## ⚙️ Setup & Installation

### Local Setup

**1. Clone the repository**
```bash
git clone <your-repo-url>
cd project1
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Create a `.env` file** (see [Environment Variables](#environment-variables))

**5. Run migrations**
```bash
python manage.py migrate
```

**6. Create a superuser (optional)**
```bash
python manage.py createsuperuser
```

**7. Start the development server**
```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

---

### Docker Setup

**1. Make sure Docker Desktop is running**

**2. Create your `.env` file** (see [Environment Variables](#environment-variables))

**3. Build and start containers**
```bash
docker-compose up --build
```

**4. Run migrations inside the container**
```bash
docker-compose exec app python manage.py migrate
```

**5. Create a superuser inside the container (optional)**
```bash
docker-compose exec app python manage.py createsuperuser
```

The API will be available at `http://localhost:8000/`.

---

## 🔑 Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True

# Database (PostgreSQL)
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=db
DB_PORT=5432
```

> ⚠️ **Never commit your `.env` file to version control.** It is already listed in `.gitignore`.

---

## 🔐 Authentication

This API uses **Token Authentication**. After login, include the token in all protected requests:

```
Authorization: Token <your-token-here>
```

---

## 📬 Usage Examples

### Register a Doctor
```http
POST /api/auth/register/
Content-Type: application/json

{
    "username": "dr_smith",
    "password": "securepass123",
    "email": "dr.smith@hospital.com",
    "role": "doctor",
    "license_no": "LIC-00123",
    "specialization": "Cardiology",
    "hospital_name": "City General Hospital"
}
```

### Register a Patient
```http
POST /api/auth/register/
Content-Type: application/json

{
    "username": "john_patient",
    "password": "securepass123",
    "email": "john@example.com",
    "role": "patient",
    "insurance_no": "INS-98765",
    "medical_history": "No known allergies"
}
```

### Login
```http
POST /api/auth/login/
Content-Type: application/json

{
    "username": "dr_smith",
    "password": "securepass123"
}
```
**Response:**
```json
{
    "id": 1,
    "username": "dr_smith",
    "email": "dr.smith@hospital.com",
    "role": "doctor",
    "token": "abc123yourtokenhere"
}
```

### Create Staff (Doctor only)
```http
POST /api/doctor/create_staff/
Authorization: Token abc123yourtokenhere
Content-Type: application/json

{
    "username": "jane_staff",
    "password": "securepass123",
    "email": "jane@hospital.com",
    "employee_id": "EMP-001",
    "department": "Cardiology",
    "permissions": [1, 2]
}
```

---

## 👨‍💻 Admin Panel

Access the Django admin interface at `/admin/` with your superuser credentials to manage users, profiles, groups, and permissions directly.

---

## 📄 License

This project is for educational purposes, demonstrating role-based access control patterns in Django REST Framework.
