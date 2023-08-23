import os
import psycopg2
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import jwt

load_dotenv()

CONNECTION_STRING_DB = os.getenv("CONNECTION_STRING_DB")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
USERNAME = os.getenv("APP_SUPERUSER")
PASSWORD = os.getenv("APP_PASSWORD")

app = Flask(__name__, static_url_path='', static_folder='static')
app.config['STATICFILES_DIRS'] = [
    os.path.join(app.static_folder, 'files')
]

conn = psycopg2.connect(CONNECTION_STRING_DB)


@app.route('/generate-token', methods=['POST'])
def generate_token():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not authenticate_user(username, password):
        return jsonify({'message': 'Invalid username or password'}), 401
    token = jwt.encode({'username': username}, JWT_SECRET_KEY, algorithm='HS256')
    encoded_token = token
    return jsonify({'token': encoded_token})


@app.route('/get_environment_variables')
def get_environment_variables():
    return jsonify({
        'username': USERNAME,
        'password': PASSWORD,
        'jwt_secret_key': JWT_SECRET_KEY
    })


def authenticate_user(username, password):
    return username == USERNAME and password == PASSWORD


def validate_token(token):
    try:
        jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        return True
    except jwt.exceptions.DecodeError:
        return False


@app.route('/employees', methods=['POST'])
def create_employee():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'message': 'Unauthorized'}), 401
    token = auth_header.split(' ')[1]
    if not validate_token(token):
        return jsonify({'message': 'Invalid token'}), 401
    cur = conn.cursor()
    cur.execute("SELECT MAX(employee_id) FROM employees")
    max_id = cur.fetchone()[0]
    if max_id is None:
        new_id = 1
    else:
        existing_ids = set(range(1, max_id + 1))
        cur.execute("SELECT employee_id FROM employees")
        used_ids = set(row[0] for row in cur.fetchall())
        available_ids = existing_ids - used_ids
        if available_ids:
            new_id = min(available_ids)
        else:
            new_id = max_id + 1
    data = request.get_json()
    name = data.get('name')
    organization = data.get('organization')
    role = data.get('role')
    cur.execute("INSERT INTO employees (employee_id, name, organization, role) VALUES (%s, %s, %s, %s)",
                (new_id, name, organization, role))
    conn.commit()
    cur.close()
    return jsonify({
        'employeeId': new_id,
        'name': name,
        'organization': organization,
        'role': role
    })


@app.route('/employees', methods=['GET'])
def get_employees():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'message': 'Unauthorized'}), 401
    token = auth_header.split(' ')[1]
    if not validate_token(token):
        return jsonify({'message': 'Invalid token'}), 401
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees ORDER BY employee_id")
    rows = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]
    employees = []
    for row in rows:
        employee = {
            'name': None,
            'organization': None,
            'role': None,
            'employeeId': None,
        }
        for col_name, value in zip(column_names, row):
            if col_name == 'name':
                employee['name'] = value
            elif col_name == 'organization':
                employee['organization'] = value
            elif col_name == 'role':
                employee['role'] = value
            elif col_name == 'employee_id':
                employee['employeeId'] = value
        employees.append(employee)
    cur.close()
    return jsonify(employees)


@app.route('/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'message': 'Unauthorized'}), 401
    token = auth_header.split(' ')[1]
    if not validate_token(token):
        return jsonify({'message': 'Invalid token'}), 401
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees WHERE employee_id = %s", (employee_id,))
    employee = cur.fetchone()
    cur.close()
    if employee:
        return jsonify({
            'name': employee[0],
            'organization': employee[1],
            'role': employee[2],
            'employeeId': employee[3],
        })
    return jsonify({'error': 'Employee not found'}), 404


@app.route('/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'message': 'Unauthorized'}), 401
    token = auth_header.split(' ')[1]
    if not validate_token(token):
        return jsonify({'message': 'Invalid token'}), 401
    cur = conn.cursor()
    data = request.get_json()
    name = data.get('name')
    organization = data.get('organization')
    role = data.get('role')
    cur.execute("UPDATE employees SET name = %s, organization = %s, role = %s WHERE employee_id = %s",
                (name, organization, role, employee_id))
    updated_rows = cur.rowcount
    conn.commit()
    cur.close()
    if updated_rows > 0:
        return jsonify({'message': 'Employee updated'})
    return jsonify({'error': 'Employee not found'}), 404


@app.route('/employees/<int:employee_id>', methods=['PATCH'])
def patch_employee(employee_id):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'message': 'Unauthorized'}), 401
    token = auth_header.split(' ')[1]
    if not validate_token(token):
        return jsonify({'message': 'Invalid token'}), 401
    cur = conn.cursor()
    data = request.get_json()
    name = data.get('name')
    organization = data.get('organization')
    role = data.get('role')
    update_fields = []
    if name:
        update_fields.append("name = %s")
    if organization:
        update_fields.append("organization = %s")
    if role:
        update_fields.append("role = %s")
    if not update_fields:
        return jsonify({'message': 'No fields to update'})
    update_query = "UPDATE employees SET " + ", ".join(update_fields) + " WHERE employee_id = %s"
    cur.execute(update_query, [value for value in data.values() if value] + [employee_id])
    updated_rows = cur.rowcount
    conn.commit()
    cur.close()
    if updated_rows > 0:
        return jsonify({'message': 'Employee updated'})
    return jsonify({'error': 'Employee not found'}), 404


@app.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'message': 'Unauthorized'}), 401
    token = auth_header.split(' ')[1]
    if not validate_token(token):
        return jsonify({'message': 'Invalid token'}), 401
    cur = conn.cursor()
    cur.execute("DELETE FROM employees WHERE employee_id = %s", (employee_id,))
    deleted_rows = cur.rowcount
    if deleted_rows > 0:
        cur.execute("UPDATE employees SET employee_id = employee_id - 1 WHERE employee_id > %s", (employee_id,))
        conn.commit()
        return jsonify({'message': 'Employee deleted'})
    return jsonify({'error': 'Employee not found'}), 404


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
