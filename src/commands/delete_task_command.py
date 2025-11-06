from src.config.extensions import db
from src.models.task import Task


def delete_task(task: Task) -> None:
    db.session.delete(task)
    db.session.commit()


