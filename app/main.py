from fastapi import FastAPI
from app.database import engine
from app.models import category,order,orderitem,product
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base
from app.Route.category_route import router as category_route
from app.Route.product_route import router as product_router
from app.Route.order_route import router as order_router
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Radius Market API")


origins = [
    "http://localhost:8080"   # React dev
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # allowed frontend domains
    allow_credentials=True,
    allow_methods=["*"],         # GET, POST, PUT, DELETE
    allow_headers=["*"],         # all headers
)

app.mount("/static", StaticFiles(directory="static"), name="static")

Base.metadata.create_all(bind=engine)

app.include_router(category_route)
app.include_router(product_router)
app.include_router(order_router)
@app.get("/")
def root():
    return {"message": "Radius Market Backend Running 🚀"}