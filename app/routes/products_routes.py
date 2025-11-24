from sqlalchemy.orm import Session
from ..database import get_db
from fastapi import APIRouter, HTTPException, status, Depends
from ..models import products_model, users_model, farmers_model, buyers_model, products_category_model
from ..schemas.products_schema import Product, ProductResponse
from ..middlewares.auth import AuthMiddleware
from datetime import datetime
from typing import List



router = APIRouter(tags=["Products"])



@router.post("/products")
def create_product(product: Product, current_user=Depends(AuthMiddleware), db: Session = Depends(get_db)):
    user = db.query(users_model.User).filter(users_model.User.id == current_user.id).first()
    # if not new_product:
    #     raise HTTPException(
    #         status_code = status.HTTP_404_NOT_FOUND,
    #         detail = "User ID does not exists!"
    #     )
 
    db_farmer = db.query(farmers_model.Farmer).filter(farmers_model.Farmer.user_id == current_user.id).first()
    if not db_farmer:
        db_farmer = farmers_model.Farmer(user_id=current_user.id)
        db.add(db_farmer)
        db.commit()
        db.refresh(db_farmer)
    
    db_category = db.query(products_category_model.ProductCategory).filter(products_category_model.ProductCategory.category_name == product.category.value).first()
    if not db_category:
        db_category = products_category_model.ProductCategory(category_name=product.category.value)
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
   

    new_product = products_model.Product(
        **product.model_dump(exclude={"category"}),
        farmer_id = db_farmer.id,
        category_id = db_category.id
        )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.get("/products/{product_id}")
def get_a_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(products_model.Product).filter(products_model.Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Product with ID not found"
        )

    return product

@router.put("/products/{product_id}") # REMEMBER TO CHECK IF A USER CAN UPDATE ANOTHER USER'S PRODUCT
def update_product(product_id: int, product: Product, current_user=Depends(AuthMiddleware), db: Session = Depends(get_db)):
    user = db.query(products_model.Product).filter(products_model.Product.farmer_id == current_user.id).first()
    if not user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Farmer with ID not found"
        )
    updated_product = db.query(products_model.Product).filter(products_model.Product.id == product_id).first()
    if not update_product:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Product with ID not found"
        )
    
    for field, value in product.dict().items():
        setattr(updated_product, field, value)

    db_category = db.query(products_category_model.ProductCategory).filter(products_category_model.ProductCategory.category_name == updated_product.category.value).first()
    if not db_category:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Category to update not found"
        )
    # updated_product.category_id = db_category.id   "OR"
    setattr(updated_product, "category_id", db_category.id)

    db.commit()
    db.refresh(updated_product)
    return updated_product

@router.delete("/products/{product_id}")
def delete_product(product_id: int, current_user=Depends(AuthMiddleware), db: Session = Depends(get_db)):
    user = db.query(products_model.Product).filter(products_model.Product.farmer_id == current_user.id)
    product_to_delete = db.query(products_model.Product).filter(products_model.Product.id == product_id).first()
    if not product_to_delete:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Product with ID not found"
        )


    db.delete(product_to_delete)
    db.commit()
    raise HTTPException(
        status_code = status.HTTP_204_NO_CONTENT,
        detail = "Product deleted successfully"
    )

@router.get("/products")
def get_all_products(db: Session=Depends(get_db)):
    return db.query(products_model.Product).all()
