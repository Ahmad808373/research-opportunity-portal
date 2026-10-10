"""A small Flask REST API backed entirely by MySQL."""
import os
import re
from datetime import date
from pathlib import Path

import mysql.connector
from flask import Flask, jsonify, request, send_from_directory
from werkzeug.exceptions import HTTPException

from db import close_connection, get_connection

FRONTEND = Path(__file__).resolve().parent.parent / 'frontend'
app = Flask(__name__, static_folder=str(FRONTEND), static_url_path='/static')
app.config['MAX_CONTENT_LENGTH'] = 65536
app.teardown_appcontext(close_connection)

TEXT_LIMITS = {
    'title': 200,
    'description': 10000,
    'research_area': 150,
    'faculty_name': 150,
    'department': 150,
    'required_skills': 10000,
}
FIELDS = list(TEXT_LIMITS) + ['available_positions', 'application_deadline', 'status']
MAX_INT = 2147483647


def json_body():
    if not request.is_json:
        raise ValueError('Send a JSON object with Content-Type: application/json.')
    # Malformed JSON raises BadRequest and is handled as a safe JSON 400 below.
    data = request.get_json()
    if not isinstance(data, dict) or not data:
        raise ValueError('The request must contain a non-empty JSON object.')
    unknown = set(data) - set(FIELDS)
    if unknown:
        raise ValueError('Unknown fields: ' + ', '.join(sorted(unknown)) + '.')
    return data


def validate_opportunity(data):
    cleaned = {}
    for field, limit in TEXT_LIMITS.items():
        value = data.get(field)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(field.replace('_', ' ').capitalize() + ' is required.')
        value = value.strip()
        if len(value) > limit:
            raise ValueError(f'{field} must be at most {limit} characters.')
        cleaned[field] = value
    positions = data.get('available_positions')
    if type(positions) is not int or not 0 <= positions <= MAX_INT:
        raise ValueError(f'Available positions must be an integer from 0 to {MAX_INT}.')
    deadline = data.get('application_deadline')
    if not isinstance(deadline, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', deadline):
        raise ValueError('Application deadline must be a valid date in YYYY-MM-DD format.')
    try:
        parsed_date = date.fromisoformat(deadline)
        if parsed_date.year < 1000:
            raise ValueError()
    except ValueError:
        raise ValueError('Application deadline must be a real date from year 1000 onward.') from None
    if data.get('status') not in ('Open', 'Closed'):
        raise ValueError('Status must be Open or Closed.')
    cleaned.update(available_positions=positions, application_deadline=deadline,
                   status=data['status'])
    return cleaned


def valid_id(raw_id):
    if not re.fullmatch(r'[0-9]{1,10}', raw_id):
        raise ValueError('Opportunity ID must be a positive integer.')
    opportunity_id = int(raw_id)
    if not 1 <= opportunity_id <= MAX_INT:
        raise ValueError('Opportunity ID is out of range.')
    return opportunity_id


def serialize(row):
    row['application_deadline'] = row['application_deadline'].isoformat()
    return row


@app.get('/')
def home():
    return send_from_directory(FRONTEND, 'index.html')


@app.post('/api/opportunities')
def create_opportunity():
    data = validate_opportunity(json_body())
    connection = get_connection()
    with connection.cursor(dictionary=True) as cursor:
        # Column names come only from our constant FIELDS, never from user input.
        columns = ', '.join(FIELDS)
        placeholders = ', '.join(['%s'] * len(FIELDS))
        cursor.execute(f'INSERT INTO opportunities ({columns}) VALUES ({placeholders})',
                       tuple(data[field] for field in FIELDS))
        opportunity_id = cursor.lastrowid
        cursor.execute('SELECT * FROM opportunities WHERE id = %s', (opportunity_id,))
        opportunity = serialize(cursor.fetchone())
    connection.commit()
    return jsonify(message='Opportunity created.', opportunity=opportunity), 201


@app.get('/api/opportunities')
def get_opportunities():
    with get_connection().cursor(dictionary=True) as cursor:
        cursor.execute('SELECT * FROM opportunities ORDER BY id DESC')
        rows = [serialize(row) for row in cursor.fetchall()]
    return jsonify(rows), 200


@app.get('/api/opportunities/<raw_id>')
def get_opportunity(raw_id):
    opportunity_id = valid_id(raw_id)
    with get_connection().cursor(dictionary=True) as cursor:
        cursor.execute('SELECT * FROM opportunities WHERE id = %s', (opportunity_id,))
        row = cursor.fetchone()
    if row is None:
        return jsonify(error='Opportunity not found.'), 404
    return jsonify(serialize(row)), 200


@app.put('/api/opportunities/<raw_id>')
def update_opportunity(raw_id):
    opportunity_id = valid_id(raw_id)
    changes = json_body()
    connection = get_connection()
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute('SELECT * FROM opportunities WHERE id = %s FOR UPDATE',
                       (opportunity_id,))
        row = cursor.fetchone()
        if row is None:
            return jsonify(error='Opportunity not found.'), 404
        existing = serialize(row)
        existing.update(changes)
        data = validate_opportunity(existing)
        assignments = ', '.join(field + ' = %s' for field in FIELDS)
        cursor.execute(f'UPDATE opportunities SET {assignments} WHERE id = %s',
                       tuple(data[field] for field in FIELDS) + (opportunity_id,))
        cursor.execute('SELECT * FROM opportunities WHERE id = %s', (opportunity_id,))
        opportunity = serialize(cursor.fetchone())
    connection.commit()
    return jsonify(message='Opportunity updated.', opportunity=opportunity), 200


@app.delete('/api/opportunities/<raw_id>')
def delete_opportunity(raw_id):
    opportunity_id = valid_id(raw_id)
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute('DELETE FROM opportunities WHERE id = %s', (opportunity_id,))
        deleted = cursor.rowcount
    connection.commit()
    if deleted == 0:
        return jsonify(error='Opportunity not found.'), 404
    return jsonify(message='Opportunity deleted.', id=opportunity_id), 200


@app.errorhandler(ValueError)
def invalid_data(error):
    return jsonify(error=str(error)), 400


@app.errorhandler(HTTPException)
def http_error(error):
    if error.code == 400:
        message = 'Invalid JSON. Check the request body syntax.'
    else:
        message = error.name + '.'
    return jsonify(error=message), error.code


@app.errorhandler(mysql.connector.Error)
def database_error(error):
    # Never return or log passwords, connection settings, or SQL error text.
    app.logger.error('Database operation failed (%s).', type(error).__name__)
    return jsonify(error='Database operation failed. Check the server and local configuration.'), 500


@app.errorhandler(Exception)
def unexpected_error(error):
    app.logger.error('Unexpected server error (%s).', type(error).__name__)
    return jsonify(error='An unexpected server error occurred. Please try again.'), 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=int(os.getenv('PORT', '5000')), debug=False)
