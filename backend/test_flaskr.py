import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

class TriviaTestCase(unittest.TestCase):
  def setUp(self):
    self.app = create_app()
    self.client = self.app.test_client
    self.database_name = 'trivia_test'
    self.database_path = 'postgres://{}@{}/{}'.format('jamesmiller', 'localhost:5432', self.database_name)
    setup_db(self.app, self.database_path)

    with self.app.app_context():
      self.db = SQLAlchemy()
      self.db.init_app(self.app)
      self.db.create_all()

    self.new_question = {
        "question": 'When Michael Jordan played for the Chicago Bulls, how many NBA\
          championships did he win?',
        "answer": "6",
        "category": 6,
        "difficulty": 2,
      }

  def tearDown(self):
    pass

  def test_get_categories(self):
    res = self.client().get('/categories')
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertTrue(data['categories'])

  def test_get_questions(self):
    res = self.client().get('/questions')
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(data["success"], True)
    self.assertTrue(data['questions'])
    self.assertTrue(len(data["questions"]) > 0)
    self.assertTrue(len(data["questions"]) <= 10)
    self.assertTrue(data["total_questions"])
    self.assertTrue(data['categories'])
    self.assertEqual(data['current_category'], None)
    # test for different pages
    res = self.client().get('/questions?page=2')
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(data["success"], True)
    self.assertTrue(data['questions'])
    self.assertTrue(len(data["questions"]) > 0)
    self.assertTrue(len(data["questions"]) <= 10)
    self.assertTrue(data["total_questions"])
    self.assertTrue(data['categories'])
    self.assertEqual(data['current_category'], None)

  def test_delete_question(self):
    res = self.client().delete('/questions/4')
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(data["success"], True)
    self.assertEqual(data["deleted"], 4)
    self.assertTrue(data["questions"])
    self.assertTrue(data["total_questions"] > 10)

  def test_post_question(self):
    res = self.client().post('/questions', self.new_question)
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(data["success"], True)
    self.assertTrue(data["id"])
    self.assertEqual(data["question"], self.new_question["question"])
    self.assertEqual(data["answer"], "6")
    self.assertEqual(data["difficulty"], 2)
    self.assertEqual(data["category"], 6)




  if __name__ == '__main__':
    unittest.main()