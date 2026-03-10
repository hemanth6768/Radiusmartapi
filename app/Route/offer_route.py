from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.Service.offer_service import OfferService
from app.schemas.offer import OfferCreate, OfferUpdate, OfferResponse


router = APIRouter(prefix="/offers", tags=["Offers"])


@router.post("/", response_model=OfferResponse)
def create_offer(offer: OfferCreate, db: Session = Depends(get_db)):
    return OfferService.create_offer(db, offer)


@router.get("/", response_model=List[OfferResponse])
def get_offers(db: Session = Depends(get_db)):
    return OfferService.get_offers(db)


@router.get("/{offer_id}", response_model=OfferResponse)
def get_offer(offer_id: int, db: Session = Depends(get_db)):
    return OfferService.get_offer(db, offer_id)


@router.put("/{offer_id}", response_model=OfferResponse)
def update_offer(offer_id: int, updates: OfferUpdate, db: Session = Depends(get_db)):
    return OfferService.update_offer(db, offer_id, updates)


@router.delete("/{offer_id}")
def delete_offer(offer_id: int, db: Session = Depends(get_db)):
    return OfferService.delete_offer(db, offer_id)