"""Task model definition using SQLModel."""

from sqlmodel import Field, SQLModel


class Task(SQLModel, table=True):
    """Tasks db model class."""

    __tablename__ = "tasks"

    id: int = Field(primary_key=True, nullable=False)
    title: str = Field(description="Title of the task", nullable=False, max_length=100)
    description: str = Field(description="Description of a task", nullable=True, max_length=300)
