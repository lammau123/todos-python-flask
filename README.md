# Create a Simple RESTful API for a Todo List

## Objective: 
Develop a RESTful API that manages a simple todo list. The API should allow clients to create, read, update, and delete (CRUD) todo items. The data should be stored in memory (i.e., not persist beyond the runtime of the application).

## Requirements:
Single File: All code (including the server, routes, and in-memory data storage) must be contained within a single file, server.py.
Endpoints:
- GET /todos: Retrieve a list of all todo items.
- GET /todos/:id: Retrieve a specific todo item by its ID.
- POST /todos: Create a new todo item. The request body should contain the task description and its status (e.g., {"task": "Buy groceries", "completed": false}).
- PUT /todos/:id: Update an existing todo item by its ID. The request body should allow updating the task description and/or its status.
- DELETE /todos/:id: Delete a specific todo item by its ID.
## In-Memory Storage:
Store the todo items in memory using an array or a similar data structure.
Each todo item should have a unique ID, a task description, and a completed status (true/false).
## Validation:
Ensure that all required fields are provided and valid when creating or updating a todo item.
Handle errors gracefully, returning appropriate HTTP status codes and error messages.
## Language and Framework:
Flask python

The solution must be self-contained and executable as a single script.