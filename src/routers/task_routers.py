from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.models.task import Task
from src.schemas.task_schema import TaskCreate, TaskResponse, TaskUpdate
from src.utils.helpers import get_task_or_404
from src.utils.dependencies import get_current_user
from src.models.user import User
task_router = APIRouter(prefix="/tasks", tags=["Tasks"])


#-----------CreateTasks--------------------
@task_router.post("/", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_task = Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

#-----------GetTasks-------------------------
@task_router.get("/", response_model=list[TaskResponse])
def get_tasks(
    completed: bool | None= None,
    task_type: str | None= None ,
    page: int =1,
    limit: int = 10 ,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
   query = db.query(Task)

   if completed is not None:
       query = query.filter(Task.completed == completed)

   if task_type is not None:
       query = query.filter(Task.task_type == task_type)   

   return query.offset((page -1) * limit).limit(limit).all()   

#-----------GetTask--------------------
@task_router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_task_or_404(task_id, db)

#-----------UpdateTask--------------------
@task_router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_data: TaskUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = get_task_or_404(task_id, db)
    for field, value in task_data.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task   
 
#-----------DeleteTask--------------------
@task_router.delete("/{task_id}")
def delete_task(task_id: int, db: Session= Depends(get_db), current_user: User = Depends(get_current_user)):
    task = get_task_or_404(task_id, db)
    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}
