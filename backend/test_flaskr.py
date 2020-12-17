import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

passwordRead = open('password.txt', 'r')
password = passwordRead.readline()

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.database_name = "trivia_test"
        self.database_path = "postgres://postgres:{}@{}/{}".format(password, 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # Categories table has to be filled for the test to operate correctly
    def test_get_categories(self):
        res = self.client.get('/categories')
        print(res.data)
        data = json.loads(res.data)

        category_list = Category.query.all()
        categories = []
        for category in category_list:
            categories.append(category.type)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['categories'], categories)
    
    def test_422_get_categories(self):
        res = self.client.get('/categories')
        print(res.data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()