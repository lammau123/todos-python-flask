import logging
from flask import Flask, jsonify, request
import hashlib
import time

# Configure logging with timestamp
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Generate id for todo
def generate_id():
    return hashlib.md5(str(time.time()).encode()).hexdigest()

# Create todo object
def create_todo_object(task, completed):
    return { "id": generate_id(), "task": task, "completed": completed }
   
# validate data based on field and rules in fields param 
def validate_fields(data, fields):
    errors = {}
    for field, rules in fields.items():
        value = data.get(field)
        if value is None and rules.get('required', False):
            errors[field] = 'Field is required'
        else:
            if 'min_length' in rules and len(value) < rules['min_length']:
                errors[field] = f'Minimum length is {rules["min_length"]}'
            if 'max_length' in rules and len(value) > rules['max_length']:
                errors[field] = f'Maximum length is {rules["max_length"]}'
    return errors

# decorator factory
def validate_todo_middleware(fields):
    def decorator(f):   
        def wrapper(*args, **kwargs):
            data = request.get_json()
            if not data:
                logging.error(f"validation failed with empty data in request body.")
                return jsonify({"error": "Invalid data"}), 400
            errors = validate_fields(data, fields)
            if errors:
                logging.error(f"validation failed with error {errors}.")
                return jsonify(errors), 400
            return f(*args, **kwargs)
        return wrapper
    return decorator

todo_list = [ 
    create_todo_object("Buy groceries", False),
    create_todo_object("Buy meat", False),
    create_todo_object("Buy a bottle of water", False)
]

app = Flask(__name__)

@app.get('/todos')
def get_todos():
    """
    Retrieve a list of all todo items.

    Returns:
        list: A list of todo items.
    """
    logging.info(f"Queried all todo item list successfully.")
    return jsonify(todo_list), 200

@app.get('/todos/<id>')
def get_todo(id):
    """
    Retrieve a specific todo item by its id.

    Args:
        id (str): The id of the todo item.

    Returns:
        dict: A JSON object representing the todo item.
        HTTP Status Code 200: Indicates that the todo item was found.
        HTTP Status Code 404: Indicates that the todo item was not found.
    """
    todo = next((item for item in todo_list if item['id'] == id), None)
    if todo is None:
        logging.error(f"Todo item with id {id} not found.")
        return jsonify({"error": "Todo item not found"}), 404
    logging.info(f"Todo item with id {id} found.")
    return jsonify(todo), 200

@app.post('/todos', endpoint='create_todo_post')
@validate_todo_middleware({
    'task': {'min_length': 3, 'max_length': 255},
    'completed': {'required': True}
})
def create_todo(): 
    """
    Create a new todo item.

    This endpoint accepts a JSON payload with 'title' and 'description' fields,
    validates the input, creates a new todo item, and returns the created item.

    Returns:
        dict: A JSON object representing the newly created todo item.
        HTTP Status Code 201: Indicates that the todo item was successfully created.
        HTTP Status Code 400: Indicates that the input data is invalid.
    """
    data = request.get_json()
    todo = create_todo_object(data['task'], data['completed'])
    todo_list.append(todo)
    logging.info(f"Todo item with id {todo['id']} created successfully.")
    return jsonify(todo), 201

@app.put('/todos/<id>', endpoint='update_todo_put')
@validate_todo_middleware({
    'task': {'min_length': 3, 'max_length': 255},
    'completed': {'required': True}
})
def update_todo(id):
    """
    Update an existing todo item by its id.

    This endpoint accepts a JSON payload with 'task' and 'status' fields,
    validates the input, updates the todo item, and returns the updated item.

    Args:
        id (str): The id of the todo item to update.

    Returns:
        dict: A JSON object representing the updated todo item.
        HTTP Status Code 200: Indicates that the todo item was successfully updated.
        HTTP Status Code 400: Indicates that the input data is invalid.
        HTTP Status Code 404: Indicates that the todo item was not found.
    """
    data = request.get_json()

    todo = next((item for item in todo_list if item['id'] == id), None)
    if todo is None:
        logging.error(f"Todo item with id {id} not found.")
        return jsonify({"error": "Todo item not found"}), 404

    todo['task'] = data['task']
    todo['completed'] = data['completed']
    logging.info(f"Todo item with id {id} updated successfully.")
    return jsonify(todo), 200
    
@app.delete('/todos/<id>')
def delete_todo(id):
    """
    Delete a specific todo item by its id.

    Args:
        id (str): The id of the todo item to delete.

    Returns:
        dict: A JSON object with a success message.
        HTTP Status Code 200: Indicates that the todo item was successfully deleted.
        HTTP Status Code 404: Indicates that the todo item was not found.
    """
    todo = next((item for item in todo_list if item['id'] == id), None)
    if todo is None:
        logging.error(f"Todo item with id {id} not found.")
        return jsonify({"error": "Todo item not found"}), 404

    todo_list.remove(todo)
    logging.info(f"Todo item with id {id} deleted successfully.")
    return jsonify({"message": "Todo item deleted successfully"}), 200