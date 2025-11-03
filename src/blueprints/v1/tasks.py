from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_openapi3 import APIBlueprint, Tag

from src.errors.errors import ValidationError
from src.queries.list_tasks_query import list_tasks_for_user
from src.queries.get_task_query import get_task_for_user
from src.commands.create_task_command import create_task as create_task_cmd
from src.commands.update_task_command import update_task as update_task_cmd
from src.commands.delete_task_command import delete_task as delete_task_cmd

tasks_tag = Tag(name="Tasks", description="CRUD operations for tasks")

api_v1_tasks = APIBlueprint("tasks", __name__, url_prefix="/v1")


@api_v1_tasks.get("/tareas", tags=[tasks_tag])
@jwt_required()
def list_tasks():
    """
    List tasks for the authenticated user
    ---
    Returns: 200 with a list of tasks belonging to the requester
    """
    user_id = get_jwt_identity()
    tasks = list_tasks_for_user(user_id)
    return jsonify([t.to_dict() for t in tasks]), 200


@api_v1_tasks.get("/tareas/<int:task_id>", tags=[tasks_tag])
@jwt_required()
def get_task(task_id: int):
    """
    Get a single task by id for the authenticated user
    ---
    Returns: 200 with the task or 404 if not found
    """
    user_id = get_jwt_identity()
    task = get_task_for_user(user_id, task_id)
    return jsonify(task.to_dict()), 200


@api_v1_tasks.post("/tareas", tags=[tasks_tag])
@jwt_required()
def create_task():
    """
    Create a new task for the authenticated user
    ---
    Request JSON: {"title": str, "description": str?, "completed": bool?}
    Returns: 201 with created task
    """
    user_id = get_jwt_identity()
    payload = request.get_json(silent=True) or {}
    title = (payload.get("title") or "").strip()
    description = payload.get("description")
    completed = bool(payload.get("completed", False))

    if not title:
        raise ValidationError({"title": "required"})

    task = create_task_cmd(user_id=user_id, title=title, description=description, completed=completed)
    return jsonify(task.to_dict()), 201


@api_v1_tasks.put("/tareas/<int:task_id>", tags=[tasks_tag])
@jwt_required()
def update_task(task_id: int):
    """
    Update fields of a task for the authenticated user
    ---
    Request JSON: {"title"?: str, "description"?: str, "completed"?: bool}
    Returns: 200 with updated task or 404 if not found
    """
    user_id = get_jwt_identity()
    payload = request.get_json(silent=True) or {}
    task = get_task_for_user(user_id, task_id)

    if "title" in payload:
        title = (payload.get("title") or "").strip()
        if not title:
            raise ValidationError({"title": "cannot be empty"})
        payload["title"] = title
    updated = update_task_cmd(task, payload)
    return jsonify(updated.to_dict()), 200


@api_v1_tasks.delete("/tareas/<int:task_id>", tags=[tasks_tag])
@jwt_required()
def delete_task(task_id: int):
    """
    Delete a task for the authenticated user
    ---
    Returns: 200 with deletion confirmation or 404 if not found
    """
    user_id = get_jwt_identity()
    task = get_task_for_user(user_id, task_id)
    delete_task_cmd(task)
    return jsonify({"deleted": True, "id": task_id}), 200
