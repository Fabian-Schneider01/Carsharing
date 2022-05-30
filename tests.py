import unittest
from unittest.mock import patch
import os
import sqlite3
from app import app

class FlaskTestCase(unittest.TestCase):
    #test index route
    def test_index_route(self):
        tester = app.test_client(self)
        response = tester.get("/")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    #test login route
    def test_login_route(self):
        tester = app.test_client(self)
        response = tester.get("/login")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    #test register route
    def test_register_route(self):
        tester = app.test_client(self)
        response = tester.get("/register")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
    
    #check if database exists
    def test_existing_db(self):
        tester = os.path.exists("database.sqlite")
        self.assertTrue(tester)

    #check if connection is being created
    def test_connection(self, dbname='database.sqlite'):
        tester = sqlite3.connect(dbname)
        self.assertTrue(tester)

    #check login functionality
    def test_client(self):
        tester = app.test_client().post('/login', 
            data={
                'Benutzername': 'lena', 
                'Passwort': 'x',
                'Email': 'lena@gerken.de',
                'Adresse': 1
                })
        self.assertTrue(tester)

    #check register redirect
    def test_register_redirect(self):
        tester = app.test_client(self)
        response = tester.get("/login")
        html = response.data.decode()
        assert '<a href="/register">'in html
        self.assertEqual(response.status_code, 200)

    #test setting up secret key
    def setUp(self):
        app.config['SECRET_KEY'] = '4khJ7Ggljy'
        self.app = app.test_client()
        assert self.app 

    #test session
    def test_session(self):
        with patch("app.session", dict()) as session:
            client = app.test_client()
            response = client.post("/", data={
                "username": "test"
            })
            self.assertEqual(session.get("username") != "", True)
            self.assertEqual(response.data != b"", True)

if __name__ == '__main__':
    unittest.main()

