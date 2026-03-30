from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status

from app.Service.offer_service import OfferService
from app.schemas.offer import (
    OfferCreate,
    OfferResponse,
    OfferUpdate,
    DiscountType,
)
from app.dependencies.offer_dependency import get_offer_service

router = APIRouter(prefix="/offers", tags=["Offers"])


# ------------------------------------------------------------------ #
#  Offer CRUD                                                          #
# ------------------------------------------------------------------ #

@router.get(
    "/",
    response_model=List[OfferResponse],
    summary="List all offers",
)
def get_all_offers(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    is_active: Optional[bool] = Query(default=None, description="Filter by active status"),
    service: OfferService = Depends(get_offer_service),
):
    return service.get_all_offers(skip=skip, limit=limit, is_active=is_active)


@router.get(
    "/active",
    response_model=List[OfferResponse],
    summary="Get currently active offers (respects date window)",
)
def get_active_offers(
    service: OfferService = Depends(get_offer_service),
):
    return service.get_active_offers()


@router.get(
    "/discount-types",
    summary="List all supported discount types",
)
def get_discount_types():
    descriptions = {
        DiscountType.PERCENTAGE: "Reduce price by a percentage. discount_value = 0–100.",
        DiscountType.FLAT: "Reduce price by a fixed amount. discount_value = rupee/unit amount.",
        DiscountType.FIXED_PRICE: "Override price to a fixed value. discount_value = selling price.",
        DiscountType.BUY_X_GET_Y: (
            "Buy X get Y free. discount_value = free item count per cycle. "
            "e.g. Buy 2 Get 1: discount_value=1, cycle size = 3."
        ),
    }
    return [{"type": dt.value, "description": desc} for dt, desc in descriptions.items()]


@router.get(
    "/{offer_id}",
    response_model=OfferResponse,
    summary="Get a single offer by ID",
)
def get_offer_by_id(
    offer_id: int,
    service: OfferService = Depends(get_offer_service),
):
    return service.get_offer_by_id(offer_id)


@router.post(
    "/",
    response_model=OfferResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new offer with linked variants",
)
def create_offer(
    data: OfferCreate,
    service: OfferService = Depends(get_offer_service),
):
    return service.create_offer(data)


@router.patch(
    "/{offer_id}",
    response_model=OfferResponse,
    summary="Partially update an offer",
)
def update_offer(
    offer_id: int,
    data: OfferUpdate,
    service: OfferService = Depends(get_offer_service),
):
    return service.update_offer(offer_id, data)


@router.delete(
    "/{offer_id}",
    summary="Delete an offer",
)
def delete_offer(
    offer_id: int,
    service: OfferService = Depends(get_offer_service),
):
    return service.delete_offer(offer_id)


@router.patch(
    "/{offer_id}/toggle",
    response_model=OfferResponse,
    summary="Toggle offer active/inactive status",
)
def toggle_offer_status(
    offer_id: int,
    service: OfferService = Depends(get_offer_service),
):
    return service.toggle_offer_status(offer_id)


# ------------------------------------------------------------------ #
#  Variant ↔ Offer                                                     #
# ------------------------------------------------------------------ #

@router.get(
    "/{offer_id}/variants",
    response_model=OfferResponse,
    summary="Get an offer with all its linked variants",
)
def get_offer_with_variants(
    offer_id: int,
    service: OfferService = Depends(get_offer_service),
):
    """Returns the offer object which includes offer_variants list."""
    return service.get_offer_by_id(offer_id)


@router.post(
    "/{offer_id}/variants",
    response_model=OfferResponse,
    summary="Add variants to an existing offer",
)
def add_variants_to_offer(
    offer_id: int,
    variant_ids: List[int],
    service: OfferService = Depends(get_offer_service),
):
    return service.add_variants_to_offer(offer_id, variant_ids)


@router.delete(
    "/{offer_id}/variants",
    summary="Remove specific variants from an offer",
)
def remove_variants_from_offer(
    offer_id: int,
    variant_ids: List[int],
    service: OfferService = Depends(get_offer_service),
):
    return service.remove_variants_from_offer(offer_id, variant_ids)


# ------------------------------------------------------------------ #
#  Variant-centric lookups                                             #
# ------------------------------------------------------------------ #

@router.get(
    "/variants/{variant_id}/offers",
    response_model=List[OfferResponse],
    summary="Get all offers (active + inactive) linked to a variant",
)
def get_offers_for_variant(
    variant_id: int,
    service: OfferService = Depends(get_offer_service),
):
    return service.get_offers_for_variant(variant_id)


@router.get(
    "/variants/{variant_id}/offers/active",
    response_model=List[OfferResponse],
    summary="Get currently active offers for a variant (sorted by priority)",
)
def get_active_offers_for_variant(
    variant_id: int,
    service: OfferService = Depends(get_offer_service),
):
    return service.get_active_offers_for_variant(variant_id)


# ------------------------------------------------------------------ #
#  Pricing utility                                                     #
# ------------------------------------------------------------------ #

@router.get(
    "/{offer_id}/calculate-price",
    summary="Calculate discounted price for a given original price",
)
def calculate_discounted_price(
    offer_id: int,
    original_price: float = Query(..., gt=0, description="Original selling price"),
    quantity: int = Query(default=1, ge=1, description="Cart quantity (relevant for buy_x_get_y)"),
    service: OfferService = Depends(get_offer_service),
):
    return service.calculate_discounted_price(offer_id, original_price, quantity)