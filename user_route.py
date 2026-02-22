from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import user_query
from database import get_db


router = APIRouter()

@router.get("/all-users")
def get_all_users(db: Session = Depends(get_db)):
    users = user_query.get_all_users(db)
    return {"users": users}