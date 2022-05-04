import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def pagination(request, selected_questions):
    
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selected_questions]
    current_questions = questions[start:end]
    
    return current_questions

def show_form_errors(fieldName, errorMessages):
    return flash(
        'Some errors on ' +
        fieldName.replace('_', ' ') +
        ': ' +
        ' '.join([str(message) for message in errorMessages]),
        'warning'
    )


def create_app(test_config=None):
  app = Flask(__name__)
  setup_db(app)
 # CORS(app, resources={r"*/api/*" : {"origins": '*'}})
  CORS(app)

  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
      response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTION')
      return response


    

  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs -done
  '''
  
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow -done
  '''


  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
   
    categories = Category.query.all()
    
    categoriesdic = {}
    for category in categories:
        categoriesdic[category.id] = category.type

    if (len(categoriesdic) == 0):
            abort(404)

    return jsonify({
            'success': True,
            'categories': categoriesdic
      })





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
  @app.route('/questions')
  def get_questions():
        try:
            
            selected_questions = Question.query.all()
            totalQuestions = len(selected_questions)
            currentQuestions = pagination(request, selected_questions)

            if (len(currentQuestions) == 0):
                abort(404)

            categories = Category.query.all()
            # categoriesdic = {}
            # for category in categories:
            #     categoriesdic[category.id] = category.type
            

            return jsonify({
                'success': True,
                'questions': currentQuestions,
                'total_questions': totalQuestions,
                'categories': {category.id: category.type for category in categories}
            })
        except Exception as e:
            print(sys.exc_info())
            print(e)
            abort(404)



  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:id>', methods=['DELETE'])
  def delete_question(id):
        try:
            question = Question.query.filter_by(id=id).one_or_none()
          
            if question is None:
                abort(404)

            question.delete()
            
            selected_questions = Question.query.order_by(Question.id).all()
            currentQuestions = pagination(request, selected_questions)

            return jsonify({
                'success': True,
                'deleted':id
                
            })

        except Exception as e:
            print(e)
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
  @app.route("/questions", methods=['POST'])
  def createnew_question():
        
        body = request.get_json()
        if not ('question' in body and 'answer' in body and 'category' in body and 'difficulty' in body
            and body.get('question') != '' and body.get('answer') != '' and body.get('category') != '' and body.get('difficulty') != ''):
            abort(422)

        try:
            
            question = Question(question=body.get('question', None), answer=body.get('answer', None),
                                category=body.get('category', None), difficulty=body.get('difficulty', None))
            question.insert()

            
            selected_questions = Question.query.order_by(Question.id).all()
            currentQuestions = pagination(request, selected_questions)

            return jsonify({
                'success': True,
                'created': question.id,
                'questions': currentQuestions,
                'total_questions': len(selected_questions)
            })

        except Exception as e:
            print(e)
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
  @app.route("/questions/search", methods=['POST'])
  def search():
        body = request.get_json()
        searchitem = body.get('searchTerm')
        questions = Question.query.filter(
            Question.question.ilike('%'+searchitem+'%')).all()

        if questions:
            currentQuestions = pagination(request, questions)
            return jsonify({
                'success': True,
                'questions': currentQuestions,
                'total_questions': len(questions)

            })
        else:
            abort(404)



  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route("/categories/<int:id>/questions")
  def questions_in_selectedcategory(id):
        
        category = Category.query.filter_by(id=id).one_or_none()
        if category:
           
            questionsInCat = Question.query.filter_by(category=str(id)).all()
            currentQuestions = pagination(request, questionsInCat)

            return jsonify({
                'success': True,
                'questions': currentQuestions,
                'total_questions': len(questionsInCat),
                'current_category': category.type
            })
        
        else:
            abort(404)



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
  def get_quizzes():
        
        try:
            body = request.get_json()
            previous_questions = body.get('previous_questions', None)
            quiz_category = body.get('quiz_category', None)
            category_id = quiz_category['id']

            if category_id == 0:
                questions = Question.query.filter(
                    Question.id.notin_(previous_questions)).all()
            else:
                questions = Question.query.filter(
                    Question.id.notin_(previous_questions),
                    Question.category == category_id).all()
            question = None
            if(questions):
                question = random.choice(questions)

            return jsonify({
                'success': True,
                'question': question.format()
            })

        except Exception:
            abort(404)
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  def bad_request(error):
        return jsonify({
            "success": False,
            'error': 400,
            "message": "Bad request"
        }), 400

  @app.errorhandler(404)
  def page_not_found(error):
        return jsonify({
            "success": False,
            'error': 404,
            "message": "Page not found"
        }), 404

  @app.errorhandler(422)
  def unprocessable_recource(error):
        return jsonify({
            "success": False,
            'error': 422,
            "message": "Unprocessable resource"
        }), 422

  @app.errorhandler(500)
  def internal_server_error(error):
        return jsonify({
            "success": False,
            'error': 500,
            "message": "Internal server error"
        }), 500

  @app.errorhandler(405)
  def invalid_method(error):
        return jsonify({
            "success": False,
            'error': 405,
            "message": "Method not allowed!"
        }), 405

  
  return app

    