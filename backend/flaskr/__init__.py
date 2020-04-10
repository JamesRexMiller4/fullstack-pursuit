import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import *

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  # cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  @app.after_request
  def after_request(res):
    res.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    res.headers.add('Access-Control-Allow-Methods', 'GET, DELETE, POST')
    return res

  return app