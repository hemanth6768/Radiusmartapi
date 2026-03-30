from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from datetime import datetime, timezone

from app.models.offer import Offer
from app.models.offervariant import OfferVariant
from app.schemas.offer import OfferCreate, OfferUpdate


class OfferRepository:
    def __init__(self, db: Session):
        self.db = db

    # ------------------------------------------------------------------ #
    #  Offer CRUD                                                          #
    # ------------------------------------------------------------------ #

    def get_all(
        self,
        skip: int = 0,
        limit: int = 50,
        is_active: Optional[bool] = None,
    ) -> List[Offer]:
        query = self.db.query(Offer).options(joinedload(Offer.offer_variants))
        if is_active is not None:
            query = query.filter(Offer.is_active == is_active)
        return query.order_by(Offer.priority.desc()).offset(skip).limit(limit).all()

    def get_by_id(self, offer_id: int) -> Optional[Offer]:
        return (
            self.db.query(Offer)
            .options(joinedload(Offer.offer_variants))
            .filter(Offer.id == offer_id)
            .first()
        )

    def get_active_offers(self) -> List[Offer]:
        """Offers that are active AND within their date window (if set)."""
        now = datetime.now(timezone.utc)
        return (
            self.db.query(Offer)
            .options(joinedload(Offer.offer_variants))
            .filter(
                Offer.is_active == True,
                (Offer.start_date == None) | (Offer.start_date <= now),
                (Offer.end_date == None) | (Offer.end_date >= now),
            )
            .order_by(Offer.priority.desc())
            .all()
        )

    def create(self, data: OfferCreate) -> Offer:
        offer = Offer(
            name=data.name,
            discount_type=data.discount_type,
            discount_value=data.discount_value,
            priority=data.priority,
            start_date=data.start_date,
            end_date=data.end_date,
            is_active=data.is_active,
        )
        self.db.add(offer)
        self.db.flush()  # get offer.id before committing

        for variant_id in data.variant_ids:
            self.db.add(OfferVariant(offer_id=offer.id, variant_id=variant_id))

        self.db.commit()
        self.db.refresh(offer)
        return offer

    def update(self, offer: Offer, data: OfferUpdate) -> Offer:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(offer, field, value)
        self.db.commit()
        self.db.refresh(offer)
        return offer

    def delete(self, offer: Offer) -> None:
        self.db.delete(offer)
        self.db.commit()

    # ------------------------------------------------------------------ #
    #  OfferVariant helpers                                                #
    # ------------------------------------------------------------------ #

    def get_offers_by_variant(self, variant_id: int) -> List[Offer]:
        """All offers (active or not) linked to a variant."""
        return (
            self.db.query(Offer)
            .join(Offer.offer_variants)
            .filter(OfferVariant.variant_id == variant_id)
            .options(joinedload(Offer.offer_variants))
            .order_by(Offer.priority.desc())
            .all()
        )

    def get_active_offers_by_variant(self, variant_id: int) -> List[Offer]:
        """Active + date-valid offers for a variant, ordered by priority."""
        now = datetime.now(timezone.utc)
        return (
            self.db.query(Offer)
            .join(Offer.offer_variants)
            .filter(
                OfferVariant.variant_id == variant_id,
                Offer.is_active == True,
                (Offer.start_date == None) | (Offer.start_date <= now),
                (Offer.end_date == None) | (Offer.end_date >= now),
            )
            .options(joinedload(Offer.offer_variants))
            .order_by(Offer.priority.asc())
            .all()
        )

    def add_variants_to_offer(self, offer_id: int, variant_ids: List[int]) -> List[OfferVariant]:
        """Append new variants to an existing offer (skips duplicates)."""
        existing_ids = {
            ov.variant_id
            for ov in self.db.query(OfferVariant).filter(OfferVariant.offer_id == offer_id).all()
        }
        new_entries = []
        for vid in variant_ids:
            if vid not in existing_ids:
                ov = OfferVariant(offer_id=offer_id, variant_id=vid)
                self.db.add(ov)
                new_entries.append(ov)
        self.db.commit()
        return new_entries

    def remove_variants_from_offer(self, offer_id: int, variant_ids: List[int]) -> int:
        """Remove specific variants from an offer. Returns deleted count."""
        deleted = (
            self.db.query(OfferVariant)
            .filter(
                and_(
                    OfferVariant.offer_id == offer_id,
                    OfferVariant.variant_id.in_(variant_ids),
                )
            )
            .delete(synchronize_session=False)
        )
        self.db.commit()
        return deleted

    def variant_link_exists(self, offer_id: int, variant_id: int) -> bool:
        return (
            self.db.query(OfferVariant)
            .filter(OfferVariant.offer_id == offer_id, OfferVariant.variant_id == variant_id)
            .first()
            is not None
        )
    
