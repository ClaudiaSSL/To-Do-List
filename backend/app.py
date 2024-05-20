from flask import Flask, jsonify, request, Response
from flask_cors import CORS, cross_origin
from db_utils import DBquery
from models import Task



# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

if __name__ == '__main__':
    app.run()

if not DBquery('tasks.db').check_if_table_exists():
    DBquery('tasks.db').create_table()


@app.route('/tasks', methods=['GET', 'POST'])
def all_tasks() -> Response:
    response_object = {'status': 'success'}
    db=DBquery('tasks.db')
    if request.method == 'POST':
        post_data = request.get_json()
        description = post_data.get('description')
        about = post_data.get('for')
        done = post_data.get('done')
        db.add((description, about, done), 'tasks')   
        response_object['message'] = 'Task added!'
    else:
        data=list(db.fetch_all(Task, 'tasks'))
        response_object['tasks'] = data
    db.close()
    return jsonify(response_object)

@app.route('/autocomplete', methods=['POST'])
def all_autocomplete() -> Response:
    response_object = {'status': 'success'}
    db=DBquery('tasks.db')
    post_data = request.get_json()
    data = list(db.autocomplete(post_data.get('table'), post_data.get('column'), post_data.get('value')))
    temp=[]
    for item in data:
        if item not in temp:
            temp.append(item)
    response_object['autocomplete'] = temp
    db.close()
    return jsonify(response_object)


@app.route('/tasks/<int:task_id>', methods=['PUT', 'DELETE'])
@cross_origin()
def single_task(task_id:int) -> Response:
    response_object = {'status': 'success'}
    db=DBquery('tasks.db')
    if request.method == 'PUT':
        post_data = request.get_json()
        data = (
            post_data.get('description'),
            post_data.get('for'),
            post_data.get('done'),
            post_data.get('id')
        )
        db.update(data, 'tasks')
        response_object['message'] = 'Task updated!'
    if request.method == 'DELETE':
        db.delete(task_id, 'tasks')
        response_object['message'] = 'Task removed!'
    db.close()
    return jsonify(response_object)