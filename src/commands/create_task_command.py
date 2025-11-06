from src.config.extensions import db
from src.models.task import Task
from src.errors.errors import ValidationError


def create_task(user_id: int, title: str, description=None, completed: bool = False) -> Task:
    # validate title at usecase level
    title = (title or "") if title is not None else ""
    title = title.strip()
    if not title:
        raise ValidationError({"title": "required"})

    task = Task(title=title, description=description, completed=completed, user_id=user_id)
    db.session.add(task)
    db.session.commit()
    return task
