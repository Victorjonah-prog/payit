from fastapi import FastAPI, status, HTTPException
from .models.base import Base
from .database import engine
from .models.users_model import User
from .models.products_model import Product
from .models.farmers_model import Farmer
from .models.buyers_model import Buyer
from .models.orders_model import Order
from .models.products_category_model import ProductCategory
from sqlalchemy.exc import OperationalError
from .routes import users_routes, products_routes, auth_routes, orders_routes
#from .routes import admin
import time

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

# def init_products_category(db: SessionLocal=(get_db)):
#     category_names=["grains","tubers","cereals","fruits","livestock","vegetables","oils","latex"]
    
#     try:
#         count = db.query(ProductCategory).count()
#         if count == 0:
#             for cat_name in category_names:
#                 new_category = ProductCategory(category_name=cat_name)
#                 db.add(new_category)
#         db.commit()
#         db.refresh(new_category)
#         logger.info(f"PRODUCT CATEGORY POPULATED SUCCESSFULLY")
#     except Exception as e:
#         logger.info(f"PRODUCT CATEGORY DATABASE FAILED : {e}")




app = FastAPI(
    title = "PayIt App",
    version = "0.0.1",
    description = "market place..."
    )

app.include_router(users_routes.router)
app.include_router(products_routes.router)
app.include_router(auth_routes.router)
app.include_router(orders_routes.router)
#app.include_router(admin.router)
@app.on_event("startup")
def on_startup():
    db_and_table_init()
    #admin.init_products_category()
   

