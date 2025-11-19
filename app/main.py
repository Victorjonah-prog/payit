from fastapi import FastAPI
from .database import Base, engine
from .routes import user_routes, products_routes
import logging

logger = logging.getLogger(__name__)


app = FastAPI()


Base.metadata.create_all(bind=engine)



app.include_router(user_routes.router, prefix="/api", tags=["users"])
app.include_router(products_routes.router, prefix="/api", tags=["products"])

@app.get("/")
def read_root():
    return {"message": "Welcome to PayIt API"}