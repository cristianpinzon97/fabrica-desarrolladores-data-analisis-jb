from typing import Dict, Any

from src.config.extensions import db
from src.models.task import Task


def update_task(task: Task, updates: Dict[str, Any]) -> Task:
    if "title" in updates:
        task.title = updates["title"]
    if "description" in updates:
        task.description = updates["description"]
    if "completed" in updates:
        task.completed = bool(updates["completed"])
    db.session.commit()
    return task


