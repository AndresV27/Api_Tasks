from fastapi import FastAPI
from src.database.db import engine, SessionLocal
from src.models import task, user, role
from src.models.role import Role
from src.routers.task_routers import task_router
from src.routers.user_routers import user_router
from src.routers.auth_routers import auth_router
from contextlib import asynccontextmanager
from src.utils.auth import hash_password
from src.models.user import User
from fastapi.middleware.cors import CORSMiddleware

import os

task.Base.metadata.create_all(bind=engine)
user.Base.metadata.create_all(bind=engine)
role.Base.metadata.create_all(bind=engine)

#-----------CreateDefaultRoles--------------------
def create_default_roles():
    db = SessionLocal()
    try:
        if not db.query(Role).first():
            roles = [
                Role(name= "admin"),
                Role(name= "user")
            ]
            db.add_all(roles)
            db.commit()
    finally:
        db.close()    

#-----------CreateDefaultAdmin--------------------
def create_default_admin():
    db = SessionLocal()
    try:
        admin_email = os.getenv("ADMIN_EMAIL")
        admin_password = os.getenv("ADMIN_PASSWORD")
        
        if not db.query(User).filter(User.email == admin_email).first():
            admin = User(
                name = "Admin",
                email = admin_email,
                password = hash_password(admin_password),
                role_id = 1,
                is_active = True
            )
            db.add(admin)
            db.commit()
    finally:
        db.close()


@asynccontextmanager
async def startup(app: FastAPI):
    create_default_roles()
    create_default_admin()
    yield         

app = FastAPI(title="Task Manager API", lifespan= startup)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(task_router)
app.include_router(user_router)
app.include_router(auth_router)

@app.get('/')
def root():
    return {"message": "Welcome to Task Manager API"}

