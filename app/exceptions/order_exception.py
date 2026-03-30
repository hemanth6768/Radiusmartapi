"""
Domain-specific exceptions for the Order module.
Each maps to a specific HTTP status in the router layer,
keeping business logic free from HTTP concerns.
"""


class OrderBaseException(Exception):
    """Base for all order-domain exceptions."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class UserNotFoundException(OrderBaseException):
    pass


class AddressNotFoundException(OrderBaseException):
    pass


class AddressAccessDeniedException(OrderBaseException):
    pass


class ProductVariantNotFoundException(OrderBaseException):
    def __init__(self, variant_id: int):
        self.variant_id = variant_id
        super().__init__(f"Product variant {variant_id} not found")


class InsufficientStockException(OrderBaseException):
    def __init__(self, variant_id: int, available: float, requested: float):
        self.variant_id = variant_id
        self.available  = available
        self.requested  = requested
        super().__init__(
            f"Insufficient stock for variant {variant_id}: "
            f"requested {requested}, available {available}"
        )


class InvalidOrderRequestException(OrderBaseException):
    pass


class OrderNotFoundException(OrderBaseException):
    pass