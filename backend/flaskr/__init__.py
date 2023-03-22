import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    cors = CORS(app, resources={r"/": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')

        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """

    @app.route('/categories', methods=['GET'])
    @cross_origin()
    def get_categories():
        categories_list = Category.query.all()

        categories_dict = {}
        for item in categories_list:
            categories_dict.update({
                item.id: item.type
            })

        return jsonify({
            'categories': categories_dict,
        })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route('/questions', methods=['GET'])
    @cross_origin()
    def get_questions_per_page():
        page = request.args.get('page', 1, int)
        limit = page * QUESTIONS_PER_PAGE
        offset = (page - 1) * QUESTIONS_PER_PAGE

        question_list = Question.query.limit(limit).offset(offset).all()
        total_count = Question.query.count()

        categories_list = Category.query.all()

        question_list = [ques.format() for ques in question_list]
        categories_dict = {}
        for item in categories_list:
            categories_dict.update({
                item.id: item.type
            })

        current_category = ''
        if len(question_list) > 0:
            categories = Category.query.filter(Category.id == question_list[0]['category']).first()
            if categories:
                current_category = categories.type

        return jsonify({
            'total_questions': total_count,
            'questions': question_list,
            'categories': categories_dict,
            'current_category': current_category,
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    @cross_origin()
    def delete_questions(question_id):

        deleted_question = Question.query.filter(Question.id == question_id).first()
        if deleted_question:
            deleted_question.delete()
        else:
            abort(404)

        return jsonify({
            "success": True,
            'message': 'Success'
        })

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    @app.route('/questions', methods=['POST'])
    @cross_origin()
    def post_new_questions():
        question = request.json.get('question', '')
        answer = request.json.get('answer', '')
        category = request.json.get('category', 0)
        difficulty = request.json.get('difficulty', 0)

        if not question or not answer or category == 0 or difficulty == 0:
            abort(422)

        new_question = Question(question, answer, category, difficulty)

        new_question.insert()

        return jsonify({
            "success": True,
            'message': 'Success',
        })

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route('/questions/search', methods=['POST'])
    @cross_origin()
    def search_questions():
        searchTerm = request.json.get('searchTerm', '').strip()

        question_list = Question.query.filter(Question.question.ilike(f'%{searchTerm}%')).limit(QUESTIONS_PER_PAGE).offset(0).all()
        total_count = Question.query.filter(Question.question.ilike(f'%{searchTerm}%')).count()

        current_category = ''
        question_list = [ques.format() for ques in question_list]

        if len(question_list) > 0:
            categories = Category.query.filter(Category.id == question_list[0]['category']).first()
            if categories:
                current_category = categories.type

        return jsonify({
            'total_questions': total_count,
            'questions': question_list,
            'current_category': current_category,
        })

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route('/categories/<int:category_id>/questions')
    @cross_origin()
    def get_questions_by_category(category_id):

        question_list = Question.query.filter(Question.category == category_id).all()
        total_count = Question.query.filter(Question.category == category_id).count()

        category = Category.query.filter(Category.id == category_id).first()

        question_list = [ques.format() for ques in question_list]
        current_category = ''
        if category:
            current_category = category.type

        return jsonify({
            'total_questions': total_count,
            'questions': question_list,
            'current_category': current_category,
        })

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route('/quizzes', methods=['POST'])
    @cross_origin()
    def get_quizzes():
        previous_questions = request.json.get('previous_questions', [])
        quiz_category = request.json.get('quiz_category', {})

        filter_condition = []
        if len(previous_questions) > 0:
            filter_condition.append(Question.id.notin_(previous_questions))
        if quiz_category.__len__() > 0:
            cate_id = quiz_category.get("id", 0)
            if cate_id != 0:
                filter_condition.append(Question.category == cate_id)

        first_quest = Question.query.filter(*filter_condition).first()

        return jsonify({
            'question': first_quest.format() if first_quest is not None else None,
        })

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 422

    return app

