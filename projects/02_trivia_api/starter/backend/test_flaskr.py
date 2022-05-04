import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

from dotenv import load_dotenv


load_dotenv()








class TriviaTestCase(unittest.TestCase):
    """This class represultents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        
        self.database_name = "postgres_test"
        self.username = os.environ["USERID"]
        self.password = os.environ["PASSWORD"]
        self.host = os.environ["HOST"]
        self.port = os.environ["PORT"]
        self.database_path = "postgresql://{}:{}@{}:{}/{}".format(self.username,self.password,self.host,self.port,self.database_name)
        
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
    def test_for_paginated_questions(self):
        result = self.client().get('/questions')
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["categories"]))
        self.assertTrue(len(data["questions"]))

    def test_for_page_bad_request(self):
        result = self.client().get('/questions?page=1000')
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Page not found')

    def test_for_categories(self):
        result = self.client().get('/categories')
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])

    def test_get_categories_not_allowed(self):
        result = self.client().delete('/categories')
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 405)
        self.assertEqual(data["success"], False)


    def test_delete_question(self):
        result = self.client().delete('/questions/5')
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_delete_question_not_found(self):
        result = self.client().delete('/questions/10000')
        
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable resource")

    def test_add_question(self):
        newQuestion = {
            'question': 'what is your name?',
            'answer': 'Manal',
            'difficulty': 1,
            'category': 1
        }
        result = self.client().post('/questions', json=newQuestion)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_search(self):
        search = {'searchTerm': 'what', }
        result = self.client().post('/questions/search', json=search)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 10)

    def test_search_not_found(self):
        search = {
            'searchTerm': 'dcbsckjdsc',
        }
        result = self.client().post('/questions/search', json=search)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Page not found')

    def test_questions_in_category(self):
        result = self.client().get('/categories/1/questions')
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotEqual(len(data['questions']), 0)
        self.assertEqual(data['current_category'], 'Science')

    def test_questions_in_category_not_found(self):
        result = self.client().get('/categories/100/questions')
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_quiz(self):
        result = self.client().post('/quizzes',
                                 json={'previous_questions': [],
                                       'quiz_category':
                                       {'id': '5', 'type': 'Entertainment'}})
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertTrue(data['question'])
        self.assertEqual(data['question']['category'], 5)

    def test_quiz_not_found_category(self):
        quiz = {
            'previous_questions': [6],
            'quiz_category': {
                'type': 'XXX',
                'id': 'X'
            }
        }
        result = self.client().post('/quizzes', json=quiz)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 404)
        self.assertEqual(data['success'], False)



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()