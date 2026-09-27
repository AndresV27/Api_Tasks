from pydantic import BaseModel
from datetime import datetime

class TaskBase(BaseModel):
    title: str
    description: str | None = None
    task_type: str
    user_id: int

class TaskCreate(TaskBase):
    pass
    # por ahora igual a taskbase pero sirve para agragar mas campos adelante

class TaskResponse(TaskBase):
    id: int
    completed: bool
    created_at: datetime

    class Config:
        from_atributes = True    

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    task_type: str | None = None
    completed: bool | None = None