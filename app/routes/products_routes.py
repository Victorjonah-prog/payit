from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator
from ..database import db_dependency
from ..models.products import Products
from typing import List


router = APIRouter()


class ProductCreate(BaseModel):
    user_id: int
    name: str = Field(min_length=3, max_length=50)
    price: float = Field(gt=0)           
    quantity: int = Field(ge=1)          
    category: str = Field(min_length=3)

    @field_validator("name")
    def validate_name(cls, value):
        if not value.replace(" ", "").isalpha():
            raise ValueError("Product name must contain only letters and spaces")
        return value

    @field_validator("category")
    def validate_category(cls, value):
        allowed = ["electronics","tubers", "grains","clothing","fruits","oils","synthetic","livestock","cereals","vegetables","latex", "food", "furniture", "services"]
        if value.lower() not in allowed:
            raise ValueError(f"Category must be one of: {', '.join(allowed)}")
        return value.lower()

    model_config = {
        "from_attributes": True
    }


@router.post("/products/", response_model=ProductCreate)
def create_product(product: ProductCreate, db: db_dependency):

    
    db_product = db.query(Products).filter(Products.name == product.name).first()
    if db_product:
        raise HTTPException(status_code=400, detail="Product already registered")

    db_product = Products(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.get("/products/", response_model=List[ProductCreate])
def get_all_products(db: db_dependency):
    products = db.query(Products).all()
    return products

@router.get("/products/{product_id}", response_model=ProductCreate)
def get_product_by_id(product_id: int, db: db_dependency):
    product = db.query(Products).filter(Products.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: db_dependency):
    product = db.query(Products).filter(Products.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}

@router.get("/users/{user_id}/products", response_model=List[ProductCreate])
def get_products_by_user(user_id: int, db: db_dependency):
    products = db.query(Products).filter(Products.user_id == user_id).all()

    if not products:
        raise HTTPException(status_code=404, detail="No products found for this user")

    return products

@router.put("/products/{product_id}", response_model=ProductCreate)
def update_product(product_id: int, product: ProductCreate, db: db_dependency):
    db_product = db.query(Products).filter(Products.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="product not found")
    for key, value in product.dict().items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product