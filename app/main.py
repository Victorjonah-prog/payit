from fastapi import FastAPI, status, HTTPException
from .models.base import Base
from .database import engine
# from app.models.users_model import User
from .models.products_model import Product
import os
from sqlalchemy.exc import OperationalError
from .routes import users_routes, products_routes, auth_routes, orders_routes, oauth
from fastapi.staticfiles import StaticFiles
import time
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware


import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def db_and_table_init():
    retries = 10
    for i in range(retries):
        try:
            logger.info("STARTING APPLICATION!")
            Base.metadata.create_all(bind=engine)
            logger.info("DATABASE INITIALIZED SUCCESSFULLY!")
            break
        except OperationalError as e:
            logger.warning(f"MySQL NOT READY, RETRYING ({i+1}/{retries}) {e}...")
            time.sleep(3)
        except Exception as e:
            logger.info(f"DATABASE INITIALIZATION FAILED: {e}")



app = FastAPI(
    title = "PayIt App",
    version = "0.0.1",
    description = "market place..."
    )


app.include_router(users_routes.router)
app.include_router(oauth.router)
app.include_router(auth_routes.router)
app.include_router(products_routes.router)
app.include_router(orders_routes.router)


app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv('JWT_SECRET_KEY'),
    https_only=False
)


origins = [
    "http://localhost:8000"


]

app.add_middleware(CORSMiddleware,allow_origins=origins,
                   allow_credentials=True,
                   allow_methods = ["*"],
                   allow_headers = ["*"]

                   )

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
def on_startup():
    db_and_table_init()

@app.get("/")
def home():
    return{
        "status":"success",
        "message":"hello world"
    }

   

