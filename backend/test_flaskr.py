import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
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
    # Test for success
    # test: GET /questions endpoint
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        # we want to make sure that the staus code is 200, the success value of the body is true, assert true that there is a number of total questions and that there are questions and categories in that list
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        # self.assertTrue(len(data['categories']))
     
    # Test for error behavior
    # test error: GET /questions?page=1000 endpoint .. page = 1000 isn't found
    def test_404_sent_requesting_questions_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # test: GET /categories endpoint .. test successful get categories
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        # self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))
        self.assertEqual(res.status_code, 200)

    # test error: GET /categories/9999 endpoint .. 9999 isn't found
    def test_404_sent_requesting_non_existing_category(self):
        res = self.client().get('/categories/9999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # test: DELETE /questions/13 a specific question endpoint .. test successful delete a question
    def test_delete_question(self):
        res = self.client().delete('/questions/13')
        data = json.loads(res.data)
        # question = Question.query.filter(Question.id == 13).one_or_none()

        # self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], '13')
        # self.assertEqual(question, None)


    # test error: DELETE /questions/a endpoint .. abc isn't found as a path so we can't process it
    def test_422_sent_deleting_non_existing_question(self):
        res = self.client().delete('/questions/abc')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # test: POST /questions endpoint .. test successful add a question
    def test_add_question(self):
        new_question = {
            'question': 'new question',
            'answer': 'new answer',
            'difficulty': 1,
            'category': 1
        }
        total_questions_before = len(Question.query.all())
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)
        total_questions_after = len(Question.query.all())

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(total_questions_after, total_questions_before + 1)

    # test error: POST /questions/question endpoint .. question isn't found as a path so we can't process it
    def test_422_add_question(self):
        new_question = {
            'question': 'new_question',
            'answer': 'new_answer',
            'category': 1
        }
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    # test: POST /questions/search endpoint .. test successful serach of a question
    def test_search_questions(self):
        new_search = {'searchTerm': 'abc'}
        res = self.client().post('/questions/search', json=new_search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['questions'])
        self.assertIsNotNone(data['total_questions'])

    # test error: POST /questions/search endpoint .. question isn't found in the search
    def test_404_search_question(self):
        new_search = {
            'searchTerm': '',
        }
        res = self.client().post('/questions/search', json=new_search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
        
    # test: GET /categories/1/questions endpoint
    def test_get_questions_per_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    # test error: GET /categories/a/questions endpoint .. questions isn't found in its categories
    def test_404_get_questions_per_category(self):
        res = self.client().get('/categories/a/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    # test: POST /quizzes endpoint
    def test_play_quiz(self):
        # new_quiz_round = {'previous_questions': [],'quiz_category': {'type': 'Entertainment', 'id': 5}}
        new_quiz_round = {'previous_questions': [],'quiz_category': {'type': 'Science', 'id': 1}}
        res = self.client().post('/quizzes', json=new_quiz_round)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    # test error: POST /quizzes endpoint .. previous_questions isn't found in quizzes path so we can't process it
    def test_404_play_quiz(self):
        new_quiz_round = {'previous_questions': []}
        res = self.client().post('/quizzes', json=new_quiz_round)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    ################################################
    # To test all these test, We run one line
        # python3 test_flaskr.py  
    ################################################

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()