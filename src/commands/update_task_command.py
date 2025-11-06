from typing import Dict, Any

from src.config.extensions import db
from src.models.task import Task
from src.errors.errors import ValidationError


def update_task(task: Task, updates: Dict[str, Any]) -> Task:
    # Validate title at use-case level if present
    if "title" in updates:
        title = (updates.get("title") or "")
        title = title.strip()
        if not title:
            raise ValidationError({"title": "cannot be empty"})
        updates["title"] = title

    if "title" in updates:
        task.title = updates["title"]
    if "description" in updates:
        task.description = updates["description"]
    if "completed" in updates:
        task.completed = bool(updates["completed"])
    db.session.commit()
    return task
