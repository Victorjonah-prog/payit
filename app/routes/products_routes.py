from sqlalchemy.orm import Session
from app.enums import Category
from ..database import get_db
from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status, Depends
from ..models import products_model, users_model, farmers_model, buyers_model, products_category_model
from ..middlewares.auth import AuthMiddleware
from datetime import datetime
from typing import List
import aiofiles
import os
from uuid import uuid4
from ..middlewares.auth import AuthMiddleware  
from ..models.users_model import User



router = APIRouter(tags=["Products"])

UPLOAD_DIR= "static/images"

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(
    category: Category = Form(...),
    status: str = Form(...),
    name: str = Form(...),
    image: UploadFile = File(...),
    description: str = Form(...),
    unit_price: str = Form(...),
    quantity: str = Form(...),
    current_user: User = Depends(AuthMiddleware),
    db: Session = Depends(get_db)
):
    
    farmer = db.query(farmers_model.Farmer).filter_by(user_id=current_user.id).first()
    if not farmer:
        farmer = farmers_model.Farmer(
            user_id=current_user.id,
        )
        db.add(farmer)
        db.commit()
        db.refresh(farmer)

    # upload image
    allowed_ext = {"jpg", "jpeg", "png"}
    file_ext = image.filename.split(".")[-1].lower() 
    if file_ext not in allowed_ext:
        raise HTTPException(status_code=400, detail="Only jpg/jpeg/png allowed")

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_name = f"{uuid4()}.{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, file_name)
    async with aiofiles.open(file_path, "wb") as f:
        await f.write(await image.read())

    #check size image 
    image_size = 2 * 1024 * 1024  
    if os.path.getsize(file_path) > image_size:
        os.remove(file_path)
        raise HTTPException(status_code=400, detail="Image size exceeds 2 MB limit") 


    new_product = products_model.Product(
        farmer_id=farmer.id, 
        category=category,
        status=status,
        name=name,
        image_url=f"/static/images/{file_name}",
        description=description,
        unit_price=float(unit_price),
        quantity=int(quantity),
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {
        "success": True,
        "message": "Product created successfully! Farmer profile auto-created.",
        "product": new_product
    }

@router.get("/")
def get_all_products(
    db: Session = Depends(get_db)
):
    products = db.query(products_model.Product).all()
    return products


@router.get("/category/{category}")
def get_products_by_category(
    category: Category,
    db: Session = Depends(get_db)
):
    products = db.query(products_model.Product).filter_by(category=category).all()
    return products

@router.get("/farmer/{farmer_id}")
def get_products_by_farmer( 
    farmer_id: int,
    db: Session = Depends(get_db)
):
    products = db.query(products_model.Product).filter_by(farmer_id=farmer_id).all()
    return products

@router.put("/{product_id}")
def update_product(
    product_id: int,
    status: str = Form(...),
    name: str = Form(...),
    description: str = Form(...),
    unit_price: str = Form(...),
    quantity: str = Form(...),
    current_user: User = Depends(AuthMiddleware),
    db: Session = Depends(get_db)
):
    farmer = db.query(farmers_model.Farmer).filter_by(user_id=current_user.id).first()
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer profile not found")

    product = db.query(products_model.Product).filter_by(id=product_id, farmer_id=farmer.id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.status = status
    product.name = name
    product.description = description
    product.unit_price = float(unit_price)
    product.quantity = int(quantity)
    product.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(product)

    return product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    current_user: User = Depends(AuthMiddleware),
    db: Session = Depends(get_db)
):
    farmer = db.query(farmers_model.Farmer).filter_by(user_id=current_user.id).first()
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer profile not found")

    product = db.query(products_model.Product).filter_by(id=product_id, farmer_id=farmer.id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()

    return