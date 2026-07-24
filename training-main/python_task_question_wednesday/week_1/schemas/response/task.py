"""Schemas for task responses."""

from typing import List, Optional

from sqlmodel import Field, SQLModel


class BaseTaskList(SQLModel):
    """Schema representing a task."""

    id: int = Field(description="Task Id")
    title: str = Field(description="Task Title", max_length=100)
    description: Optional[str] = Field(description="Task Description", max_length=300)


class TaskList(SQLModel):
    """Schema representing a list of tasks."""

    task_list: List[BaseTaskList]
