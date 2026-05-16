from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.models.task import Task
from src.models.user import User


#-----------SearchTasks--------------------
def get_task_or_404(task_id: int, db: Session)->Task:
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found" )
    return task

#-----------SearchUsers--------------------
def get_user_or_404(user_id: int, db: Session)->User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found" )
    return user

#-----------ValidateUsers--------------------
def validate_active_user(user: User):
    if not user.is_active:
        raise HTTPException(status_code=403, detail="User is inactive")
