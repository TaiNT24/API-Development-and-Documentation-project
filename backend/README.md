# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Documenting your Endpoints

### Documentation

`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

---
`GET '/questions'`

- Get list of question (maximum 10 questions/page) and total questions, dictionary of categories
- Request Arguments: None
- Returns:

```json
{
    "total_questions": 16,
    "questions": [
      {
        "id": 1,
        "question": "Question",
        "answer": "Answer",
        "category": 1,
        "difficulty": 1
      },
      ...
    ],
    "categories": {
          "1": "Science",
          "2": "Art",
          "3": "Geography",
          "4": "History",
          "5": "Entertainment",
          "6": "Sports"
    },
    "current_category": "Science"
}
```

---
`DELETE '/questions/<int:question_id>'`

- Delete a question by id
- Request Arguments: question_id: id of the question
- Returns:

If the id of question is exist
```json
{
    "success": true,
    "message": "Success"
}
```
If the id of question is not exist
```json
{
    "success": false,
    "error": 404,
    "message": "Not found"
}
```

---
`POST '/questions'`

- Add new question
- Request Arguments: 

```json
{
    "question": "Question",
    "answer": "Answer",
    "category": 1,
    "difficulty": 1
}
```

- Returns:

```json
{
    "success": true,
    "message": "Success"
}
```


---
`POST '/questions/search'`

- Search questions
- Request Arguments: 

```json
{
    "searchTerm": "Search text"
}
```

- Returns:

```json
{
  "total_questions": 12,
  "questions": [
    {
        "id": 1,
        "question": "Question",
        "answer": "Answer",
        "category": 1,
        "difficulty": 1
    },
    ...
  ],
  "current_category": "Science"
}
```


---
`GET '/categories/<int:category_id>/questions'`

- Get a question by category id
- Request Arguments: category_id: id of the category
- Returns:

```json
{
  "total_questions": 12,
  "questions": [
    {
        "id": 1,
        "question": "Question",
        "answer": "Answer",
        "category": 1,
        "difficulty": 1
    },
    ...
  ],
  "current_category": "Science"
}
```


---
`POST '/quizzes'`

- Play quizzes
- Request Arguments: 

```json
{
    "previous_questions": [1,2],
    "quiz_category": {
      "id": 1,
      "type": "Science"
    }
}
```

- Returns:

```json
{
  "question": {
    "id": 1,
    "question": "Question",
    "answer": "Answer",
    "category": 1,
    "difficulty": 1
  }
}
```


## Testing

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
