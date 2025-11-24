from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..middlewares.auth import AuthMiddleware
from ..models import users_model
from ..models import orders_model
from ..models import buyers_model
from ..models import products_model
from ..schemas.orders_schema import Order
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(tags=["Orders"])

@router.post("/orders")
def order_product(order: Order, current_user=Depends(AuthMiddleware), db: Session= Depends(get_db)):
    # product_available = db.query(products_model.Product).filter((products_model.Product.name == order.product_name)|
    # (products_model.Product.quantity == 0)).first()
    product_available = db.query(products_model.Product).filter(products_model.Product.name == order.product_name).first()
    if not product_available:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Product not found or out of stock"
        )

    new_buyer = db.query(buyers_model.Buyer).filter(buyers_model.Buyer.user_id == current_user.id)
    new_buyer = buyers_model.Buyer(user_id = current_user.id)
    db.add(new_buyer)
    db.commit()
    db.refresh(new_buyer)
    
    new_order = orders_model.Order(
        **order.model_dump(exclude={"product_name"}),
        product_id = product_available.id,
        buyer_id = new_buyer.id,
        unit_price = product_available.unit_price,
        order_status = "pending",
        amount = product_available.unit_price * order.quantity
    )
    
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


@router.get("/orders/{order_id}")
def get_an_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(orders_model.Order).filter(orders_model.Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Order with ID not found"
        )

    return order


@router.delete("/orders/{order_id}")
def cancel_order(order_id: int, current_user = Depends(AuthMiddleware), db: Session = Depends(get_db)):
    buyer_exists = db.query(buyers_model.Buyer).filter(buyers_model.Buyer.user_id == current_user.id).first()
    if not buyer_exists:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Buyer ID not found"
        )
    order_exists = db.query(orders_model.Order).filter(orders_model.Order.id == order_id).first()
    if not order_exists:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Order ID not found!"
        )

    if order_exists.order_status.value == 'delivered':
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Can not cancel. Order already processed!"
            )
    else:
        db.delete(order_exists)
        db.commit()
        raise HTTPException(
        status_code = status.HTTP_204_NO_CONTENT,
        detail = "Order cancelled!"
        )

    
@router.get("/orders")
def get_all_orders(db: Session=Depends(get_db)):
    return db.query(orders_model.Order).all()
   
   