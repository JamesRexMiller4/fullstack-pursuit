import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  app = Flask(__name__)
  setup_db(app)


  return app