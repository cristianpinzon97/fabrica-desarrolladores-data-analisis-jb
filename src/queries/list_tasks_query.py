from typing import List

from src.models.task import Task


def list_tasks_for_user(user_id: int) -> List[Task]:
    return Task.query.filter_by(user_id=user_id).order_by(Task.id.desc()).all()


