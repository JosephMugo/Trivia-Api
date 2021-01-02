import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random 

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={r"/questions/*": {"origins": "*"}})
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
      response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
      return response
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def get_categories():
      try:
          category_list = Category.query.all()
          categories = []
          for category in category_list:
                categories.append(category.type)
          return jsonify(
              {
                "success": True,
                "categories": categories,
              }
          )
      except:
          print('Error: ' + str(sys.exc_info()))
          abort(422)

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions', methods=['GET'])
  def get_questions():
      try:
          questions = Question.query.all()
          formatted_questions = paginate_questions(request, questions)

          category_list = Category.query.all()
          categories = []
          for category in category_list:
                categories.append(category.type)

          return jsonify({
              "success": True,
              "questions": formatted_questions,
              "total_questions": len(formatted_questions),
              "categories": categories
          })
      except:
          print('Error: ' + str(sys.exc_info()))
          abort(422)

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
      try:
          question = Question.query.filter_by(id=question_id).one_or_none()

          if question is None:
              abort(404)
          
          question.delete()
          questions_after_delete = Question.query.order_by(Question.id).all()
          questions = paginate_questions(request, questions_after_delete)

          return jsonify({
              "success": True,
              "deleted": question_id,
              "questions": questions,
              'total_questions': len(questions_after_delete)
          })
      except:
        abort(422)
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def post_question():
      body = request.get_json()
      question = body.get("question", None)
      answer = body.get("answer", None)
      difficulty = body.get("difficulty", None)
      category = body.get("category", None)
      search_term = body.get("searchTerm", None)
      try:
          if (search_term != None):
              questions = Question.query.all()
              # Search
              search_result = list(filter(lambda x: search_term in x.question, Question.query.all()))
              
              return jsonify({
                  "success": True,
                  "questions": paginate_questions(request, search_result),
                  "total_questions": len(search_result)
              })
          else:
              # Add new question
              question = Question(question=question, answer=answer, difficulty=difficulty, category=category)
              question.insert()

              questions = Question.query.all()
              formatted_questions = [question.format() for question in questions]

              return jsonify({
                  "success": True,
                  "question_created": question.id,
                  "questions": formatted_questions,
                  "total_questions": len(formatted_questions)
              })
      except:
          print(sys.exc_info())
          abort(422)
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  # TODO Implemented in the /question POST method endpoint above
  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_categorie_questions(category_id):
      try:
          questions = Question.query.filter_by(category=category_id).all()
          formatted_questions = paginate_questions(request, questions)
          return jsonify({"questions": formatted_questions})
      except:
          print(sys.exc_info())
          abort(422)
  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
      try:
          body = request.get_json()
          print(body)
          previous_questions = body.get('previous_questions', None)
          quiz_category = body.get('quiz_category', None)
          if (quiz_category == None):
              abort(422)

          # return a random question 
          # when there is a previous questions
          if (previous_questions != None and len(previous_questions) != 0):
              print('Category choose: {}'.format(quiz_category))
              if (quiz_category['type'] == 'click'):
                  questions = Question.query.all()
              elif (quiz_category['type'] == 'Science'):
                  questions = Question.query.filter_by(category=1).all()
              elif (quiz_category['type'] == 'Art'):
                  questions = Question.query.filter_by(category=2).all()
              elif (quiz_category['type'] == 'Geography'):
                  questions = Question.query.filter_by(category=3).all()
              elif (quiz_category['type'] == 'History'):
                  questions = Question.query.filter_by(category=4).all()
              elif (quiz_category['type'] == 'Entertainment'):
                  questions = Question.query.filter_by(category=5).all()
              elif (quiz_category['type'] == 'Sports'):
                  questions = Question.query.filter_by(category=6).all()
              
              for question in questions[:]:
                  for id in previous_questions:
                      if question.id == id:
                          questions.remove(question)
              print('Questions: {}'.format(questions)) 
              if len(questions) == 0:
                  return jsonify({
                      "question": False
                  })
              else:
                  random_question = questions[random.randint(0, len(questions) - 1)].format()
                  print('Random Question'.format(random_question))
              return jsonify({
                  "question": random_question
              })
            # no previous questions
          else:
              print('\n\n No Previous \n\n')
              print(quiz_category)
              print('Category choose: {}'.format(quiz_category['type']))
              if (quiz_category['type'] == 'click'):
                  print('Getting all categories')
                  questions = Question.query.all()
              elif (quiz_category['type'] == 'Science'):
                  print('Getting Science Category')
                  questions = Question.query.filter_by(category=1).all()
              elif (quiz_category['type'] == 'Art'):
                  print('Getting Art Category')
                  questions = Question.query.filter_by(category=2).all()
              elif (quiz_category['type'] == 'Geography'):
                  print('Getting Geography Category')
                  questions = Question.query.filter_by(category=3).all()
              elif (quiz_category['type'] == 'History'):
                  print('Getting History Category')
                  questions = Question.query.filter_by(category=4).all()
              elif (quiz_category['type'] == 'Entertainment'):
                  print('Getting Entertainment Category')
                  questions = Question.query.filter_by(category=5).all()
              elif (quiz_category['type'] == 'Sports'):
                  print('Getting Sports Category')
                  questions = Question.query.filter_by(category=6).all()
              if len(questions) == 0:
                  return jsonify({
                      "question": False
                  })
              random_question = questions[random.randint(0, len(questions) - 1)].format()
              return jsonify({
                  "question": random_question
              })
      except: 
          print(sys.exc_info())
          abort(422)
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          "success": False,
          "error": 404,
          "message": "Not Found"
      }), 404
  
  @app.errorhandler(422)
  def unprocessable_entity(error):
      return jsonify({
          "success": False,
          "error": 422,
          "message": "Unprocessable Entity"
      }), 422
  @app.errorhandler(405)
  def method_not_allowed(error):
      return jsonify({
          "success": False,
          "error": 405,
          "message": "Method Not Allowed"
      })
  return app

    