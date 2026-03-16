from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.Service.home_service import HomeService
from app.schemas.home import HomeResponse

router = APIRouter(prefix="/home", tags=["Home"])


@router.get("/", response_model=HomeResponse)
def get_home(db: Session = Depends(get_db)):
    return HomeService.get_home_data(db)