import os
from flask import Flask, request, abort, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
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
    response.headers.add('Access-Control-Allow-Methods', 'GET, DELETE, POST, OPTIONS')
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

    try:
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

  @app.route('/categories/<int:category_id>/questions')
  def get_questions_by_category(category_id):
    try:
      questions = Question.query.order_by(Question.id).filter(Question.category==category_id).all()
      current_questions = paginate_questions(request, questions)

      response = {
        "success": True,
        "questions": current_questions,
        "total_questions": len(questions),
        "current_category": category_id
      }
      return jsonify(response)
    except:
      abort(422)

  @app.route('/quizzes', methods=["POST", "OPTIONS"])
  @cross_origin()
  def post_quiz_play(): 
    body = request.get_json()

    try:
      category = body.get("quiz_category", None)
      previous_questions = body.get("previous_questions", None)

      if category["id"] == 0 and len(previous_questions) == 0:
        questions = Question.query.order_by(Question.id).all()
        random_index = random.randint(0, len(questions) - 1)
        current_question = questions[random_index]
        response = {
              "success": True,
              "question": current_question.format()
            }
        return jsonify(response)
      else:
        if category["id"] == 0:
          questions = Question.query.order_by(Question.id).all()
          new_list = []

          for question in questions:
            if not question.__dict__["id"] in previous_questions:
              new_list.append(question)
          

          if len(new_list) > 0:
            random_index = random.randint(0, len(new_list) - 1)
            current_question = new_list[random_index]
            response = {
              "success": True,
              "question": current_question.format()
            }
            return jsonify(response)
          else:
            response = {
            "success": True,
            "question": False
            }
            return jsonify(response)

        else:
          if len(previous_questions) == 0:
            questions = Question.query.order_by(Question.id).filter(Question.category==category["id"]).all()
            random_index = random.randint(0, len(questions) - 1)
            current_question = questions[random_index]

            response = {
              "success": True,
              "question": current_question.format()
            }
            return jsonify(response)
          else: 
            questions = Question.query.order_by(Question.id).filter(Question.category==category["id"]).all()
            new_list = []

            for question in questions:
              if not question.__dict__["id"] in previous_questions:
                new_list.append(question)

            if len(new_list) > 0:
              random_index = random.randint(0, len(new_list) - 1)
              current_question = new_list[random_index]
              response = {
                "success": True,
                "question": current_question.format()
              }
              return jsonify(response)
            else:
              response = {
              "success": True,
              "question": False
              }
              return jsonify(response)
    except:
      abort(422)

  return app