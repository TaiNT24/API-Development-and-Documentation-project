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
        # response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Allow-Control-Allow-Credentials', 'true')

        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """

    @app.route('/messages')
    @cross_origin()
    def get_messages():
        return 'GETTING MESSAGES'

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

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route('/questions', methods=['POST'])
    @cross_origin()
    def search_questions():
        searchTerm = request.json.get('searchTerm', '')

        question_list = Question.query.filter(Question.question.ilike(f'%{searchTerm}%')).all()
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

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    return app

