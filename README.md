# practical-multiminds

## Steps to run the project

- Create virtual environment [env]
- To install necessary dependancy run `pip install -r requirements.txt` command.
- Create task database in pgadmin.
- Run `python manage.py makemigrations` command.
- Run `python manage.py migrate` command.
- Run the project with `python manage.py runserver` command.

# For API documentation :

- http://127.0.0.1:8000/swagger/
- http://127.0.0.1:8000/redoc/

## API Endpoints

# User Authentication

Endpoint: api/register/
Method:POST
description: Register User.
Request Example:
{
"username": "test_user",
"email": "testuser@gmail.com",
"phone_number": "123456789",
"password": "Test@123",
"role": "admin"
}

Endpoint: api/login/
Method:POST
Description: Login with email and password.
Request Example:
{
"password": "Test@123",
"email": "testuser@gmail.com"
}

Response:
{
"token": "8787b7898990ksjdksjekeuriergtrkgj"
}

Endpoint: api/password-reset/
Method: PUT/PATCH
Description: Reset the password.
Authentication Header: {Authorization: Token " "}
Request Example:
{
"password": "test"
}

Endpoint: api/user-list
Method: GET
Description: Get the list of users (only admin user have permission to perform this request)

# Task Management

Endpoint: api/tasks/
Method: POST
Description: New task Created by the authenticated user (only admin user have permission to perform this request).
Authentication Header: {Authorization: Token " "}
Request Example:
{
"title": "task4",
"description": "task description",
"due_date": "2024-10-10",
"priority": "low",
"complete_status": "todo",
"assigned_to": "2"
}

Endpoint: api/tasks
Method: GET
Description: List all tasks which is created by logged-in user/assigned_to is logged-in user.
Authentication Header: {Authorization: Token " "}
Query Parameters:
search="task"

- api/tasks?search="task"

Endpoint: api/tasks/{id}/
Method: GET
Description: Retrive task with id by the authenticated user created by logged-in user/assigned_to is logged-in user.
Authentication Header: {Authorization: Token " "}

Endpoint: api/tasks/{id}/
Method: PATCH
Description: Partially Update task with id if created by logged-in user/assigned_to is logged-in user.
Authentication Header: {Authorization: Token " "}
Request Example:
{
"priority": "medium",
"complete_status": "inprogress"
}

Endpoint: /tasks/{id}/
Method: DELETE
Description: Delete a task with id if created by logged-in user/assigned_to is logged-in user.
Authentication Header: {Authorization: Token " "}

# Collaboration

Endpoint: api/tasks/{task_id}/comments/
Method: GET
Description: List all comments for a task by the authenticated user.
Authentication Header: {Authorization: Token " "}

Endpoint: api/tasks/{task_id}/comments/
Method: POST
Description: Create a new comment on a task.
Authentication Header: {Authorization: Token " "}
Request Example:
{
"content" : "New Comment"
}

Endpoint: api/tasklists/
Method: GET
Description: List all task lists (public and owned by the user).
Authentication Header: {Authorization: Token " "}
Query params:
"search"="task_name"

- api/tasklists/?search="task_name"

Endpoint: api/tasklists/
Method: POST
Description: Create a new task list.
Authentication Header: {Authorization: Token " "}
Request Example:
{
"name": "Task List",
"is_public": "True",
"tasks": [2,1]
}

Endpoint: GET /tasklists/{id}/:
Method: GET
Description: Retrieve a specific task list (public and owned by the user).
Authentication Header: {Authorization: Token " "}

Endpoint: /tasklists/{id}/
Method: PATCH
Description: Partially update a task list (public and owned by the user).
Authentication Header: {Authorization: Token " "}
Request Example:
{

}

Endpoint: /tasklists/{id}/
Method: DELETE
Description: Delete a task list (public and owned by the user).
Authentication Header: {Authorization: Token " "}
