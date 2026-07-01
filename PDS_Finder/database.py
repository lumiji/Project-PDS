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
            name_ext TEXT, 
            middle_name TEXT,
            birthdate TEXT, 
            birthplace TEXT,
            sex TEXT,
            civil_status TEXT, 
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
            res_address TEXT, 
            telephone_num TEXT, 
            mobile_num TEXT, 
            email_add TEXT, 
            
            -- SECTION 2: FAMILY BACKGROUND
            spouse_surname TEXT, 
            spouse_firstname TEXT, 
            spouse_middlename TEXT, 
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
            
            date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Complete PDS Database initialized successfully!")