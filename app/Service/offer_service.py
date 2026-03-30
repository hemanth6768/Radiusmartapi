from typing import List, Optional
from fastapi import HTTPException, status

from app.Repository.offer_repository import OfferRepository
from app.schemas.offer import OfferCreate, OfferUpdate
from app.models.offer import Offer


class OfferService:
    def __init__(self, repo: OfferRepository):
        self.repo = repo

    # ------------------------------------------------------------------ #
    #  Internal helpers                                                    #
    # ------------------------------------------------------------------ #

    def _get_or_404(self, offer_id: int) -> Offer:
        offer = self.repo.get_by_id(offer_id)
        if not offer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Offer with id {offer_id} not found",
            )
        return offer

    @staticmethod
    def _apply_discount(base_price: float, offer: Offer, quantity: int = 1) -> float:
        """
        Pure discount calculation — no DB calls, no HTTPException.
        Used internally by ProductService to compute variant sales_price,
        and reused by calculate_discounted_price() below.

        Returns the final discounted price rounded to 2 decimal places.
        """
        discount_type = offer.discount_type
        discount_value = offer.discount_value
        final_price = base_price

        if discount_type == "percentage":
            final_price = base_price * (1 - discount_value / 100)

        elif discount_type == "flat":
            final_price = max(base_price - discount_value, 0)

        elif discount_type == "fixed_price":
            final_price = discount_value

        elif discount_type == "buy_x_get_y":
            # discount_value = free items per cycle
            # e.g. Buy 2 Get 1: discount_value=1, cycle=3
            # Every 3 items, 1 is free → effective per-unit price drops
            free_per_cycle = int(discount_value)
            cycle = free_per_cycle + 1
            free_items = (quantity // cycle) * free_per_cycle
            payable_items = quantity - free_items
            final_price = (base_price * payable_items) / quantity if quantity else base_price

        return round(final_price, 2)

    # ------------------------------------------------------------------ #
    #  Offer CRUD                                                          #
    # ------------------------------------------------------------------ #

    def get_all_offers(
        self,
        skip: int = 0,
        limit: int = 50,
        is_active: Optional[bool] = None,
    ) -> List[Offer]:
        return self.repo.get_all(skip=skip, limit=limit, is_active=is_active)

    def get_offer_by_id(self, offer_id: int) -> Offer:
        return self._get_or_404(offer_id)

    def get_active_offers(self) -> List[Offer]:
        return self.repo.get_active_offers()

    def create_offer(self, data: OfferCreate) -> Offer:
        return self.repo.create(data)

    def update_offer(self, offer_id: int, data: OfferUpdate) -> Offer:
        offer = self._get_or_404(offer_id)
        return self.repo.update(offer, data)

    def delete_offer(self, offer_id: int) -> dict:
        offer = self._get_or_404(offer_id)
        self.repo.delete(offer)
        return {"detail": f"Offer {offer_id} deleted successfully"}

    def toggle_offer_status(self, offer_id: int) -> Offer:
        offer = self._get_or_404(offer_id)
        update_data = OfferUpdate(is_active=not offer.is_active)
        return self.repo.update(offer, update_data)

    # ------------------------------------------------------------------ #
    #  Variant <-> Offer                                                   #
    # ------------------------------------------------------------------ #

    def get_offers_for_variant(self, variant_id: int) -> List[Offer]:
        return self.repo.get_offers_by_variant(variant_id)

    def get_active_offers_for_variant(self, variant_id: int) -> List[Offer]:
        return self.repo.get_active_offers_by_variant(variant_id)

    def add_variants_to_offer(self, offer_id: int, variant_ids: List[int]) -> Offer:
        self._get_or_404(offer_id)
        if not variant_ids:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="variant_ids list cannot be empty",
            )
        if len(variant_ids) != len(set(variant_ids)):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Duplicate variant_ids provided",
            )
        self.repo.add_variants_to_offer(offer_id, variant_ids)
        return self._get_or_404(offer_id)

    def remove_variants_from_offer(self, offer_id: int, variant_ids: List[int]) -> dict:
        self._get_or_404(offer_id)
        if not variant_ids:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="variant_ids list cannot be empty",
            )
        deleted = self.repo.remove_variants_from_offer(offer_id, variant_ids)
        return {"detail": f"{deleted} variant link(s) removed from offer {offer_id}"}

    # ------------------------------------------------------------------ #
    #  Discount calculation utility                                        #
    # ------------------------------------------------------------------ #

    def calculate_discounted_price(
        self, offer_id: int, original_price: float, quantity: int = 1
    ) -> dict:
        """
        Returns the effective price after applying an offer's discount.
        Useful for cart/checkout preview endpoints.
        """
        offer = self._get_or_404(offer_id)

        if original_price < 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="original_price must be non-negative",
            )

        final_price = self._apply_discount(original_price, offer, quantity)

        return {
            "offer_id": offer_id,
            "discount_type": offer.discount_type,
            "original_price": original_price,
            "final_price": final_price,
            "savings": round(original_price - final_price, 2),
            "quantity": quantity,
        }