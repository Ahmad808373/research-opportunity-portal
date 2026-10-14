"""Live HTTP/MySQL checks. Use a disposable, initialized *_test database only.

Run from the project root: python -m unittest discover -s tests -v
The suite starts/stops its own Flask process on port 5010, never your main server.
"""
import copy
import json
import os
import subprocess
import sys
import time
import unittest
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import mysql.connector
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / 'backend' / '.env')
BASE = 'http://127.0.0.1:5010'
EXAMPLE = {
    'title': 'Test: Network Traffic Analysis',
    'description': 'Study university network traffic and identify congestion.',
    'research_area': 'Computer Networks',
    'faculty_name': 'Dr. Example Faculty',
    'department': 'Computer Science',
    'required_skills': 'Python, TCP/IP, Wireshark',
    'available_positions': 2,
    'application_deadline': '2026-12-20',
    'status': 'Open',
}


def request(method, path='', body=None, raw=None, content_type='application/json'):
    payload = raw if raw is not None else (json.dumps(body).encode() if body is not None else None)
    req = Request(BASE + '/api/opportunities' + path, data=payload, method=method,
                  headers={'Content-Type': content_type})
    try:
        with urlopen(req, timeout=10) as response:
            return response.status, json.load(response)
    except HTTPError as error:
        return error.code, json.load(error)


class PortalAPITests(unittest.TestCase):
    @classmethod
    def start_backend(cls, db_port=None):
        env = dict(os.environ, PORT='5010')
        if db_port is not None:
            env['DB_PORT'] = str(db_port)
        cls.server = subprocess.Popen([sys.executable, str(ROOT / 'backend' / 'portal_app.py')],
                                      env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for attempt in range(60):
            try:
                with urlopen(BASE, timeout=1): return
            except (URLError, TimeoutError): time.sleep(.1)
        cls.stop_backend()
        raise RuntimeError('Test Flask server did not start.')

    @classmethod
    def stop_backend(cls):
        if getattr(cls, 'server', None) is not None:
            cls.server.terminate()
            cls.server.wait(timeout=10)

    @classmethod
    def setUpClass(cls):
        db_name = os.getenv('DB_NAME', '')
        if not db_name.endswith('_test'):
            raise RuntimeError('Set DB_NAME to an initialized disposable database ending in _test.')
        cls.db = mysql.connector.connect(
            host=os.getenv('DB_HOST', '127.0.0.1'), port=int(os.getenv('DB_PORT', '3306')),
            user=os.getenv('DB_USER', 'portal_user'), password=os.getenv('DB_PASSWORD', ''),
            database=db_name, autocommit=True)
        cls.addClassCleanup(cls.db.close)
        cls.start_backend()
        cls.addClassCleanup(cls.stop_backend)

    def setUp(self):
        with self.db.cursor() as cursor: cursor.execute('DELETE FROM opportunities')

    def create(self, body=None):
        status, response = request('POST', body=body or EXAMPLE)
        self.assertEqual(status, 201, response)
        return response['opportunity']

    def test_complete_crud(self):
        ids = []
        for title in ['Networks', 'Machine Learning', 'Human Computer Interaction']:
            data = dict(EXAMPLE, title=title)
            ids.append(self.create(data)['id'])
        self.assertEqual(len(set(ids)), 3)
        status, rows = request('GET')
        self.assertEqual(status, 200)
        self.assertEqual(len(rows), 3)
        status, row = request('GET', '/' + str(ids[0]))
        self.assertEqual(status, 200)
        self.assertEqual(row['title'], 'Networks')
        self.assertEqual(set(row), set(EXAMPLE) | {'id'})
        updated = dict(EXAMPLE, title='Updated title', description='New description',
                       research_area='Security', faculty_name='Professor Updated', department='IT',
                       required_skills='SQL', available_positions=0, application_deadline='2027-02-28')
        status, response = request('PUT', '/' + str(ids[0]), updated)
        self.assertEqual(status, 200)
        self.assertEqual({k: response['opportunity'][k] for k in updated}, updated)
        # MySQL rowcount can be zero for an unchanged update: it must still be 200.
        self.assertEqual(request('PUT', '/' + str(ids[0]), updated)[0], 200)
        status, response = request('PUT', '/' + str(ids[0]), {'status': 'Closed'})
        self.assertEqual(status, 200)
        self.assertEqual(response['opportunity']['status'], 'Closed')
        self.assertEqual(request('GET', '/' + str(ids[0]))[1]['status'], 'Closed')
        self.assertEqual(request('DELETE', '/' + str(ids[0]))[0], 200)
        self.assertEqual(request('GET', '/' + str(ids[0]))[0], 404)
        self.assertEqual(request('DELETE', '/' + str(ids[0]))[0], 404)
        with self.db.cursor() as cursor:
            cursor.execute('SELECT COUNT(*) FROM opportunities WHERE id=%s', (ids[0],))
            self.assertEqual(cursor.fetchone()[0], 0)

    def test_empty_database(self):
        self.assertEqual(request('GET'), (200, []))

    def test_required_fields(self):
        for field in EXAMPLE:
            for value in [None, '', '   ']:
                with self.subTest(field=field, value=value):
                    data = dict(EXAMPLE)
                    data[field] = value
                    status, response = request('POST', body=data)
                    self.assertEqual(status, 400)
                    self.assertIn('error', response)
            data = dict(EXAMPLE)
            del data[field]
            self.assertEqual(request('POST', body=data)[0], 400)

    def test_invalid_positions(self):
        for value in [-1, 2.5, '2', True, 2147483648, [], {}]:
            with self.subTest(value=value):
                self.assertEqual(request('POST', body=dict(EXAMPLE, available_positions=value))[0], 400)

    def test_invalid_dates_and_status(self):
        for value in ['2026-02-30', '2025-02-29', '10/10/2026', '2026-1-01', '0999-12-31', '2026-12-20T00:00:00']:
            with self.subTest(value=value):
                self.assertEqual(request('POST', body=dict(EXAMPLE, application_deadline=value))[0], 400)
        self.assertEqual(request('POST', body=dict(EXAMPLE, status='open'))[0], 400)
        self.assertEqual(request('POST', body=dict(EXAMPLE, status=['Open']))[0], 400)
        self.assertEqual(self.create(dict(EXAMPLE, application_deadline='2024-02-29'))['application_deadline'], '2024-02-29')

    def test_invalid_json_and_unknown_fields(self):
        for raw in [b'{broken', b'[]', b'null', b'{}', b'"hello"', b'']:
            with self.subTest(raw=raw): self.assertEqual(request('POST', raw=raw)[0], 400)
        self.assertEqual(request('POST', raw=b'{}', content_type='text/plain')[0], 400)
        self.assertEqual(request('POST', body=dict(EXAMPLE, id=10))[0], 400)
        self.assertEqual(request('POST', body=dict(EXAMPLE, title='x' * 201))[0], 400)

    def test_missing_and_invalid_ids(self):
        for method in ['GET', 'PUT', 'DELETE']:
            body = {'status': 'Closed'} if method == 'PUT' else None
            self.assertEqual(request(method, '/2147483647', body)[0], 404)
            for value in ['abc', '0', '-1', '2147483648', '1.5', '1%20OR%201=1']:
                with self.subTest(method=method, id=value):
                    self.assertEqual(request(method, '/' + value, body)[0], 400)

    def test_invalid_update_does_not_change_record(self):
        original = self.create()
        path = '/' + str(original['id'])
        for changes in [{}, {'title': ''}, {'available_positions': -2}, {'status': 'Pending'}, {'unknown': 1}]:
            with self.subTest(changes=changes): self.assertEqual(request('PUT', path, changes)[0], 400)
        self.assertEqual(request('GET', path)[1], original)

    def test_sql_text_is_data(self):
        title = "Faculty's study'); DROP TABLE opportunities; -- <script>alert(1)</script>"
        row = self.create(dict(EXAMPLE, title=title))
        self.assertEqual(request('GET', '/' + str(row['id']))[1]['title'], title)
        self.assertEqual(len(request('GET')[1]), 1)

    def test_repeated_requests(self):
        first = self.create()
        second = self.create()
        self.assertNotEqual(first['id'], second['id'])
        self.assertEqual(len(request('GET')[1]), 2)
        # Direct API calls may create duplicates intentionally; UI blocks double clicks.

    def test_persistence_after_flask_restart(self):
        row = self.create()
        self.stop_backend()
        self.start_backend()
        self.assertEqual(request('GET', '/' + str(row['id'])), (200, row))

    def test_database_constraints(self):
        row = self.create()
        cases = [('available_positions', -1), ('title', ''), ('status', 'Pending'), ('description', None)]
        for field, value in cases:
            with self.subTest(field=field):
                with self.db.cursor() as cursor:
                    with self.assertRaises(mysql.connector.Error):
                        cursor.execute(f'UPDATE opportunities SET {field}=%s WHERE id=%s', (value, row['id']))

    def test_safe_database_failure(self):
        self.stop_backend()
        try:
            self.start_backend(db_port=1)  # Real connection failure, not a fabricated mock result.
            status, response = request('GET')
            self.assertEqual(status, 500)
            self.assertEqual(set(response), {'error'})
            for secret in ['Traceback', 'SELECT', 'password=', 'mysql.connector']:
                self.assertNotIn(secret, response['error'])
        finally:
            self.stop_backend()
            self.start_backend()


if __name__ == '__main__':
    unittest.main(verbosity=2)
