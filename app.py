from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, Task
from schemas import TaskCreate, TaskUpdate, TaskResponse, TaskListResponse
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/v1/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    try:
        task_data = TaskCreate(**data)
        task = Task(title=task_data.title, is_completed=task_data.is_completed)
        db.session.add(task)
        db.session.commit()
        return jsonify({"id": task.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/v1/tasks', methods=['GET'])
def list_tasks():
    tasks = Task.query.all()
    return jsonify(TaskListResponse(tasks=[task.to_dict() for task in tasks]).dict()), 200

@app.route('/v1/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = Task.query.get(id)
    if task:
        return jsonify(TaskResponse.from_orm(task).dict()), 200
    return jsonify({"error": "There is no task at that id"}), 404

@app.route('/v1/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return '', 204
    return jsonify({"error": "There is no task at that id"}), 404

@app.route('/v1/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get(id)
    if task:
        data = request.get_json()
        task.title = data.get("title", task.title)
        task.is_completed = data.get("is_completed", task.is_completed)
        db.session.commit()
        return '', 204
    return jsonify({"error": "There is no task at that id"}), 404

@app.route('/v1/tasks/bulk', methods=['POST'])
def bulk_add_tasks():
    data = request.get_json()
    tasks = data.get("tasks", [])
    new_tasks = []
    for task_data in tasks:
        task = Task(title=task_data['title'], is_completed=task_data.get('is_completed', False))
        new_tasks.append(task)
    db.session.bulk_save_objects(new_tasks)
    db.session.commit()
    return jsonify({"tasks": [{"id": task.id} for task in new_tasks]}), 201

@app.route('/v1/tasks/bulk', methods=['DELETE'])
def bulk_delete_tasks():
    data = request.get_json()
    task_ids = [task['id'] for task in data.get('tasks', [])]
    Task.query.filter(Task.id.in_(task_ids)).delete(synchronize_session=False)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
