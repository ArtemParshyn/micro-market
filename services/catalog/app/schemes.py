from pydantic import BaseModel, field_validator, ConfigDict
from decimal import Decimal

class RequestCreateCategory(BaseModel):
    name: str

    @field_validator("name", mode="before")
    @classmethod
    def strip_description(cls, v: str) -> str:
        if len(v.strip()) < 1:
            raise ValueError("Name must not be empty.")
        return v.strip()

class ResponseCategory(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str

class ResponseProduct(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    price: Decimal
    description: str

class RequestCreateProduct(BaseModel):
    name: str
    price: Decimal
    description: str
    category_id: int

    @field_validator("name", mode="before")
    @classmethod
    def strip_name(cls, v: str) -> str:
        if len(v.strip()) < 1:
            raise ValueError("Name must not be empty.")
        return v.strip()

    @field_validator("description", mode="before")
    @classmethod
    def strip_description(cls, v: str) -> str:
        if len(v.strip()) < 1:
            raise ValueError("Name must not be empty.")
        return v.strip()

    @field_validator('price', mode="after")
    def description_must_bigger_than_0(cls, v: Decimal) -> Decimal:
        if v <= Decimal(0):
            raise ValueError('Price cannot be lower than 0.')
        return v
