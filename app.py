import os
import psycopg2
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

CONNECTION_STRING_DB = os.getenv("CONNECTION_STRING_DB")

app = Flask(__name__)

conn = psycopg2.connect(CONNECTION_STRING_DB)


@app.route('/employees', methods=['POST'])
def create_employee():
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
    skill = data.get('skill')

    cur.execute("INSERT INTO employees (employee_id, name, organization, skill) VALUES (%s, %s, %s, %s)",
                (new_id, name, organization, skill))
    conn.commit()
    cur.close()

    return jsonify({
        'employeeId': new_id,
        'name': name,
        'organization': organization,
        'skill': skill
    })


@app.route('/employees', methods=['GET'])
def get_employees():
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees")
    rows = cur.fetchall()
    employees = []
    for row in rows:
        employee = {
            'employeeId': row[0],
            'name': row[1],
            'organization': row[2],
            'skill': row[3]
        }
        employees.append(employee)
    cur.close()
    return jsonify(employees)


@app.route('/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees WHERE employee_id = %s", (employee_id,))
    employee = cur.fetchone()
    cur.close()

    if employee:
        return jsonify({
            'employeeId': employee[0],
            'name': employee[1],
            'organization': employee[2],
            'skill': employee[3]
        })

    return jsonify({'error': 'Employee not found'}), 404


@app.route('/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    cur = conn.cursor()

    data = request.get_json()
    name = data.get('name')
    organization = data.get('organization')
    skill = data.get('skill')

    cur.execute("UPDATE employees SET name = %s, organization = %s, skill = %s WHERE employee_id = %s",
                (name, organization, skill, employee_id))
    updated_rows = cur.rowcount
    conn.commit()
    cur.close()

    if updated_rows > 0:
        return jsonify({'message': 'Employee updated'})

    return jsonify({'error': 'Employee not found'}), 404


@app.route('/employees/<int:employee_id>', methods=['PATCH'])
def patch_employee(employee_id):
    cur = conn.cursor()

    data = request.get_json()
    name = data.get('name')
    organization = data.get('organization')
    skill = data.get('skill')

    update_fields = []
    if name:
        update_fields.append("name = %s")
    if organization:
        update_fields.append("organization = %s")
    if skill:
        update_fields.append("skill = %s")

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
    cur = conn.cursor()
    cur.execute("DELETE FROM employees WHERE employee_id = %s", (employee_id,))
    deleted_rows = cur.rowcount

    if deleted_rows > 0:
        cur.execute("UPDATE employees SET employee_id = employee_id - 1 WHERE employee_id > %s", (employee_id,))
        conn.commit()

        return jsonify({'message': 'Employee deleted'})

    return jsonify({'error': 'Employee not found'}), 404


if __name__ == '__main__':
    app.run()
