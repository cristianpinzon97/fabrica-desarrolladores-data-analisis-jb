from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_openapi3 import APIBlueprint, Tag

from src.errors.errors import ValidationError
from src.extensions import db
from src.models import Task

tasks_tag = Tag(name="Tasks", description="CRUD operations for tasks")

api_v1_tasks = APIBlueprint("tasks", __name__, url_prefix="/v1")


@api_v1_tasks.get("/tareas", tags=[tasks_tag])
@jwt_required()
def list_tasks():
    user_id = get_jwt_identity()
    tasks = Task.query.filter_by(user_id=user_id).order_by(Task.id.desc()).all()
    return jsonify([t.to_dict() for t in tasks]), 200


@api_v1_tasks.get("/tareas/<int:task_id>", tags=[tasks_tag])
@jwt_required()
def get_task(task_id: int):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if task is None:
        return jsonify({"msg": "task not found"}), 404
    return jsonify(task.to_dict()), 200


@api_v1_tasks.post("/tareas", tags=[tasks_tag])
@jwt_required()
def create_task():
    user_id = get_jwt_identity()
    payload = request.get_json(silent=True) or {}
    title = (payload.get("title") or "").strip()
    description = payload.get("description")
    completed = bool(payload.get("completed", False))

    if not title:
        raise ValidationError({"title": "required"})

    task = Task(title=title, description=description, completed=completed, user_id=user_id)
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201


@api_v1_tasks.put("/tareas/<int:task_id>", tags=[tasks_tag])
@jwt_required()
def update_task(task_id: int):
    user_id = get_jwt_identity()
    payload = request.get_json(silent=True) or {}
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if task is None:
        return jsonify({"msg": "task not found"}), 404

    if "title" in payload:
        title = (payload.get("title") or "").strip()
        if not title:
            raise ValidationError({"title": "cannot be empty"})
        task.title = title
    if "description" in payload:
        task.description = payload.get("description")
    if "completed" in payload:
        task.completed = bool(payload.get("completed"))

    db.session.commit()
    return jsonify(task.to_dict()), 200


@api_v1_tasks.delete("/tareas/<int:task_id>", tags=[tasks_tag])
@jwt_required()
def delete_task(task_id: int):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if task is None:
        return jsonify({"msg": "task not found"}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({"deleted": True, "id": task_id}), 200
