import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        with open('password.txt', 'r') as passwordFile:
            self.password = passwordFile.readline()
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.database_name = "trivia_test"
        self.database_path = "postgres://postgres:{}@{}/{}".format(self.password, 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after each test"""
        
    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # GET Categories Test
    # Categories table has to be filled for the test to operate correctly
    def test_get_categories(self):
        res = self.client.get('/categories')
        data = json.loads(res.data)

        category_list = Category.query.all()
        categories = []
        for category in category_list:
            categories.append(category.type)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['categories'], categories)
    
    def test_404_get_categories(self):
        res = self.client.get('/categories/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    # GET Questions Test
    def test_get_questions(self):
        res = self.client.get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories']))

    def test_404_get_questions(self):
        res = self.client.get('/questions/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    # Delete Question
    def test_delete_question(self):
        id = Question.query.first().id

        res = self.client.delete('/questions/' + str(id))
        data = json.loads(res.data)
        question = Question.query.filter_by(id=5).first()
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], id)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
    
    def test_404_delete_question(self):
        res = self.client.delete('/questions/1000')
        data = json.loads(res.data)
        question = Question.query.filter_by(id=1000).first()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Not Found")

    # Add Question
    def test_post_question(self):
        new_question = {
            "question": "What is the test question",
            "answer": "This is the test question",
            "difficulty": 1,
            "category": 1
        }

        res = self.client.post('/questions', json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])

    def test_422_post_question(self):
        res = self.client.post('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unprocessable Entity")

    # Search Questions
    def test_search_questions(self):
        search_term = {
            "searchTerm": "title"
        }
        res = self.client.post('/questions', json=search_term)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue((len(data['questions']) >= 0))
        self.assertTrue((data['total_questions'] >= 0))

    def test_422_search_question(self):
        res = self.client.post('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unprocessable Entity")
        
    # Category Questions
    def test_get_categories_question(self):
        res = self.client.get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue((len(data['questions']) >= 0))
    
    def test_404_get_categories_question(self):
        res = self.client.get('/categories/10000/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Not Found")
    
    # Quiz
    def test_post_quiz(self):
        info = {
            "previous_question": [],
            "quiz_category": {
                "type": "History",
                "id": 3
            }
        }
        res = self.client.post('/quizzes', json=info)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['question']) >= 0)

    def test_422_post_quiz(self):
        res = self.client.post('/quizzes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unprocessable Entity")

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()