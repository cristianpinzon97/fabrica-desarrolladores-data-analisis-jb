from src.extensions import db
from src.models import Task


def delete_task(task: Task) -> None:
    db.session.delete(task)
    db.session.commit()


