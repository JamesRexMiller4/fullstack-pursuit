import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
# import json
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(req, selection):
  page = req.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions


def create_app(test_config=None):
  app = Flask(__name__)
  setup_db(app)
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  @app.after_request
  def after_request(res):
    res.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    res.headers.add('Access-Control-Allow-Methods', 'GET, DELETE, POST')
    return res

  @app.route('/')
  def index():
    return ':)'

  @app.route('/categories')
  def get_categories():
    categories = Category.query.order_by(Category.id).all()

    response = []

    for category in categories:
      response.append({
        "id": category.id,
        "type": category.type
      })

    if len(categories) == 0:
      abort(404)

    return jsonify({
      "success": True,
      "categories": response
    })

  return app