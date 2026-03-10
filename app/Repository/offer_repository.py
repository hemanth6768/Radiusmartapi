from sqlalchemy.orm import Session
from app.models.offer import Offer


class OfferRepository:

    @staticmethod
    def create_offer(db: Session, offer):

        db_offer = Offer(**offer.model_dump())

        db.add(db_offer)
        db.commit()
        db.refresh(db_offer)

        return db_offer


    @staticmethod
    def get_all_offers(db: Session):
        return db.query(Offer).all()


    @staticmethod
    def get_offer_by_id(db: Session, offer_id: int):
        return db.query(Offer).filter(Offer.id == offer_id).first()


    @staticmethod
    def update_offer(db: Session, db_offer, updates):

        update_data = updates.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_offer, key, value)

        db.commit()
        db.refresh(db_offer)

        return db_offer


    @staticmethod
    def delete_offer(db: Session, db_offer):

        db.delete(db_offer)
        db.commit()