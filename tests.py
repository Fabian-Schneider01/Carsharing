import unittest
from app import app
import os

class FlaskTestCase(unittest.TestCase):
    def test_index_route(self):
        tester = app.test_client(self)
        response = tester.get("/")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_login_route(self):
        tester = app.test_client(self)
        response = tester.get("/login")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_register_route(self):
        tester = app.test_client(self)
        response = tester.get("/register")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
    
    def test_existing_db(self):
        tester = os.path.exists("database.sqlite")
        self.assertTrue(tester)
    
    
        
    

if __name__ == '__main__':
    unittest.main()

