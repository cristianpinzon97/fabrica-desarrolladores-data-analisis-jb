from src.extensions import db
from src.models.task import Task


def create_task(user_id: int, title: str, description=None, completed: bool = False) -> Task:
    task = Task(title=title, description=description, completed=completed, user_id=user_id)
    db.session.add(task)
    db.session.commit()
    return task


