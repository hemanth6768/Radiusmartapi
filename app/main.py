from fastapi import FastAPI
from app.database import engine, Base
from contextlib import asynccontextmanager
from app.models.category import Category
from app.models.order import Order
from app.models.orderitem import OrderItem
from app.models.product import Product
from app.models.brand import Brand
from app.models.offer import Offer
from app.models.productvariant import ProductVariant
from fastapi.middleware.cors import CORSMiddleware
from app.Route.category_route import router as category_route
from app.Route.product_route import router as product_router
from app.Route.order_route import router as order_router
from app.Route.brand_route import router as brand_router
from app.Route.offer_route import router as offer_router
from fastapi.staticfiles import StaticFiles


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)


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

app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(category_route)
app.include_router(product_router)
app.include_router(order_router)
app.include_router(brand_router)
app.include_router(offer_router)


@app.get("/")
def root():
    return {"message": "Radius Market going to Running 🚀"}