from pydantic import BaseModel, Field, validator, model_validator
from fastapi import HTTPException


class Order(BaseModel):
    product_name: str
    quantity: int = Field(ge=1)


    @validator('quantity')
    def quantity_is_not_zero(cls, value):
        if value < 1:
            raise HTTPException(
                status_code = status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail = "Quantity can not be zero or less than 1!")
        return value