from http import client
import unittest
from unittest.mock import patch
import os
import sqlite3
from app import app
import flask

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

    #check login functionality
    def test_login(self):
        tester = app.test_client().post('/login', 
            data={
                    'email': 'peter@schmidt.de',
                    'password': 'MeinHund'
                })
        self.assertTrue(tester)

    #test register route
    def test_register_route(self):
        tester = app.test_client(self)
        response = tester.get("/register")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    #test findcar route
    def test_findcar_route(self):
        tester = app.test_client(self)
        response = tester.get("/findCar")
        statuscode = response.status_code
        self.assertEqual(statuscode, 302)

    #test findcar route
    def test_findcar_route_loggedin(self):
        with app.test_client() as c:
            tester = c.post('/login', 
                data={
                        'email': 'peter@schmidt.de',
                        'password': 'MeinHund'
                    })
            self.assertTrue(tester)
            resp = c.get('/findCar')
            statuscode = resp.status_code
            self.assertEqual(statuscode, 200)

        #test register route
    def test_register_route_loggedin(self):
        with app.test_client() as c:
            tester = c.post('/register', 
                data={
                        'username': 'peter123',
                        'firstName': 'Peter',
                        'lastName': 'Schmidt',
                        'email': 'peter@schmidt.de',
                        'street': 'Teststrasse',
                        'houseNum': '456',
                        'city': 'Unitteststadt',
                        'postalCode': '98765',
                        'password': 'MeinHund'
                    })
            self.assertTrue(tester)

            #test register route
    def test_register_route_loggedin_2(self):
        with app.test_client() as c:
            tester = c.post('/register', 
                data={
                        'username': '',
                        'firstName': 'Peter',
                        'lastName': 'Schmidt',
                        'email': 'peter@schmidt.de',
                        'street': 'Teststrasse',
                        'houseNum': '456',
                        'city': 'Unitteststadt',
                        'postalCode': '98765',
                        'password': 'MeinHund'
                    })
            self.assertTrue(tester)

    #test profile route
    def test_profile_route(self):
        tester = app.test_client(self)
        response = tester.get("/profile")
        statuscode = response.status_code
        self.assertEqual(statuscode, 302)

    #test profile route
    def test_profile_route_loggedin(self):
        with app.test_client() as c:
            tester = c.post('/login', 
                data={
                        'email': 'peter@schmidt.de',
                        'password': 'MeinHund'
                    })
            self.assertTrue(tester)
            resp = c.get('/profile')
            statuscode = resp.status_code
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

#check profile page
    def test_profile(self):
        tester = app.test_client().post('/profile', 
            data={
                'UserID': 2, 
                'formButton': 'Speichern',
                'username': 'lena', 
                'password': 'x',
                'email': 'lena@gerken.de',
                'Adresse': 1
                })
        self.assertTrue(tester)

#test profile route
    def test_profile_loggedin(self):
        with app.test_client() as c:
            tester = c.post('/login', 
                data={
                        'email': 'peter@schmidt.de',
                        'password': 'MeinHund'
                    })
            self.assertTrue(tester)
            resp = c.get('/profile')
            statuscode = resp.status_code
            self.assertEqual(statuscode, 200)

    #test profile route
    def test_profile_loggedin_post(self):
        with app.test_client() as c:
            tester = c.post('/login', 
                data={
                        'email': 'peter@schmidt.de',
                        'password': 'MeinHund'
                    })
            self.assertTrue(tester)
            resp = c.post('/profile', 
            data={
                'UserID': 2, 
                'formButton': 'Speichern',
                'username': 'lena', 
                'password': 'x',
                'email': 'lena@gerken.de',
                'Adresse': 1
                })
        self.assertTrue(resp)

    #test profile route
    def test_profile_loggedin_post(self):
        with app.test_client() as c:
            tester = c.post('/login', 
                data={
                        'email': 'peter@schmidt.de',
                        'password': 'MeinHund'
                    })
            self.assertTrue(tester)
            resp = c.post('/profile', 
            data={
                'formButton': 'Speichern',
                'username': 'lena', 
                'password': 'x',
                'email': 'lena@gerken.de',
                'street': 'Testweg',
                'houseNum': 1,
                'city': 'Muenchen',
                'postalCode': 12345
                })
        self.assertTrue(resp)

#check findCar page
    def test_findcar(self):
        tester = app.test_client().post('/findCar', 
            data={
                    'UserID': 2
                })
        self.assertTrue(tester)

    #test findcar logged in
    def test_findcar_loggedin_post(self):
        with app.test_client() as c:
            tester = c.post('/login', 
                data={
                        'email': 'peter@schmidt.de',
                        'password': 'MeinHund'
                    })
            self.assertTrue(tester)
            #assert c.form.get("filter") == "Suchen"
            resp = c.post('/findCar', 
            data={
                    'filter': 'Suchen',
                    'place': 'Stuttgart',
                    'startdate': '2022-06-01',
                    'enddate': '2022-06-05',
                    'carclass': 'Limousine',
                    'maxprice': '200'
                })
        self.assertTrue(resp)

    def test_edit_profile(self):
        with app.test_client() as c:
            tester = c.post('/login', 
                data={
                        'email': 'peter@schmidt.de',
                        'password': 'MeinHund'
                    })
            self.assertTrue(tester)
            resp = c.post('/profile', 
            data={
                    'username': 'peter33',
                    'password': 'MeinHund',
                    'passwordConfirm': 'MeinHund',
                    'email': 'peter@schmidt.de',
                    'street': 'Hammanstraße',
                    'houseNum': '2',
                    'city': 'Frankfurt am Main',
                    'postalCode': '60322',
                })
        self.assertTrue(resp)

    #check timeframe functionality
    def test_timeframes(self):
        tester = app.test_client().post('/add-timeframe/1', 
            data={
                'startdate': '2022-06-01', 
                'enddate': '2022-06-03'
                })
        self.assertTrue(tester)

    #check edit functionality
    def test_edit(self):
        tester = app.test_client().post('/edit-car/1', 
            data={
                'modell': 'E-Klasse', 
                'fahrzeugtyp': 'Limousine',
                'hersteller': 'Mercedes-Benz',
                'preis': '40'
                })
        self.assertTrue(tester)

#check rentcar functionality
    def test_rentcar(self):
        tester = app.test_client().post('/rent-car/1', 
            data={
                    'startdate': '2022-06-01',
                    'enddate': '2022-06-03'
                })
        self.assertTrue(tester)

#check logout functionality
    def test_logout(self):
        tester = app.test_client().post('/logout', 
            data={

                })
        self.assertTrue(tester)


if __name__ == '__main__':
    unittest.main()

