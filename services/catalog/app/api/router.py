from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import DbSession
from services.catalog.app.schemes import ResponseProduct, RequestCreateProduct, ResponseCategory, RequestCreateCategory
from services.catalog.app.service import service_get_products, service_create_products, service_get_all_categories, \
    service_create_category, service_get_all_products_via_category, service_get_product

router = APIRouter()

@router.get("/products/{id_product}", response_model=ResponseProduct)
async def get_product(db: DbSession, id_product: int):
    return await service_get_product(db=db, id_product=id_product)

@router.get("/products", response_model=list[ResponseProduct])
async def get_all_products(db: DbSession):
    return await service_get_products(db=db)

@router.post("/products", response_model=ResponseProduct)
async def create_product(db: DbSession, product: RequestCreateProduct):
    return await service_create_products(db=db, product=product)

@router.get("/categories", response_model=list[ResponseCategory])
async def get_all_categories(db: DbSession):
    return await service_get_all_categories(db=db)

@router.post("/categories", response_model=ResponseCategory)
async def create_category(db: DbSession, category: RequestCreateCategory):
    return await service_create_category(db=db, category=category)

@router.get("/categories/{id_category}/products", response_model=list[ResponseProduct])
async def get_all_products_via_category(db: DbSession, id_category: int):
    return await service_get_all_products_via_category(db=db, id_category=id_category)
