from fastapi import FastAPI
from src.database.db import engine
from src.models import task, user
from src.routers.task_routers import task_router
from src.routers.user_routers import user_router

task.Base.metadata.create_all(bind=engine)
user.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(task_router)
app.include_router(user_router)

@app.get('/')
def root():
    return {"message": "Welcome to Task Manager API"}

