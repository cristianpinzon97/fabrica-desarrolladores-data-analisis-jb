from typing import Optional

from src.models import Task


def get_task_for_user(user_id: int, task_id: int) -> Optional[Task]:
    return Task.query.filter_by(id=task_id, user_id=user_id).first()


