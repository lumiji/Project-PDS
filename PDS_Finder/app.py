from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import json
import os
import sys
from database import init_db

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY') or 'default-secret-key'

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else: 
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, "pds_records.db")

init_db()


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _clean_value(value):
    if value is None:
        return "N/A"  # Default to N/A if missing
    value = value.strip()
    return value if value else "N/A"  # Return N/A if empty string


def _build_address(prefix=""):
    prefix = f"{prefix}_" if prefix else ""
    return {
        "zip_code": _clean_value(request.form.get(f"{prefix}zip_code")),
        "house": _clean_value(request.form.get(f"{prefix}house")),
        "street": _clean_value(request.form.get(f"{prefix}street")),
        "village": _clean_value(request.form.get(f"{prefix}village")),
        "barangay": _clean_value(request.form.get(f"{prefix}barangay")),
        "city": _clean_value(request.form.get(f"{prefix}city")),
        "province": _clean_value(request.form.get(f"{prefix}province")),
    }


def _build_children_list():
    names = request.form.getlist('child_name[]')
    dobs = request.form.getlist('child_dob[]')
    children = []

    for index in range(max(len(names), len(dobs), 0)):
        child_name = _clean_value(names[index]) if index < len(names) else "N/A"
        child_dob = _clean_value(dobs[index]) if index < len(dobs) else "N/A"
        if child_name != "N/A" or child_dob != "N/A":
            children.append({"name": child_name, "date_of_birth": child_dob})

    return json.dumps(children)


def _build_rows(field_map):
    """
    Generic repeating-row builder.
    field_map: dict of {output_key: form_field_name_with_brackets}
    Returns a JSON list of dicts, skipping fully-empty rows.
    """
    lists = {key: request.form.getlist(form_name) for key, form_name in field_map.items()}
    max_len = max((len(v) for v in lists.values()), default=0)

    rows = []
    for i in range(max_len):
        row = {}
        has_value = False
        for key, values in lists.items():
            val = _clean_value(values[i]) if i < len(values) else "N/A"
            if val != "N/A":
                has_value = True
            row[key] = val
        if has_value:
            rows.append(row)

    return json.dumps(rows)


def _build_string_list(field_name):
    """Turn a newline-separated textarea into a JSON list of strings."""
    raw = request.form.get(field_name, "") or ""
    items = [line.strip() for line in raw.splitlines() if line.strip()]
    return json.dumps(items)


def _extract_pds_form_data():
    """Reads the whole PDS form and returns a dict matching the employees table columns."""

    # SECTION 1: PERSONAL INFORMATION
    civil_status = _clean_value(request.form.get('civil_status'))
    civil_status_other = _clean_value(request.form.get('civil_status_other'))
    if civil_status == 'Other' and civil_status_other != "N/A":
        civil_status = f"Other: {civil_status_other}"

    residential_address = _build_address()
    permanent_address = _build_address('perm')

    values = {
        'surname': _clean_value(request.form.get('surname')),
        'first_name': _clean_value(request.form.get('first_name')),
        'name_ext': _clean_value(request.form.get('name_ext')),
        'middle_name': _clean_value(request.form.get('middle_name')),
        'birthdate': _clean_value(request.form.get('birthdate')),
        'birthplace': _clean_value(request.form.get('birthplace')),
        'sex': _clean_value(request.form.get('sex')),
        'civil_status': civil_status,
        'civil_status_other': civil_status_other,
        'height_m': _clean_value(request.form.get('height_m')),
        'weight_kg': _clean_value(request.form.get('weight_kg')),
        'blood_type': _clean_value(request.form.get('blood_type')),
        'umid_id_num': _clean_value(request.form.get('umid_id_num')),
        'pagibig_id_num': _clean_value(request.form.get('pagibig_id_num')),
        'philhealth_num': _clean_value(request.form.get('philhealth_num')),
        'philsys_num': _clean_value(request.form.get('philsys_num')),
        'tin_num': _clean_value(request.form.get('tin_num')),
        'agency_emp_num': _clean_value(request.form.get('agency_emp_num')),
        'citizenship': _clean_value(request.form.get('citizenship')),
        'country': _clean_value(request.form.get('country')),
        'res_address': json.dumps(residential_address),
        'perm_address': json.dumps(permanent_address),
        'zip_code': residential_address.get('zip_code'),
        'telephone_num': _clean_value(request.form.get('telephone_num')),
        'mobile_num': _clean_value(request.form.get('mobile_num')),
        'email_add': _clean_value(request.form.get('email_add')),

        # SECTION 2: FAMILY BACKGROUND
        'spouse_surname': _clean_value(request.form.get('spouse_surname')),
        'spouse_firstname': _clean_value(request.form.get('spouse_first_name')),
        'spouse_extensionname': _clean_value(request.form.get('spouse_extensionname')),
        'spouse_middlename': _clean_value(request.form.get('spouse_middle_name')),
        'spouse_occupation': _clean_value(request.form.get('spouse_occupation')),
        'spouse_employer': _clean_value(request.form.get('spouse_employer')),
        'spouse_business_add': _clean_value(request.form.get('spouse_business_add')),
        'spouse_telephone': _clean_value(request.form.get('spouse_telephone')),
        'children_list': _build_children_list(),
        'father_surname': _clean_value(request.form.get('father_surname')),
        'father_firstname': _clean_value(request.form.get('father_firstname')),
        'father_middlename': _clean_value(request.form.get('father_middlename')),
        'father_extensionname': _clean_value(request.form.get('father_extensionname')),
        'mother_maidenname': _clean_value(request.form.get('mother_maidenname')),
        'mother_surname': _clean_value(request.form.get('mother_surname')),
        'mother_firstname': _clean_value(request.form.get('mother_firstname')),
        'mother_middlename': _clean_value(request.form.get('mother_middlename')),

        # SECTION 3: EDUCATIONAL BACKGROUND (flat fields, one row per level)
        'elem_school': _clean_value(request.form.get('elem_school')),
        'elem_degree': _clean_value(request.form.get('elem_degree')),
        'elem_from': _clean_value(request.form.get('elem_from')),
        'elem_to': _clean_value(request.form.get('elem_to')),
        'elem_units': _clean_value(request.form.get('elem_units')),
        'elem_grad': _clean_value(request.form.get('elem_grad')),
        'elem_honors': _clean_value(request.form.get('elem_honors')),

        'sec_school': _clean_value(request.form.get('sec_school')),
        'sec_degree': _clean_value(request.form.get('sec_degree')),
        'sec_from': _clean_value(request.form.get('sec_from')),
        'sec_to': _clean_value(request.form.get('sec_to')),
        'sec_units': _clean_value(request.form.get('sec_units')),
        'sec_grad': _clean_value(request.form.get('sec_grad')),
        'sec_honors': _clean_value(request.form.get('sec_honors')),

        'voc_school': _clean_value(request.form.get('voc_school')),
        'voc_degree': _clean_value(request.form.get('voc_degree')),
        'voc_from': _clean_value(request.form.get('voc_from')),
        'voc_to': _clean_value(request.form.get('voc_to')),
        'voc_units': _clean_value(request.form.get('voc_units')),
        'voc_grad': _clean_value(request.form.get('voc_grad')),
        'voc_honors': _clean_value(request.form.get('voc_honors')),

        'college_school': _clean_value(request.form.get('college_school')),
        'college_degree': _clean_value(request.form.get('college_degree')),
        'college_from': _clean_value(request.form.get('college_from')),
        'college_to': _clean_value(request.form.get('college_to')),
        'college_units': _clean_value(request.form.get('college_units')),
        'college_grad': _clean_value(request.form.get('college_grad')),
        'college_honors': _clean_value(request.form.get('college_honors')),

        'grad_school': _clean_value(request.form.get('grad_school')),
        'grad_degree': _clean_value(request.form.get('grad_degree')),
        'grad_from': _clean_value(request.form.get('grad_from')),
        'grad_to': _clean_value(request.form.get('grad_to')),
        'grad_units': _clean_value(request.form.get('grad_units')),
        'grad_grad': _clean_value(request.form.get('grad_grad')),
        'grad_honors': _clean_value(request.form.get('grad_honors')),

        # SECTION 4: CIVIL SERVICE ELIGIBILITY
        'civil_service_eligibility': _build_rows({
            'career_service': 'cs_career[]',
            'rating': 'cs_rating[]',
            'date_of_examination': 'cs_date[]',
            'place_of_examination': 'cs_place[]',
            'license_number': 'cs_lic_num[]',
            'date_of_validity': 'cs_validity[]',
        }),

        # SECTION 5: WORK EXPERIENCE
        'work_experience': _build_rows({
            'from_date': 'we_from[]',
            'to_date': 'we_to[]',
            'position_title': 'we_position[]',
            'department_agency': 'we_department[]',
            'status_of_appointment': 'we_status[]',
            'govt_service': 'we_govt_service[]',
        }),

        # SECTION 6: VOLUNTARY WORK
        'voluntary_work': _build_rows({
            'organization': 'vw_org[]',
            'from_date': 'vw_from[]',
            'to_date': 'vw_to[]',
            'hours': 'vw_hours[]',
            'position_nature': 'vw_position[]',
        }),

        # SECTION 7: LEARNING AND DEVELOPMENT
        'learning_and_development': _build_rows({
            'title': 'ld_title[]',
            'from_date': 'ld_from[]',
            'to_date': 'ld_to[]',
            'hours': 'ld_hours[]',
            'type': 'ld_type[]',
            'conducted_by': 'ld_conducted_by[]',
        }),

        # SECTION 8: OTHER INFORMATION
        'skills_and_hobbies': _build_string_list('skills_and_hobbies'),
        'non_academic_distinctions': _build_string_list('non_academic_distinctions'),
        'membership_in_assoc_org': _build_string_list('membership_in_assoc_org'),

        # BACKGROUND QUESTIONS (34-40)
        'rel_3rd_degree': _clean_value(request.form.get('rel_3rd_degree')),
        'rel_3rd_degree_details': _clean_value(request.form.get('rel_3rd_degree_details')),
        'rel_4th_degree': _clean_value(request.form.get('rel_4th_degree')),
        'rel_4th_degree_details': _clean_value(request.form.get('rel_4th_degree_details')),
        'admin_offense_guilty': _clean_value(request.form.get('admin_offense_guilty')),
        'admin_offense_details': _clean_value(request.form.get('admin_offense_details')),
        'criminally_charged': _clean_value(request.form.get('criminally_charged')),
        'criminal_charge_details': _clean_value(request.form.get('criminal_charge_details')),
        'criminal_date_filed': _clean_value(request.form.get('criminal_date_filed')),
        'criminal_case_status': _clean_value(request.form.get('criminal_case_status')),
        'convicted_crime': _clean_value(request.form.get('convicted_crime')),
        'convicted_crime_details': _clean_value(request.form.get('convicted_crime_details')),
        'separated_from_service': _clean_value(request.form.get('separated_from_service')),
        'separation_details': _clean_value(request.form.get('separation_details')),
        'candidate_election': _clean_value(request.form.get('candidate_election')),
        'candidate_election_details': _clean_value(request.form.get('candidate_election_details')),
        'resigned_to_campaign': _clean_value(request.form.get('resigned_to_campaign')),
        'resigned_campaign_details': _clean_value(request.form.get('resigned_campaign_details')),
        'immigrant_status': _clean_value(request.form.get('immigrant_status')),
        'immigrant_country': _clean_value(request.form.get('immigrant_country')),
        'indigenous_member': _clean_value(request.form.get('indigenous_member')),
        'indigenous_details': _clean_value(request.form.get('indigenous_details')),
        'disability': _clean_value(request.form.get('disability')),
        'disability_id_no': _clean_value(request.form.get('disability_id_no')),
        'solo_parent': _clean_value(request.form.get('solo_parent')),
        'solo_parent_id_no': _clean_value(request.form.get('solo_parent_id_no')),

        # SECTION 41: REFERENCES
        'references_list': _build_rows({
            'name': 'ref_name[]',
            'address': 'ref_address[]',
            'contact': 'ref_contact[]',
        }),

        # SECTION 42: CERTIFICATION / GOV'T ISSUED ID
        'gov_id_type': _clean_value(request.form.get('gov_id_type')),
        'gov_id_number': _clean_value(request.form.get('gov_id_number')),
        'gov_id_date_place_issuance': _clean_value(request.form.get('gov_id_date_place_issuance')),
        'date_accomplished': _clean_value(request.form.get('date_accomplished')),
    }

    return values


# Whitelisted sort columns: maps the public "sort_by" value to a safe SQL expression.
# COLLATE NOCASE gives a proper case-insensitive alphabetical sort for text columns.
SORTABLE_COLUMNS = {
    'name': ['surname COLLATE NOCASE', 'first_name COLLATE NOCASE'],
    'department': ['department COLLATE NOCASE'],
    'date_created': ['date_created'],
}



def _build_employee_query(search_query, department, sort_by, sort_dir):
    where_clauses = []
    params = []

    if search_query:
        # Broaden the search beyond just 3 fields, and make it robust to leading/
        # trailing whitespace so a stray space doesn't hide otherwise-matching rows.
        term = f"%{search_query.strip()}%"
        where_clauses.append('''(
            surname LIKE ? COLLATE NOCASE OR
            first_name LIKE ? COLLATE NOCASE OR
            middle_name LIKE ? COLLATE NOCASE OR
            agency_emp_num LIKE ? COLLATE NOCASE OR
            email_add LIKE ? COLLATE NOCASE OR
            mobile_num LIKE ? COLLATE NOCASE OR
            department LIKE ? COLLATE NOCASE OR
            (surname || ' ' || first_name) LIKE ? COLLATE NOCASE OR
            (first_name || ' ' || surname) LIKE ? COLLATE NOCASE
        )''')
        params.extend([term] * 9)

    if department and department != 'All':
        where_clauses.append('department = ?')
        params.append(department)

    sql = 'SELECT * FROM employees'
    if where_clauses:
        sql += ' WHERE ' + ' AND '.join(where_clauses)

    columns = SORTABLE_COLUMNS.get(sort_by, SORTABLE_COLUMNS['date_created'])
    direction = 'ASC' if sort_dir == 'asc' else 'DESC'
    order_expr = ', '.join(f'{col} {direction}' for col in columns)
    sql += f' ORDER BY {order_expr}'


    return sql, params


@app.route('/dashboard')
def dashboard():
    search_query = request.args.get('search_query', '').strip()
    department = request.args.get('department', 'All')
    sort_by = request.args.get('sort_by', 'date_created')
    sort_dir = request.args.get('sort_dir', 'desc')

    sql, params = _build_employee_query(search_query, department, sort_by, sort_dir)

    conn = get_db_connection()
    employees = conn.execute(sql, params).fetchall()
    departments = conn.execute('SELECT name FROM departments ORDER BY name ASC').fetchall()
    conn.close()

    return render_template(
        'index.html',
        employees=employees,
        departments=departments,
        search_query=search_query,
        selected_department=department,
        sort_by=sort_by,
        sort_dir=sort_dir,
    )



@app.route('/assign_department/<int:id>', methods=['POST'])
def assign_department(id):
    selected = request.form.get('department')
    new_dept = request.form.get('new_department')

    final_dept = new_dept if selected == '__NEW__' and new_dept else selected

    conn = get_db_connection()
    conn.execute('UPDATE employees SET department = ? WHERE id = ?', (final_dept, id))

    if final_dept != 'N/A':
        conn.execute('INSERT OR IGNORE INTO departments (name) VALUES (?)', (final_dept,))

    conn.commit()
    conn.close()
    flash(f"Department updated to {final_dept}!", "success")
    return redirect(url_for('dashboard'))


@app.route('/manage_department/add', methods=['POST'])
def add_department():
    new_dept = request.form.get('new_department').strip()
    if new_dept:
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO departments (name) VALUES (?)', (new_dept,))
            conn.commit()
            flash(f"Department '{new_dept}' added!", "success")
        except sqlite3.IntegrityError:
            flash("That department already exists.", "danger")
        finally:
            conn.close()
    return redirect(url_for('dashboard'))


@app.route('/manage_department/edit', methods=['POST'])
def edit_department():
    old_name = request.form.get('old_name')
    new_name = request.form.get('new_name').strip()

    conn = get_db_connection()
    try:
        conn.execute('UPDATE departments SET name = ? WHERE name = ?', (new_name, old_name))
        conn.execute('UPDATE employees SET department = ? WHERE department = ?', (new_name, old_name))
        conn.commit()
        flash(f"Department renamed to '{new_name}'!", "success")
    except sqlite3.IntegrityError:
        flash("A department with that name already exists.", "danger")
    finally:
        conn.close()
    return redirect(url_for('dashboard'))


@app.route('/manage_department/delete', methods=['POST'])
def delete_department():
    dept_name = request.form.get('dept_name')
    conn = get_db_connection()

    conn.execute('DELETE FROM departments WHERE name = ?', (dept_name,))
    conn.execute('UPDATE employees SET department = "N/A" WHERE department = ?', (dept_name,))
    conn.commit()
    conn.close()

    flash(f"Department '{dept_name}' deleted.", "success")
    return redirect(url_for('dashboard'))


@app.route('/search', methods=['GET'])
def search():
    # Kept for backward compatibility (old bookmarks/links); delegates to the
    # same filter/sort-aware logic as /dashboard.
    return redirect(url_for('dashboard', **request.args))



@app.route('/', methods=['GET'])
def pds_form():
    return render_template('form.html', employee=None, mode='edit')


@app.route('/view_pds/<int:id>')
def view_pds(id):
    conn = get_db_connection()
    employee = conn.execute('SELECT * FROM employees WHERE id = ?', (id,)).fetchone()
    conn.close()
    return render_template('form.html', employee=employee, mode='view')


@app.route('/edit_pds/<int:id>', methods=['GET', 'POST'])
def edit_pds(id):

    if request.method == 'GET':
        conn = get_db_connection()
        employee = conn.execute('SELECT * FROM employees WHERE id = ?', (id,)).fetchone()
        conn.close()

        return render_template('form.html', employee=employee, mode='edit')

    elif request.method == 'POST':
        values = _extract_pds_form_data()

        set_clause = ', '.join([f"{col} = ?" for col in values.keys()])
        query = f"UPDATE employees SET {set_clause} WHERE id = ?"

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(query, list(values.values()) + [id])
            conn.commit()
            flash("PDS Record Successfully UPDATED!", "success")
        except Exception as exc:
            conn.rollback()
            flash(f"Database Error: {str(exc)}", "danger")
        finally:
            conn.close()

        return redirect(url_for('dashboard'))


@app.route('/delete_pds/<int:id>')
def delete_pds(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM employees WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash("PDS Record Successfully Deleted!", "success")
    return redirect(url_for('dashboard'))


@app.route('/submit_pds', methods=['POST'])
def submit_pds():
    values = _extract_pds_form_data()

    columns = list(values.keys())
    placeholders = ', '.join(['?'] * len(columns))
    query = f"INSERT INTO employees ({', '.join(columns)}) VALUES ({placeholders})"

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query, list(values.values()))
        conn.commit()
        flash("PDS Record Successfully Saved!", "success")
    except Exception as exc:
        conn.rollback()
        flash(f"Database Error: {str(exc)}", "danger")
    finally:
        conn.close()

    return redirect(url_for('dashboard'))


@app.template_filter('from_json')
def from_json(value):
    try:
        return json.loads(value) if value else []
    except Exception:
        return []


if __name__ == '__main__':
    import sys
    if getattr(sys, 'frozen', False):
        # Use Waitress for the production executable
        from waitress import serve
        print("===================================================")
        print("PDS Dashboard is Running!")
        print("Leave this window open and go to: http://localhost:5000")
        print("===================================================")
        serve(app, host='127.0.0.1', port=5000)
    else:
        # Use standard Flask for local testing
        app.run(debug=True, port=5000)