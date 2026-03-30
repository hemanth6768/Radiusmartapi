from fastapi import FastAPI
from app.database import engine, Base
from contextlib import asynccontextmanager
from app.models.category import Category
from app.models.order import Order
from app.models.orderitem import OrderItem
from app.models.product import Product
from app.models.brand import Brand
from app.models.offer import Offer
from app.models.offervariant import OfferVariant
from app.models.section import Section
from app.models.productvariant import ProductVariant
from app.models.audit_log import AuthAuditLog
from app.models.emailverification import EmailVerificationToken
from app.models.oauthaccount import OAuthAccount
from app.models.password_reset_token import PasswordResetToken
from app.models.permission import Permission
from app.models.rolepermission import RolePermission
from app.models.role import Role
from app.models.user import User
from app.models.userrole import UserRole
from app.models.session import Session
from app.models.user_address import UserAddress
from app.models.token_blocklist import TokenBlocklist  # new model from auth rewrite
from fastapi.middleware.cors import CORSMiddleware
from app.Route.category_route import router as category_route
from app.Route.product_route import router as product_router
from app.Route.order_route import router as order_router
from app.Route.brand_route import router as brand_router
from app.Route.offer_route import router as offer_router
from app.Route.section_router import router as section_router
from app.Route.home_route import router as home_router
from app.Route.auth_router import router as auth_router, limiter  # limiter must come from here
from app.Route.search_route import router as search_router
from app.Route.admin_route import router as admin_router
from app.Route.payment_route import router as payment_router
from app.Route.user_route import router as user_router
from fastapi.staticfiles import StaticFiles
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
 
 
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
 
 
app = FastAPI(lifespan=lifespan)
 
# ---------------------------------------------------------------------------
# Rate limiter — must be registered before routers are included
# app.state.limiter  → slowapi reads this on every request to find the counter
# add_exception_handler → returns a clean 429 JSON instead of a 500 crash
# ---------------------------------------------------------------------------
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
 
# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------
origins = [
    "http://localhost:8080",
    "https://radiusmartui-dbb3cxgjb4f6h4du.centralindia-01.azurewebsites.net"
]
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
# ---------------------------------------------------------------------------
# Static files
# ---------------------------------------------------------------------------
app.mount("/static", StaticFiles(directory="static"), name="static")
 
# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(category_route)
app.include_router(product_router)
app.include_router(order_router)
app.include_router(brand_router)
app.include_router(offer_router)
app.include_router(section_router)
app.include_router(home_router)
app.include_router(auth_router)
app.include_router(search_router)
app.include_router(admin_router)
app.include_router(payment_router)
app.include_router(user_router)
 
@app.get("/")
def root():
    return {"message": "Radius Market going to Running 🚀"}