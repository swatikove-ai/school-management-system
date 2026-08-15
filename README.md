<div align="center">

🏫 School Management System

A Modern Python Desktop Application for Complete School Administration

<p>
  <img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Tkinter-GUI-orange?style=for-the-badge" alt="Tkinter">
  <img src="https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/ReportLab-PDF-red?style=for-the-badge" alt="ReportLab">
</p>

<p>
  <strong>Students • Fees • Attendance • Marks • Users • Reports • Report Cards</strong>
</p>

<p>
  <a href="https://github.com/swatikove-ai/school-management-system">Repository</a> •
  <a href="https://github.com/swatikove-ai/school-management-system/issues">Issues</a>
</p>

</div>

📌 About The Project

School Management System is a Python-based desktop application developed to simplify day-to-day school administration.

The system brings essential academic and administrative operations into one centralized application with a Tkinter GUI and SQLite database.

It is designed as a practical CRUD-based software project demonstrating database integration, authentication, calculations, reporting, file export, and modular Python development.

✨ Key Features

Module

Capabilities

🔐 Authentication

Login, user management, logout and password change

👨‍🎓 Students

Add, search, update and delete student records

💰 Fees

Total fees, paid fees, pending fees and fee records

📅 Attendance

Attendance entry, records and percentage calculation

📝 Marks

Subject marks, total, percentage and grade calculation

📊 Dashboard

Quick statistics and management overview

📄 Reports

Student, fees, attendance, marks and complete reports

🎓 Report Card

Student-wise marks, fees and attendance summary

📤 Export

CSV and PDF report generation

🖨️ Print

Printable report output

🖥️ Application Modules

🔐 1. Login & User Management

Secure entry point for the application with user-management functionality.

Includes:

Login

User management

Logout

Change password

Role-based application access

👨‍🎓 2. Student Management

Central module for maintaining student information.

Student details include:

Roll Number
Student Name
Age
Gender
Class
Phone
Email

Operations:

CREATE → READ → UPDATE → DELETE

💰 3. Fees Management

Tracks student fee information and automatically calculates pending fees.

Total Fees
     │
     ├── Paid Fees
     │
     └── Pending Fees

Example:

Total Fees     ₹5,000
Paid Fees      ₹3,000
Pending Fees   ₹2,000

📅 4. Attendance Management

Maintains attendance records and calculates attendance percentage.

Attendance % = Present Days / Total Days × 100

📝 5. Marks Management

Subject-wise academic performance tracking.

Subjects:

English

Hindi

Maths

Science

Computer

The system calculates:

Total Marks
      ↓
Percentage
      ↓
Grade

📊 6. Dashboard

The dashboard provides a quick overview of important school statistics.

Possible KPIs include:

┌─────────────────┐
│ Total Students  │
└─────────────────┘

┌─────────────────┐
│ Total Fees      │
└─────────────────┘

┌─────────────────┐
│ Paid Fees       │
└─────────────────┘

┌─────────────────┐
│ Pending Fees    │
└─────────────────┘

┌─────────────────┐
│ Attendance %    │
└─────────────────┘

📄 Report Management

The reporting module provides multiple views of school data.

Available Reports

👨‍🎓 Student Report

💰 Fees Report

📅 Attendance Report

📝 Marks Report

📊 Complete Student Report

🎓 Student Report Card

Export Options

Application
    │
    ├── CSV Export
    ├── PDF Export
    └── Print

🎓 Student Report Card

The report card combines information from multiple modules into one student-wise summary.

             STUDENT REPORT CARD
                     │
        ┌────────────┼────────────┐
        ↓            ↓            ↓
     Student        Marks        Fees
   Information   Performance    Details
        │            │            │
        └────────────┼────────────┘
                     ↓
                Attendance
                     │
                     ↓
             Final Report Card

Report Card Includes

Roll Number

Student Name

Age

Gender

Class

Subject-wise Marks

Total Marks

Percentage

Grade

Total Fees

Paid Fees

Pending Fees

Attendance Percentage

🏗️ System Architecture

                 ┌─────────────────────┐
                 │       User          │
                 └──────────┬──────────┘
                            ↓
                 ┌─────────────────────┐
                 │    Tkinter GUI      │
                 └──────────┬──────────┘
                            ↓
                 ┌─────────────────────┐
                 │   Python Modules    │
                 └──────────┬──────────┘
                            ↓
        ┌───────────────────┼───────────────────┐
        ↓                   ↓                   ↓
   Students            Fees              Attendance
        │                   │                   │
        └───────────────────┼───────────────────┘
                            ↓
                         Marks
                            │
                            ↓
                       Reports
                            │
                            ↓
                 ┌─────────────────────┐
                 │   SQLite Database   │
                 └─────────────────────┘

🔄 Complete Application Flow

                    START
                      │
                      ▼
                  LOGIN PAGE
                      │
                      ▼
                  DASHBOARD
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
    STUDENTS        FEES       ATTENDANCE
        │             │             │
        └─────────────┼─────────────┘
                      ▼
                    MARKS
                      │
                      ▼
                  REPORTS
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
        CSV          PDF         PRINT
                      │
                      ▼
               REPORT CARD
                      │
                      ▼
                    END

🛠️ Technology Stack

Frontend / GUI

Tkinter

Used to build the desktop user interface, forms, tables, buttons, dashboards and report windows.

Backend

Python

Used for application logic, validation, calculations, database operations and report processing.

Database

SQLite

Used for local data persistence.

Reporting

ReportLab

Used for PDF report generation.

Data Export

CSV

Used for exporting tabular reports.

Version Control

Git + GitHub

Used for source-code management and project collaboration/portfolio hosting.

📁 Project Structure

school-management-system/
│
├── 📄 main.py
├── 📄 database.py
├── 📄 login.py
├── 📄 students.py
├── 📄 fees.py
├── 📄 attendance.py
├── 📄 marks.py
├── 📄 users.py
├── 📄 reports.py
├── 📄 fix_marks_database.py
│
├── 📄 README.md
├── 📄 requirements.txt
└── 📄 .gitignore

The local SQLite database is intentionally excluded from the public repository.

⚙️ Installation & Setup

1️⃣ Clone the repository

git clone https://github.com/swatikove-ai/school-management-system.git

2️⃣ Open the project

cd school-management-system

3️⃣ Install dependencies

python -m pip install -r requirements.txt

Or install ReportLab directly:

python -m pip install reportlab

4️⃣ Run the application

python main.py

🗄️ Database Design

The application uses SQLite for local storage.

The database layer is handled through:

database.py

The application modules communicate with the database to perform CRUD and reporting operations.

GUI
 ↓
Python Module
 ↓
Database Layer
 ↓
SQLite

🔒 Data Privacy

⚠️ Important: Real student records, passwords, phone numbers, emails and other private information should never be committed to a public repository.

The following files are excluded using .gitignore:

school.db
*.db
*.sqlite
*.sqlite3
.env
__pycache__/

📈 Power BI / Analytics Extension

The project can also be extended with a Power BI analytics layer.

SQLite
   ↓
Data Preparation
   ↓
Power BI
   ↓
Interactive Dashboard
   ├── Student Overview
   ├── Fees Analysis
   ├── Attendance Analysis
   └── Marks & Performance

🚀 Future Improvements

The project can be extended into a full web-based school management platform.

Planned Enhancements

🌐 Flask / FastAPI web version

🗄️ MySQL / PostgreSQL database

☁️ Cloud deployment

👨‍👩‍👧 Student & Parent Portal

💳 Online Fee Payment

📩 SMS / Email Notifications

📊 Advanced Analytics

📱 Mobile Application

🔌 REST API

📈 Power BI Integration

🔐 Improved authentication and authorization

🎯 Skills Demonstrated

This project demonstrates practical experience in:

Python
Tkinter
SQLite
SQL
CRUD Operations
Authentication
Database Integration
Form Validation
Data Processing
Report Generation
PDF Generation
CSV Export
Error Handling
Git
GitHub

🧪 Testing Areas

The application can be tested across:

Student CRUD operations

Fee calculations

Pending fee calculation

Attendance percentage

Subject-wise marks

Total and percentage calculation

Grade calculation

Report generation

Student report card

CSV export

PDF export

Login and user management

💡 What I Learned

Through this project, I practiced how to:

Design a modular Python application

Connect Python applications with SQLite

Perform CRUD operations using SQL

Build GUI forms using Tkinter

Validate and process user input

Calculate fees, attendance and academic results

Generate PDF and CSV reports

Structure a multi-file software project

Use Git for version control

Publish a project on GitHub

Prepare a project for portfolio presentation

👨‍💻 Author

Swati Kove

📌 GitHub:
https://github.com/swatikove-ai

<div align="center">

⭐ If you find this project useful, please consider giving it a star!

Built with Python ❤️

</div>
