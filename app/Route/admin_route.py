from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.Service.admin_service import AdminService

router = APIRouter(prefix="/admin", tags=["Admins"])

@router.post("/upload-csv")
async def upload_products_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    return await AdminService.import_products_csv(db, file)