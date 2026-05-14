from sqlalchemy import Boolean, Column, DateTime, Integer, String
from datetime import datetime, timezone
from src.database.db import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable= False)
    description = Column(String, nullable=True)
    task_type = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    completed = Column(Boolean, default=False)
