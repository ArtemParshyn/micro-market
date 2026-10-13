from pydantic import BaseModel, field_validator, ConfigDict
from decimal import Decimal


# --- Категории ---

class RequestCreateCategory(BaseModel):
    name: str

    @field_validator("name", mode="before")
    @classmethod
    def strip_name(cls, v: str) -> str:
        if len(v.strip()) < 1:
            raise ValueError("Name must not be empty.")
        return v.strip()


class ResponseCategory(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


# --- Модификаторы и добавки ---

class RequestCreateModifier(BaseModel):
    name: str
    price: Decimal = Decimal("0.00")
    weight_grams: int | None = None
    is_available: bool = True

    @field_validator("name", mode="before")
    @classmethod
    def strip_name(cls, v: str) -> str:
        if len(v.strip()) < 1:
            raise ValueError("Name must not be empty.")
        return v.strip()

    @field_validator('price', mode="after")
    def price_not_negative(cls, v: Decimal) -> Decimal:
        if v < Decimal(0):
            raise ValueError('Price cannot be lower than 0.')
        return v


class ResponseModifier(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    price: Decimal
    weight_grams: int | None = None
    is_available: bool


class RequestUpdateAvailability(BaseModel):
    is_available: bool


# --- Изображения ---

class ImageConfirmRequest(BaseModel):
    object_name: str
    filename: str
    mime: str
    size: int


class ImageUploadRequest(BaseModel):
    filename: str
    mime: str


class ImageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    upload_url: str
    object_name: str


# --- Продукты ---

class RequestCreateProduct(BaseModel):
    name: str
    price: Decimal
    description: str
    category_id: int
    weight_grams: int | None = None
    pieces_count: int | None = None
    calories: int | None = None
    spicy: bool = False
    vegetarian: bool = False
    is_available: bool = True
    modifier_ids: list[int] = []
    image: ImageConfirmRequest | None = None

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
    def price_must_be_positive(cls, v: Decimal) -> Decimal:
        if v <= Decimal(0):
            raise ValueError('Price cannot be lower than 0.')
        return v


class ResponseProduct(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    price: Decimal
    description: str
    category_id: int
    weight_grams: int | None = None
    pieces_count: int | None = None
    calories: int | None = None
    spicy: bool = False
    vegetarian: bool = False
    is_available: bool = True
    image_url: str | None = None
    modifiers: list[ResponseModifier] = []