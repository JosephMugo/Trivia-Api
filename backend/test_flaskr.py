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
            # ----> Create records <----
            # categories
            self.science = Category('Science')
            self.db.session.add(self.science)
            self.art = Category('Art')
            self.db.session.add(self.art)
            self.geography = Category('Geography')
            self.db.session.add(self.geography)
            self.history = Category('History')
            self.db.session.add(self.history)
            self.entertainment = Category('Entertainment')
            self.db.session.add(self.entertainment)
            self.sports = Category('Sports')
            self.db.session.add(self.sports)
            self.db.session.commit()
            # questions
            self.question_one = Question('What question is this?', 'test question', 1, 1)
            self.question_one.insert()
            self.question_two = Question('What type of question is this?', 'second test question', 1, 1)
            self.question_two.insert()
    
    def tearDown(self):
        """Executed after each test"""
        # binds the app to the current context
        with self.app.app_context():
            # Remove records
            # categories
            self.db.session.delete(self.science)
            self.db.session.delete(self.art)
            self.db.session.delete(self.geography)
            self.db.session.delete(self.history)
            self.db.session.delete(self.entertainment)
            self.db.session.delete(self.sports)
            
            # questions
            self.question_one.delete()
            self.question_two.delete()
            
            #commit changes
            self.db.session.commit()
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

    # # GET Questions Test
    # def test_get_questions(self):
    #     res = self.client.get('/questions')
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(len(data['questions']))
    #     self.assertTrue(data['total_questions'])
    #     self.assertTrue(len(data['categories']))

    # def test_404_get_questions(self):
    #     res = self.client.get('/questions/')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'Not Found')

    # Delete Question
    # def test_delete_question(self):
    #     id = Question.query.first().id

    #     res = self.client.delete('/questions/' + str(id))
    #     data = json.loads(res.data)
    #     question = Question.query.filter_by(id=5).first()
        
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['deleted'], id)
    #     self.assertTrue(len(data['questions']))
    #     self.assertTrue(data['total_questions'])
    
    # def test_422_delete_question(self):
    #     res = self.client.delete('/questions/1000')
    #     data = json.loads(res.data)
    #     question = Question.query.filter_by(id=1000).first()

    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], "Unprocessable Entity")

    # Post Question
    # def test_post_question(self):
    #     new_question = {
    #         "question": "What is the test question",
    #         "answer": "This is the test question",
    #         "difficulty": 1,
    #         "category": 1
    #     }

    #     res = self.client.post('/questions', json=new_question)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(len(data['questions']))
    #     self.assertTrue(data['total_questions'])

    # def test_422_post_question(self):
    #     res = self.client.post('/questions')
    #     data = json.loads(res.data)

    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], "Unprocessable Entity")
    # Search Questions
    # def test_search_questions(self):
    #     res = self.client.post('/questions', json={'searchTerm': 'test'})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['questions'])
    #     self.assertTrue(data['total_questions'])
    # Category Questions

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()