# Getting Started
### Pre-requisites and Local Development
Developers using this project should already have Python3, pip and node installed on their local machines. Before installing the requirements, be sure to create a virtual env in the root repository. Instructions on how to do so for your respective operating system, can be found at the link (https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
##Backend
From the backend folder run


`pip install requirements.txt.` 

All required packages are included in the requirements file.
To run the application run the following commands:


`export FLASK_APP=flaskr`


`export FLASK_ENV=development`


`flask run`


These commands put the application in development and directs our application to use the __init__.py file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the Flask documentation.
The application is run on http://127.0.0.1:5000/ by default and is a proxy in the frontend configuration.

## Testing

Prior to running the test suite, visitors should have PostrgeSQL installed on their local machines. Two databases will need to be constructed. 

- trivia
- trivia_test

From the /backend directory, the test suite can be run using the following commands:


`dropdb trivia_test`


`createdb trivia_test`


`psql trivia_test < trivia.psql`


`python -m unittest discover -s .`



The first time you run the tests, omit the dropdb command

## API Reference

**METHOD** | **ENDPOINT** | **RESPONSE**
--- | --- | ---
**GET** | /categories | `{categories: {1: "Science",2: "Art",3: "Geography",4: "History",5: "Entertainment",6: "Sports"},success: true}`
**GET** | /questions | `{categories: {1: 'Science', 2: 'Art', ...},current_category: null,questions: [{answer: 'Apollo 13', category: 5, difficulty: 4, id: 2, question: 'What movie earned Tom Hanks his third straight Oscar nomination, in 1996?}, ...], success: True, total_questions: 20}`
**DELETE** | /questions/<int:question_id> | `{"success": True, "deleted": 4, "questions": [{answer: 'Apollo 13',category: 5, difficulty: 4, id: 2, question: 'What movie earned Tom Hanks his third straight Oscar nomination, in 1996?}, ...], "total_questions": 19}`
**POST** - create a new question | /questions - The request should be sent with a body of: `{question: '', answer: '', category: int, difficulty: int}` | `{"success": True, "id": 12, "question": "How many NBA ....", "answer": "Six", "category": 6, "difficulty": 2, "questions": [{question: '',answer: ''}, ... ], "total_questions": 20}`
**POST** - search for question | /questions - The request should be sent with a body of: `{searchTerm: ""}` | `{"success": True, "questions": [{question: '', answer: ''}, ...], "total_questions": 4}`
**GET** | /category/<int:category_id>/questions | `{"success": True, "questions": [{question: '',answer: ''}, ... ], "total_questions": 10,"current_category": 1}`
**POST** | /quizzes - The request should be sent with a body of: `{current_category: 4, previous_questions: [20, 12]}` | `{ "success": True, "question": {question: 'How many times..., answer: '', difficulty: ...}}`

