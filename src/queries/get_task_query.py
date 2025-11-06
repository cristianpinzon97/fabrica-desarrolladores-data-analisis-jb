from src.errors.errors import NotFoundError
from src.models.task import Task


def get_task_for_user(user_id: int, task_id: int) -> Task:
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if task is None:
        raise NotFoundError("task not found")
    return task


