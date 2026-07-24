"""Endpoint for task management."""

from typing import Optional

from sqlmodel import Session, select

from models.task import Task
from schemas.request.task import TaskCreate
from schemas.response.task import BaseTaskList, TaskList


def fetch_task_list(db_session: Session, search_title: Optional[str]) -> TaskList:
    """Fetch and return task lists."""

    task_list_query = select(Task.id, Task.title, Task.description)
    if search_title:
        task_list_query = task_list_query.where(Task.title.ilike(f"%{search_title}%"))
    return db_session.exec(task_list_query).mappings().all()


def fetch_task_by_id(db_session: Session, task_id: int) -> Optional[BaseTaskList]:
    """Fetch and return task by id."""
    return db_session.get(Task, task_id)


def create_new_task(db_session: Session, task: TaskCreate) -> Task:
    """Create a new task and return the created task."""
    new_task = Task(title=task.title, description=task.description)
    db_session.add(new_task)
    db_session.commit()
    db_session.refresh(new_task)
    return (
        {"message": "Task created successfully"}
        if new_task
        else {"message": "Task creation failed"}
    )


def update_task_data(db_session: Session, existing_task: Task, task: TaskCreate) -> None:
    """Update existing task with new data."""
    try:
        existing_task.title = task.title
        if task.description:
            existing_task.description = task.description
        db_session.add(existing_task)
        db_session.commit()
        db_session.refresh(existing_task)
    except Exception as e:
        db_session.rollback()
        raise e


def delete_task_data(db_session: Session, existing_task: Task) -> None:
    """Delete existing task."""
    try:
        db_session.delete(existing_task)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise e
