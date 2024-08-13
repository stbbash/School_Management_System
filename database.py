import sqlite3
from tkinter import messagebox
from pathlib import Path
import os

# # Get the path to the AppData folder
# appdata_path = Path(os.getenv('LOCALAPPDATA'))
# # Specify the database file path
# db_path = appdata_path / "my_database.db"
# print(f"Database path: {db_path}")

db_path = "my_database.db"


def table_exists(table_name):
    try:  # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Query to check if the table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        result = cursor.fetchone()
        conn.close()
        return True if result else False
    except sqlite3.Error as e:
        return False


def connect_database():
    try:
        # Create a connection to the SQLite database (or connect to an existing one)
        conn = sqlite3.connect(db_path)

        # Create a cursor object to execute SQL commands
        cursor = conn.cursor()
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error creating Connection to database: {e}")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS app_school (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            picture BLOB,
            content_type VARCHAR(256),
            name VARCHAR(255),
            contact_address VARCHAR(255),
            town VARCHAR(255),
            ward VARCHAR(255),
            lga VARCHAR(255),
            email VARCHAR(255),
            phone VARCHAR(20),
            year_established INTEGER,
            settlement VARCHAR(10),
            education VARCHAR(20),
            category VARCHAR(20),
            gender VARCHAR(10),
            operate_shift_system VARCHAR(5),
            share_facility VARCHAR(5),
            have_boarding_facility VARCHAR(5),
            have_perimeter_fencing VARCHAR(5),
            have_security_person VARCHAR(5),
            type_of_security VARCHAR(100),
            no_of_security INTEGER DEFAULT 0,
            prepare_school_improvement_plan VARCHAR(5),
            have_pta VARCHAR(5),
            have_playground VARCHAR(5),
            have_sport_facility VARCHAR(5),
            status VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            owner_id INTEGER
        )
        ''')

    conn.commit()
    conn.close()


def search(option, value):
    try:
        allowed_columns = [
            'name', 'contact_address', 'town', 'ward', 'email', 'phone',
            'year_established', 'no_of_security', 'content_type', 'lga',
            'settlement', 'education', 'category', 'gender', 'operate_shift_system',
            'share_facility', 'have_boarding_facility', 'have_perimeter_fencing',
            'have_security_person', 'type_of_security', 'prepare_school_improvement_plan',
            'have_pta', 'have_playground', 'have_sport_facility', 'status'
        ]
        if option not in allowed_columns:
            messagebox.showerror("Error", "Invalid search option")
            return None
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        query = f'''
            SELECT *
            FROM app_school
            WHERE {option} LIKE ?
        '''
        cursor.execute(query, (f'%{value}%',))
        result = cursor.fetchall()
        conn.close()
        return result
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error accessing the database: {e}")
        return None


def create_user(name, password, owner_id):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username VARCHAR(100),
                password VARCHAR(100),
                owner_id INTEGER
            )
            ''')
        cursor.execute('''
            INSERT INTO users (
                username,
                password,
                owner_id
            ) VALUES (?, ?, ?);
        ''', (name, password, owner_id))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error creating Connection to database: {e}")


def check_user(name, password):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT username, password
            FROM users
            WHERE username = ? AND password = ?
        ''', (name, password))
        result = cursor.fetchall()  # Fetch one result
        conn.close()
        if result:
            return result  # Returns a tuple (username, password)
        else:
            return
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error accessing the database: {e}")
        return None


def insert(data):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
                INSERT INTO app_school (
                    name,
                    picture,
                    content_type,
                    contact_address,
                    town,
                    ward,
                    email,
                    phone,
                    year_established,
                    no_of_security,
                    lga,
                    settlement,
                    education,
                    category,
                    gender,
                    operate_shift_system,
                    share_facility,
                    have_boarding_facility,
                    have_perimeter_fencing,
                    have_security_person,
                    type_of_security,
                    prepare_school_improvement_plan,
                    have_pta,
                    have_playground,
                    have_sport_facility,
                    status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', data)
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "School inserted successfully!")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error inserting data into the database: {e}")


def fetch_school():
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT *
            FROM app_school
            ''')
        result = cursor.fetchall()
        conn.close()
        return result
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error accessing the database: {e}")
        return None


def update(data, record_id):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
                        UPDATE app_school SET
                            name = ?,
                            picture = ?,
                            content_type = ?,
                            contact_address = ?,
                            town = ?,
                            ward = ?,
                            email = ?,
                            phone = ?,
                            year_established = ?,
                            no_of_security = ?,
                            lga = ?,
                            settlement = ?,
                            education = ?,
                            category = ?,
                            gender = ?,
                            operate_shift_system = ?,
                            share_facility = ?,
                            have_boarding_facility = ?,
                            have_perimeter_fencing = ?,
                            have_security_person = ?,
                            type_of_security = ?,
                            prepare_school_improvement_plan = ?,
                            have_pta = ?,
                            have_playground = ?,
                            have_sport_facility = ?,
                            status = ?
                        WHERE id = ?
                    ''', (*data, record_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "School updated successfully!")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error accessing the database: {e}")
        return None


def delete(id):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Correct the SQL syntax for deletion
        cursor.execute('''
            DELETE FROM app_school
            WHERE id = ?
        ''', (id,))

        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "School deleted successfully!")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error accessing the database: {e}")
        return None


def delete_all_records():
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM app_school")
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "All records deleted successfully!")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error accessing the database: {e}")
        return None
