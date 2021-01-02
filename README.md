# Trivia API 
author: Joseph Mugo
email: joemu18@gmail.com
github: https://github.com/JosephMugo

Backend code follows: [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/)

## Getting Started
> Base Url: http://localhost:5000/ <b><i>(ran locally)</i></b>

> API Keys/Authentication: N/A
### Pre-requisites and Local Development
<b>Required</b>:
- python3
- pip
- node
#### backend
default port: `http://127.0.0.1:5000/`
##### running backend:
> set FLASK_APP = flaskr
> set FLASK_ENV=development  
> <b>flask run</b>  <i>#starts backend server</i>
#### frontend
defulat port: `http://127.0.0.1:3000`
##### running frontend:
> npm install 
> npm start <i>#starts frontend server<i/>

## Error 
#### 404 
response: `{
"success": False,
"error": 404,
"message": "Not Found"
}`
#### 422
response: `{
"success": False,
"error": 422,
"message": "Unprocessable Entity"}`
#### 405
response: `{
"success": False,
"error": 405,
"message": "Method Not Allowed"}`
## Endpoints

| Method     | Path| Info     | Parameters | Sample Request |Sample Result | 
| :---        |    :----:   |           :----:   |           :----:   |           :----:   |          ---: |
| GET | /categories | retrieves all categories   | N/A |`curl -X GET http://127.0.0.1:5000/categories`| `{ "categories": ["Science", "Art", "Geography", "History", "Entertainment", "Sports"], "success": true}` 
| GET | /questions  | retrieves paginated list of questions (10 questions) | N/A |`curl -X GET http://127.0.0.1:5000/questions`| `{"categories": ["Science", "Art", "Geography", "History", "Entertainment", "Sports"], "questions": [{"answer": "Earth", "category": 1, "difficulty": 1, "id": 1, "question": "What planet do we live on?"},{"answer": "Moon", "category": 1, "difficulty": 1, "id": 2, "question": "What rotates around the earth?"}]}`
| DELETE | /questions/<<i>question_id<i>> | delete question with id specifid <<i>question_id<i>> | <i>question_id<i> |`curl -X DELETE http://127.0.0.1:5000/questions/2`|`{"deleted": 2, "questions": [{"answer": "Earth", "category": 1, "difficulty": 1, "id": 1, "question": "What planet do we live on?"}], "success": true, "total_questions": 1}`
| POST | /questions | adds new question | <i>question(String), answer(String), difficulty(int), category(int)<i> |`curl -X POST -d "{\"question\": \"What planet do we live in?\", \"answer\": \"Earth\", \"difficulty\": 1, \"category\": 1}" -H "Content-Type: application/json" http://127.0.0.1:5000/questions`| `{"question_created: 1, "questions": [{"answer": "Apple", "category": 1, "difficulty": 1, "id": 3, "question": "What fruit starts with an A?"},{"answer": "Earth", "category": 1, "difficulty": 1, "id": 1, "question": "What planet do we live on?"}]}`
| POST |/questions|search for questions based on <i>searchTerm<i> in body| <i>searchTerm<i> |`curl -d "{\"searchTerm\": \"what\"}" -H "Content-Type: application/json" http://127.0.0.1:5000/questions`|<i>searchTerm: planet<i> `"questions": [{"answer": "Earth", "category": 1, "difficulty": 1, "id": 1, "question": "What planet do we live on?"}], "success": true, "total_questions": 1`|
| GET | /categories/<i>category_id<i>/questions |  retrieves questions based on category <<i>category_id<i>> | <i>category_id<i> |`curl http://127.0.0.1:5000/categories/1/questions`|`{questions": [{"answer": "Apple", "category": 1, "difficulty": 1, "id": 3, "question": "What fruit starts with an A?"},{"answer": "Earth", "category": 1, "difficulty": 1, "id": 1, "question": "What planet do we live on?"}]}`
| POST | /quizzes | retrieve random question based on <i>quiz_category['type']<i> and excludes questions based on <i>previous_questions<i> containing question ids| <i>previous_question(list of integers), quiz_category(object with property type(String) and id(int))<i> |`curl -d "{\"previous_question\": [], \"quiz_category\": {\"type\": \"History\", \"id\": 3}}" -H "Content-Type: application/json" http://127.0.0.1:5000/quizzes`|`{"question": {"answer": "Muhammad Ali", "category": 4, "difficulty": 1, "id": 9, "question": "What boxer's original name is Cassius Clay?"}}` <i><b>or when no questions</b><i>: `{ "question": false }`
