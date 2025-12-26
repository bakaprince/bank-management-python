Bank Management System (Python)

A console-based Bank Management System built using Python with MySQL as the backend database.

This project was initially developed as a Class 12 school project and later refactored in college to improve code structure, reliability, and maintainability.


---

Features

User registration and login system

Unique account number generation (collision-free)

Deposit, withdrawal, and balance enquiry

Modular code structure

MySQL database integration



---

Project Evolution

Version 1.0 (School Project)

Single-file implementation

Random account number generation (possible duplication)

User and employee modes

Limited modularity


Version 2.0 (College Refactor)

Modular architecture:

main.py

login_register.py

basic_features.py


Fixed authentication flow

Guaranteed unique account numbers

User-only mode (employee mode removed)

Cleaned and updated dependencies

Improved documentation



---

Project Structure

bank-management-python/
├── main.py
├── login_register.py
├── basic_features.py
├── requirements.txt
└── README.md


---

Requirements

Python 3.x

MySQL Server

Python dependencies listed in requirements.txt


Install dependencies:

pip install -r requirements.txt


---

How to Run

1. Set up the MySQL database according to the project requirements


2. Run the application:



python main.py


---

Notes

This project is intended for academic and learning purposes and demonstrates the progression from a basic monolithic implementation to a more structured and maintainable design.


---