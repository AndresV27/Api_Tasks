from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.models.user import User
from src.schemas.user_schema import UserBase, UserResponse , UserCreate, UserUpdate

user_router = APIRouter(prefix="/users", tags=["Users"])

#-----------SearchUsers--------------------
def get_user_or_404(user_id: int, db: Session)->User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found" )
    return user

#-----------CreateUsers--------------------
@user_router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

#-----------Tasks-------------------------
@user_router.get("/", response_model=list[UserResponse])
def get_users(is_active: bool | None= None,page: int =1, limit: int = 10 ,db: Session = Depends(get_db)):
   query = db.query(User)

   if is_active is not None:
       query = query.filter(User.is_active == is_active)

   return query.offset((page -1) * limit).limit(limit).all()  
 
#-----------GetUser--------------------
@user_router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return get_user_or_404(user_id, db)

#-----------UpdateUser--------------------
@user_router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    user = get_user_or_404(user_id, db)
    for field, value in user_data.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user   

#-----------DeleteUser--------------------
@user_router.delete("/{user_id}")
def delete_user(user_id: int, db: Session= Depends(get_db)):
    user = get_user_or_404(user_id, db)
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}

 