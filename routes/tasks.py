from flask import Blueprint, request, jsonify
from models import Task
from extension import db
from middleware import token_required

tasks = Blueprint('tasks', __name__)


@tasks.route('/tasks', methods=['POST'])
@token_required
def create_task(current_user):
    data = request.get_json()
    new_task = Task(
        title=data.get('title'),
        description=data.get('description'),
        user_id=current_user.id
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Task created successfully'}), 201


@tasks.route('/tasks', methods=['GET'])
@token_required
def fetch_all_tasks(current_user):
    all_tasks = Task.query.filter_by(user_id=current_user.id).all()
    return jsonify([task.to_dict() for task in all_tasks]), 200


@tasks.route('/tasks/<int:id>', methods=['GET'])
@token_required
def fetch_specific_task(current_user, id):
    task = Task.query.filter_by(id=id, user_id=current_user.id).first()
    if not task:
        return jsonify({'message': 'Task not found'}), 404
    return jsonify(task.to_dict()), 200


@tasks.route('/tasks/<int:id>', methods=['PUT'])
@token_required
def update_task(current_user, id):
    task = Task.query.filter_by(id=id, user_id=current_user.id).first()
    if not task:
        return jsonify({'message': 'Task not found'}), 404
    data = request.get_json()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    db.session.commit()
    return jsonify(task.to_dict()), 200


@tasks.route('/tasks/<int:id>', methods=['DELETE'])
@token_required
def delete_task(current_user, id):
    task = Task.query.filter_by(id=id, user_id=current_user.id).first()
    if not task:
        return jsonify({'message': 'Task not found'}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'}), 200


@tasks.route('/tasks/<int:id>/done', methods=['PATCH'])
@token_required
def mark_done(current_user, id):
    task = Task.query.filter_by(id=id, user_id=current_user.id).first()
    if not task:
        return jsonify({'message': 'Task not found'}), 404
    task.is_done = True
    db.session.commit()
    return jsonify(task.to_dict()), 200