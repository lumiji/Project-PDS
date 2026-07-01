from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import json

app = Flask(__name__)

import os

print("--- DIAGNOSTIC CHECK")
print("--- FOLDERS IN PDS_Finder: ", os.listdir(os.getcwd()))

if os.path.exists('templates'):
    print("Files inside templates:", os.listdir('templates'))
else:
    print("ERROR: Python cannot see a folder named 'templates")

print("-------------------------------")

# DATABASE CONNECTION ---
def get_db_connection():
    conn = sqlite3.connect('pds_records.db')
    conn.row_factory = sqlite3.Row 
    return conn

@app.route('/dashboard')
def dashboard():
    conn = get_db_connection()
    employees = conn.execute('SELECT * FROM employees ORDER BY date_created DESC').fetchall()
    conn.close()
    return render_template('index.html', employees=employees)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('search_query', '')
    conn = get_db_connection()
    search_sql = '''SELECT * FROM employees
                    WHERE surname LIKE ? OR first_name LIKE ? OR agency_emp_num LIKE ?'''
    results = conn.execute(search_sql, (f'%{query}%', f'%{query}%', f'%{query}%')).fetchall()
    conn.close()
    return render_template('index.html', employees=results)

# SERVE THE PDS FORM ---
@app.route('/', methods=['GET'])
def pds_form():
    return render_template('form.html')

# HANDLE FORM SUBMISSION ---
@app.route('/submit_pds', methods=['POST'])
def submit_pds():
    # Capture Standard Text Fields (Section 1 & 2 Example)
    surname = request.form.get('surname')
    first_name = request.form.get('first_name')
    middle_name = request.form.get('middle_name')
    civil_status = request.form.get('civil_status')
    
    # Capture and Bundle JSON Fields (Section 3 Example)
    # We capture multiple inputs sharing the same 'name' attribute from the HTML
    college_schools = request.form.getlist('college_school_name')
    college_degrees = request.form.getlist('college_degree')
    
    # Zip into a list of dictionaries, then convert to a JSON string
    college_data = []
    for i in range(len(college_schools)):
        if college_schools[i]: # Only add if the school name isn't blank
            college_data.append({
                "school_name": college_schools[i],
                "degree": college_degrees[i] if i < len(college_degrees) else ""
            })
    educ_college_json = json.dumps(college_data)

    # Database Insertion
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO employees (
                surname, first_name, middle_name, civil_status, educ_college
            ) VALUES (?, ?, ?, ?, ?)
        ''', (surname, first_name, middle_name, civil_status, educ_college_json))
        
        conn.commit()
        status_message = "PDS Record Successfully Saved!"
    except Exception as e:
        conn.rollback()
        status_message = f"Database Error: {str(e)}"
    finally:
        conn.close()


    return status_message

# EXECUTE THE SERVER ---
if __name__ == '__main__':
    # debug=True automatically restarts the server when you save changes in Sublime
    app.run(debug=True, port=5000)