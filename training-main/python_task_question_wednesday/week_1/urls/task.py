"""API routes for task management using FastAPI."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session

from db.session import get_db
from schemas.request.task import TaskCreate
from schemas.response.task import BaseTaskList, TaskList
from views.task import (
    create_new_task,
    delete_task_data,
    fetch_task_by_id,
    fetch_task_list,
    update_task_data,
)

task_router = APIRouter(prefix="/task", tags=["Task"])


@task_router.get("/", response_model=TaskList)
def get_task_list(
    search_title: str = Query(default=None, max_length=100),
    db: Session = Depends(get_db),
) -> TaskList:
    """Fetch a list of tasks, optionally filtered by title."""
    task_list = fetch_task_list(db, search_title)
    return {"task_list": task_list}


@task_router.get("/{task_id}", response_model=BaseTaskList)
def get_task_by_id(task_id: int, db: Session = Depends(get_db)):
    """Fetch a task by its ID."""
    task = fetch_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@task_router.post("/")
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """Create a new task."""
    return create_new_task(db, task)


@task_router.patch("/{task_id}")
def update_task(task_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    """Update an existing task."""
    try:
        existing_task = fetch_task_by_id(db, task_id)
        if not existing_task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        update_task_data(db, existing_task, task)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error"
        ) from e

    return {"message": "Task updated successfully"}


@task_router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a task by its ID."""
    try:
        existing_task = fetch_task_by_id(db, task_id)
        if not existing_task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        delete_task_data(db, existing_task)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error"
        ) from e
    return {"message": "Task deleted successfully"}
