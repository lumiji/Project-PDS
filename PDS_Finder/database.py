import sqlite3

def init_db():
    conn = sqlite3.connect('pds_records.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            
            -- SECTION 1: PERSONAL INFORMATION

            surname TEXT NOT NULL,
            first_name TEXT NOT NULL, 
            department TEXT, 
            name_ext TEXT, 
            middle_name TEXT,
            birthdate TEXT, 
            birthplace TEXT,
            sex TEXT,
            civil_status TEXT,
            civil_status_other TEXT,
            height_m REAL, 
            weight_kg REAL, 
            blood_type TEXT, 
            umid_id_num TEXT, 
            pagibig_id_num TEXT,
            philhealth_num TEXT, 
            philsys_num TEXT, 
            tin_num TEXT,
            agency_emp_num TEXT,
            citizenship TEXT, 
            country TEXT,
            res_address TEXT, 
            perm_address TEXT,
            zip_code INT, 
            telephone_num TEXT, 
            mobile_num TEXT, 
            email_add TEXT, 
            
            -- SECTION 2: FAMILY BACKGROUND
            spouse_surname TEXT, 
            spouse_firstname TEXT, 
            spouse_extensionname TEXT, 
            spouse_middlename TEXT, 
            spouse_occupation TEXT,
            spouse_employer TEXT, 
            spouse_business_add TEXT, 
            spouse_telephone TEXT, 
            children_list TEXT, -- JSON
            father_surname TEXT, 
            father_firstname TEXT,
            father_middlename TEXT, 
            father_extensionname TEXT, 
            mother_maidenname TEXT, 
            mother_surname TEXT,
            mother_firstname TEXT, 
            mother_middlename TEXT,  
            
            -- SECTION 3: EDUCATIONAL BACKGROUND
            educ_elementary TEXT, -- JSON
            educ_secondary TEXT, -- JSON
            educ_vocational TEXT, -- JSON
            educ_college TEXT, -- JSON
            educ_graduate TEXT, -- JSON
            
            -- SECTION 4: CIVIL SERVICE ELIGIBILITY
            civil_service_eligibility TEXT, -- JSON
            
            -- SECTION 5: WORK EXPERIENCE
            work_experience TEXT, -- JSON list of dictionaries
            
            -- SECTION 6: VOLUNTARY WORK OR INVOLVEMENT IN CIVIC / NON-GOVERNMENT ORGANIZATION
            voluntary_work TEXT, -- JSON list of dictionaries
            
            -- SECTION 7: LEARNING AND DEVELOPMENT (L&D) INTERVENTIONS/TRAINING PROGRAMS ATTENDED
            learning_and_development TEXT, -- JSON list of dictionaries
            
            -- SECTION 8: OTHER INFORMATION
            skills_and_hobbies TEXT, -- JSON list of strings
            non_academic_distinctions TEXT, -- JSON list of strings
            membership_in_assoc_org TEXT, -- JSON list of strings

            -- SECTION: BACKGROUND QUESTIONS (34-40)
            rel_3rd_degree TEXT,
            rel_3rd_degree_details TEXT,
            rel_4th_degree TEXT,
            rel_4th_degree_details TEXT,
            admin_offense_guilty TEXT,
            admin_offense_details TEXT,
            criminally_charged TEXT,
            criminal_charge_details TEXT,
            criminal_date_filed TEXT,
            criminal_case_status TEXT,
            convicted_crime TEXT,
            convicted_crime_details TEXT,
            separated_from_service TEXT,
            separation_details TEXT,
            candidate_election TEXT,
            candidate_election_details TEXT,
            resigned_to_campaign TEXT,
            resigned_campaign_details TEXT,
            immigrant_status TEXT,
            immigrant_country TEXT,
            indigenous_member TEXT,
            indigenous_details TEXT,
            disability TEXT,
            disability_id_no TEXT,
            solo_parent TEXT,
            solo_parent_id_no TEXT,

            -- SECTION 41: REFERENCES
            references_list TEXT, -- JSON list of dictionaries

            -- SECTION 42: CERTIFICATION / GOV'T ISSUED ID
            gov_id_type TEXT,
            gov_id_number TEXT,
            gov_id_date_place_issuance TEXT,
            date_accomplished TEXT,
            
            date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute("PRAGMA table_info(employees)")
    existing_columns = {row[1] for row in cursor.fetchall()}

    required_columns = [
        ("name_ext", "TEXT"),
        ("middle_name", "TEXT"),
        ("department", "TEXT"),
        ("birthdate", "TEXT"),
        ("birthplace", "TEXT"),
        ("sex", "TEXT"),
        ("civil_status", "TEXT"),
        ("civil_status_other", "TEXT"),
        ("height_m", "REAL"),
        ("weight_kg", "REAL"),
        ("blood_type", "TEXT"),
        ("umid_id_num", "TEXT"),
        ("pagibig_id_num", "TEXT"),
        ("philhealth_num", "TEXT"),
        ("philsys_num", "TEXT"),
        ("tin_num", "TEXT"),
        ("agency_emp_num", "TEXT"),
        ("citizenship", "TEXT"),
        ("country", "TEXT"),
        ("res_address", "TEXT"),
        ("perm_address", "TEXT"),
        ("zip_code", "INT"),
        ("telephone_num", "TEXT"),
        ("mobile_num", "TEXT"),
        ("email_add", "TEXT"),
        ("spouse_surname", "TEXT"),
        ("spouse_firstname", "TEXT"),
        ("spouse_extensionname", "TEXT"),
        ("spouse_middlename", "TEXT"),
        ("spouse_occupation", "TEXT"),
        ("spouse_employer", "TEXT"),
        ("spouse_business_add", "TEXT"),
        ("spouse_telephone", "TEXT"),
        ("children_list", "TEXT"),
        ("father_surname", "TEXT"),
        ("father_firstname", "TEXT"),
        ("father_middlename", "TEXT"),
        ("father_extensionname", "TEXT"),
        ("mother_maidenname", "TEXT"),
        ("mother_surname", "TEXT"),
        ("mother_firstname", "TEXT"),
        ("mother_middlename", "TEXT"),
        ("educ_elementary", "TEXT"),
        ("educ_secondary", "TEXT"),
        ("educ_vocational", "TEXT"),
        ("educ_college", "TEXT"),
        ("educ_graduate", "TEXT"),
        ("civil_service_eligibility", "TEXT"),
        ("work_experience", "TEXT"),
        ("voluntary_work", "TEXT"),
        ("learning_and_development", "TEXT"),
        ("skills_and_hobbies", "TEXT"),
        ("non_academic_distinctions", "TEXT"),
        ("membership_in_assoc_org", "TEXT"),
        ("rel_3rd_degree", "TEXT"),
        ("rel_3rd_degree_details", "TEXT"),
        ("rel_4th_degree", "TEXT"),
        ("rel_4th_degree_details", "TEXT"),
        ("admin_offense_guilty", "TEXT"),
        ("admin_offense_details", "TEXT"),
        ("criminally_charged", "TEXT"),
        ("criminal_charge_details", "TEXT"),
        ("criminal_date_filed", "TEXT"),
        ("criminal_case_status", "TEXT"),
        ("convicted_crime", "TEXT"),
        ("convicted_crime_details", "TEXT"),
        ("separated_from_service", "TEXT"),
        ("separation_details", "TEXT"),
        ("candidate_election", "TEXT"),
        ("candidate_election_details", "TEXT"),
        ("resigned_to_campaign", "TEXT"),
        ("resigned_campaign_details", "TEXT"),
        ("immigrant_status", "TEXT"),
        ("immigrant_country", "TEXT"),
        ("indigenous_member", "TEXT"),
        ("indigenous_details", "TEXT"),
        ("disability", "TEXT"),
        ("disability_id_no", "TEXT"),
        ("solo_parent", "TEXT"),
        ("solo_parent_id_no", "TEXT"),
        ("references_list", "TEXT"),
        ("gov_id_type", "TEXT"),
        ("gov_id_number", "TEXT"),
        ("gov_id_date_place_issuance", "TEXT"),
        ("date_accomplished", "TEXT"),
        # Education sub-fields used directly by form.html inputs
        ("elem_school", "TEXT"), ("elem_degree", "TEXT"), ("elem_from", "TEXT"),
        ("elem_to", "TEXT"), ("elem_units", "TEXT"), ("elem_grad", "TEXT"), ("elem_honors", "TEXT"),
        ("sec_school", "TEXT"), ("sec_degree", "TEXT"), ("sec_from", "TEXT"),
        ("sec_to", "TEXT"), ("sec_units", "TEXT"), ("sec_grad", "TEXT"), ("sec_honors", "TEXT"),
        ("voc_school", "TEXT"), ("voc_degree", "TEXT"), ("voc_from", "TEXT"),
        ("voc_to", "TEXT"), ("voc_units", "TEXT"), ("voc_grad", "TEXT"), ("voc_honors", "TEXT"),
        ("college_school", "TEXT"), ("college_degree", "TEXT"), ("college_from", "TEXT"),
        ("college_to", "TEXT"), ("college_units", "TEXT"), ("college_grad", "TEXT"), ("college_honors", "TEXT"),
        ("grad_school", "TEXT"), ("grad_degree", "TEXT"), ("grad_from", "TEXT"),
        ("grad_to", "TEXT"), ("grad_units", "TEXT"), ("grad_grad", "TEXT"), ("grad_honors", "TEXT"),
    ]

    for column_name, column_type in required_columns:
        if column_name not in existing_columns:
            cursor.execute(f'ALTER TABLE employees ADD COLUMN {column_name} {column_type}')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')

    # Automatically migrate existing departments so you don't lose them
    try:
        cursor.execute('''
            INSERT OR IGNORE INTO departments (name) 
            SELECT DISTINCT department FROM employees 
            WHERE department IS NOT NULL AND department != 'N/A' AND department != ''
        ''')
    except sqlite3.OperationalError:
        pass

        
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Complete PDS Database initialized successfully!")