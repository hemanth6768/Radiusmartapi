from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.Service.admin_service import AdminService
from fastapi import Request
import requests
from fastapi.responses import RedirectResponse
import os
from dotenv import load_dotenv



load_dotenv()
router = APIRouter(prefix="/admin", tags=["Admins"])


GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

@router.post("/upload-csv")
async def upload_products_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    return await AdminService.import_products_csv(db, file)




