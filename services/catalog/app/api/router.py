from fastapi import APIRouter, Query
from services.catalog.app.schemes import (
    ResponseProduct,
    RequestCreateProduct,
    ResponseCategory,
    RequestCreateCategory,
    ImageUploadRequest,
    ImageResponse,
    ImageConfirmRequest,
    ResponseModifier,
    RequestCreateModifier,
    RequestUpdateAvailability,
)
from services.catalog.app.service import (
    service_get_products,
    service_create_products,
    service_get_all_categories,
    service_create_category,
    service_get_all_products_via_category,
    service_get_product,
    service_get_upload_url,
    service_confirm_image,
    service_update_product_availability,
    service_get_all_modifiers,
    service_create_modifier,
    service_update_modifier_availability,
)
from services.catalog.db.database import DbSession

router = APIRouter()


# --- Товары ---

@router.get("/products/{id_product}", response_model=ResponseProduct)
async def get_product(db: DbSession, id_product: int):
    return await service_get_product(db=db, id_product=id_product)


@router.get("/products", response_model=list[ResponseProduct])
async def get_all_products(
    db: DbSession,
    available_only: bool = Query(default=False, description="Показывать только товары в наличии (исключить стоп-лист)"),
):
    return await service_get_products(db=db, available_only=available_only)


@router.post("/products", response_model=ResponseProduct)
async def create_product(db: DbSession, product: RequestCreateProduct):
    return await service_create_products(db=db, product=product)


@router.patch("/products/{id_product}/availability", response_model=ResponseProduct)
async def update_product_availability(db: DbSession, id_product: int, body: RequestUpdateAvailability):
    """Переключение статуса доступности товара (добавить/убрать из стоп-листа)."""
    return await service_update_product_availability(db=db, id_product=id_product, is_available=body.is_available)


# --- Категории ---

@router.get("/categories", response_model=list[ResponseCategory])
async def get_all_categories(db: DbSession):
    return await service_get_all_categories(db=db)


@router.post("/categories", response_model=ResponseCategory)
async def create_category(db: DbSession, category: RequestCreateCategory):
    return await service_create_category(db=db, category=category)


@router.get("/categories/{id_category}/products", response_model=list[ResponseProduct])
async def get_all_products_via_category(
    db: DbSession,
    id_category: int,
    available_only: bool = Query(default=False, description="Показывать только товары в наличии"),
):
    return await service_get_all_products_via_category(db=db, id_category=id_category, available_only=available_only)


# --- Модификаторы и соусы ---

@router.get("/modifiers", response_model=list[ResponseModifier])
async def get_all_modifiers(
    db: DbSession,
    available_only: bool = Query(default=False, description="Показывать только модификаторы в наличии"),
):
    return await service_get_all_modifiers(db=db, available_only=available_only)


@router.post("/modifiers", response_model=ResponseModifier)
async def create_modifier(db: DbSession, modifier: RequestCreateModifier):
    return await service_create_modifier(db=db, modifier=modifier)


@router.patch("/modifiers/{id_modifier}/availability", response_model=ResponseModifier)
async def update_modifier_availability(db: DbSession, id_modifier: int, body: RequestUpdateAvailability):
    """Переключение доступности модификатора (стоп-лист на соус/добавку)."""
    return await service_update_modifier_availability(db=db, id_modifier=id_modifier, is_available=body.is_available)


# --- Медиа и изображения ---

@router.post("/images/upload-url", response_model=ImageResponse)
async def get_upload_url(uploadrequest: ImageUploadRequest):
    return await service_get_upload_url(uploadrequest=uploadrequest)


@router.post("/images/confirm", response_model=dict)
async def confirm_image(image: ImageConfirmRequest):
    return await service_confirm_image(image=image)
