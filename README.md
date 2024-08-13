# School Management System

This is a School Management System built using Python and the `CustomTkinter` library. The application includes user registration, login, and a main interface for managing school data (CRUD operations). Below is a description of the main files in this project.

## Project Files Overview

### 1. `apsb.py` (Registration Page)
This is the main entry point of the application, which also serves as the registration page. It performs the following tasks:
- Sends a GET request to a backend API to verify the username and active status of the user.
- Allows users to register by creating a password.
- Note: This process requires an internet connection.

### 2. `login.py` (Login Page)
This script is used for user authentication after registration. It does the following:
- Creates an SQLite3 database to store user credentials.
- Allows the user to log in without requiring an internet connection after the initial registration.
- Once logged in, the user can access the main application.

### 3. `school.py` (Main Application)
This is the core of the application where users can perform CRUD (Create, Read, Update, Delete) operations on school data. It provides an interface for managing school information effectively.

### 4. `database.py`
This file contains all the database functions used across the entire application. It manages interactions with the SQLite3 database, ensuring data is correctly stored and retrieved.

### 5. `my_images.py`
Handles the management of image files within the application. It includes functions for creating, saving, and manipulating images used in the user interface.

## Requirements
- Python 3.11+
- CustomTkinter
- SQLite3
- Pillow

You can install the necessary Python packages by running:
```bash
pip install -r requirements.txt
```

## Running the Application

To run the application, execute the `apsb.py` file:
```bash
python apsb.py
```

After registration, you can log in using the `login.py` script:
```bash
python login.py
```

Once logged in, you will be redirected to the main application where you can manage school data.
