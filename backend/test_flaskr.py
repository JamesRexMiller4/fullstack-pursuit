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
    self.assertTrue(data['current_category'])
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
    self.assertTrue(data['current_category'])

  if __name__ == '__main__':
    unittest.main()