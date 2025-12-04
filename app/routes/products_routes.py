from sqlalchemy.orm import Session
from app.enums import ProductCategory
from ..database import get_db
from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status, Depends
from ..models import products_model, users_model, farmers_model, buyers_model, products_category_model
from ..middlewares.auth import AuthMiddleware
from datetime import datetime
from typing import List
import cloudinary.uploader
from ..models.users_model import User


router = APIRouter(tags=["Products"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(
    category: ProductCategory = Form(...),
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

    # Validate image type
    allowed_ext = {"jpg", "jpeg", "png"}
    file_ext = image.filename.split(".")[-1].lower() 
    if file_ext not in allowed_ext:
        raise HTTPException(status_code=400, detail="Only jpg/jpeg/png allowed")

    # Validate file type
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    # Read image contents
    contents = await image.read()
    
    # Check size (2MB limit)
    image_size = 2 * 1024 * 1024
    if len(contents) > image_size:
        raise HTTPException(status_code=400, detail="Image size exceeds 2 MB limit")

    # Upload to Cloudinary
    try:
        result = cloudinary.uploader.upload(
            contents,
            folder=f"payit/products/farmer_{farmer.id}",
            resource_type="auto",
            transformation=[
                {"width": 800, "height": 800, "crop": "limit"},
                {"quality": "auto"}
            ]
        )
        image_url = result["secure_url"]
        cloudinary_public_id = result["public_id"]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image upload failed: {str(e)}")

    
    new_product = products_model.Product(
        farmer_id=farmer.id, 
        category=category,
        status=status,
        name=name,
        image_url=image_url,  
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
        "product": new_product,
        "image_url": image_url
    }

@router.get("/getProduct")
def get_all_products(
    db: Session = Depends(get_db)
):
    products = db.query(products_model.Product).all()
    return products


@router.get("/category/{category}")
def get_products_by_category(
    category: ProductCategory,
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
async def update_product(
    product_id: int,
    status: str = Form(...),
    name: str = Form(...),
    description: str = Form(...),
    unit_price: str = Form(...),
    quantity: str = Form(...),
    image: UploadFile = File(None), 
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

    
    if image:
        allowed_ext = {"jpg", "jpeg", "png"}
        file_ext = image.filename.split(".")[-1].lower() 
        if file_ext not in allowed_ext:
            raise HTTPException(status_code=400, detail="Only jpg/jpeg/png allowed")

        if not image.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")

        contents = await image.read()
        
        image_size = 2 * 1024 * 1024
        if len(contents) > image_size:
            raise HTTPException(status_code=400, detail="Image size exceeds 2 MB limit")

        try:
            # Delete old image from Cloudinary if it exists
            if product.image_url and "cloudinary.com" in product.image_url:
                # Extract public_id from URL
                # Example: https://res.cloudinary.com/xxx/image/upload/v123/payit/products/farmer_1/abc.jpg
                # public_id would be: payit/products/farmer_1/abc
                parts = product.image_url.split("/upload/")
                if len(parts) > 1:
                    public_id = parts[1].split(".")[0]
                    if "/v" in public_id:
                        public_id = "/".join(public_id.split("/")[1:])
                    try:
                        cloudinary.uploader.destroy(f"payit/products/farmer_{farmer.id}/{public_id.split('/')[-1]}")
                    except:
                        pass  # If deletion fails, continue anyway

            # Upload new image
            result = cloudinary.uploader.upload(
                contents,
                folder=f"payit/products/farmer_{farmer.id}",
                resource_type="auto",
                transformation=[
                    {"width": 800, "height": 800, "crop": "limit"},
                    {"quality": "auto"}
                ]
            )
            product.image_url = result["secure_url"]
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Image upload failed: {str(e)}")

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

    # Delete image from Cloudinary before deleting product
    if product.image_url and "cloudinary.com" in product.image_url:
        parts = product.image_url.split("/upload/")
        if len(parts) > 1:
            public_id = parts[1].split(".")[0]
            if "/v" in public_id:
                public_id = "/".join(public_id.split("/")[1:])
            try:
                cloudinary.uploader.destroy(public_id)
            except:
                pass  

    db.delete(product)
    db.commit()

    return