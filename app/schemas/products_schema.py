# from pydantic import BaseModel, Field, validator
# from datetime import datetime
# from ..enums import Category

# class Product(BaseModel):
#     name: str = Field(min_length=2)
#     unit_price: float
#     quantity: int
#     category: Category

# class ProductResponse(Product):
#     created_at: datetime
#     updated_at: datetime