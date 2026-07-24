"""Schema for task creation requests."""

from typing import Optional

from sqlmodel import Field, SQLModel


class TaskCreate(SQLModel):
    """Task creation schema."""

    title: str = Field(description="Title of the task", nullable=False, max_length=100)
    description: Optional[str] = Field(
        default=None, description="Description of a task", nullable=True, max_length=300
    )
