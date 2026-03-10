from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.Repository.offer_repository import OfferRepository
from app.schemas.offer import OfferCreate, OfferUpdate


class OfferService:


    @staticmethod
    def create_offer(db: Session, offer: OfferCreate):

        if offer.discount_value <= 0:
            raise HTTPException(400, "Discount must be greater than 0")

        return OfferRepository.create_offer(db, offer)


    @staticmethod
    def get_offers(db: Session):
        return OfferRepository.get_all_offers(db)


    @staticmethod
    def get_offer(db: Session, offer_id: int):

        offer = OfferRepository.get_offer_by_id(db, offer_id)

        if not offer:
            raise HTTPException(404, "Offer not found")

        return offer


    @staticmethod
    def update_offer(db: Session, offer_id: int, updates: OfferUpdate):

        offer = OfferRepository.get_offer_by_id(db, offer_id)

        if not offer:
            raise HTTPException(404, "Offer not found")

        return OfferRepository.update_offer(db, offer, updates)


    @staticmethod
    def delete_offer(db: Session, offer_id: int):

        offer = OfferRepository.get_offer_by_id(db, offer_id)

        if not offer:
            raise HTTPException(404, "Offer not found")

        OfferRepository.delete_offer(db, offer)

        return {"message": "Offer deleted successfully"}