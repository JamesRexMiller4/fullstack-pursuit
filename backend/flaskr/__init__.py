import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
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
  CORS(app)

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, DELETE, POST')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response 

  @app.route('/')
  def index():
    return ':)'

  @app.route('/categories')
  def get_categories():
    categories = Category.query.order_by(Category.id).all()

    response = {}

    for category in categories:
      response[category.id] = category.type

    if len(categories) == 0:
      abort(404)

    return jsonify({
      "success": True,
      "categories": response
    })

  @app.route('/questions')
  def get_questions():
    questions = Question.query.order_by(Question.id).all()
    current_questions = paginate_questions(request, questions)

    if len(current_questions) == 0:
      abort(404)

    categories = Category.query.order_by(Category.id).all()

    categories_dict = {}

    for category in categories:
      categories_dict[category.id] = category.type

    response = {
        "success": True,
        "questions": current_questions,
        "total_questions": len(questions),
        "current_category": None,
        "categories": categories_dict
      }
    return jsonify(response)

  @app.route('/questions/<int:question_id>', methods=["DELETE"])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id==question_id).one_or_none()

      if question is None:
        abort(404)

      question.delete()

      questions = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, questions)
      
      response = {
        "success": True,
        "deleted": question_id,
        "questions": current_questions,
        "total_questions": len(questions)
      }

      return jsonify(response)
    except:
      abort(422)

  @app.route('/questions', methods=['POST'])
  def post_question():
    body = request.get_json()

    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_category = body.get('category', None)
    new_difficulty = body.get('difficulty', None)
    search = body.get('searchTerm', None)

    if search: 
      question = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search)))
      current_questions = paginate_questions(request, question)

      if len(current_questions):
        response = {
          "success": True,
          "questions": current_questions,
          "total_questions": len(question.all())
        }
        return jsonify(response)
      else:
        abort(404)

    else:
      try:
        question = Question(question=new_question,answer=new_answer,category=new_category,difficulty=new_difficulty)
        question.insert()

        questions = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, questions)

        response = {
          "success": True,
          "id": question.id,
          "question": question.question,
          "answer": question.answer,
          "category": question.category,
          "difficulty": question.difficulty,
          "questions": current_questions,
          "total_questions": len(questions)
        }
        return jsonify(response)
      except:
        abort(422)

  return app