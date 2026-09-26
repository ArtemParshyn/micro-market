from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from services.catalog.app.schemes import RequestCreateProduct, RequestCreateCategory
from services.catalog.db.repository import db_get_all_products, db_create_products, db_get_product, \
    db_get_all_categories, db_create_category, db_get_all_products_via_category


async def service_get_product(db: AsyncSession, id_product: int):
    return await db_get_product(db=db, id_product=id_product)

async def service_get_products(db: AsyncSession):
    return await db_get_all_products(db)

async def service_create_products(db: AsyncSession, product: RequestCreateProduct):
    try:
        product = await db_create_products(db=db, product=product)
        await db.commit()
        await db.refresh(product)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Product already exists")
    return product

async def service_get_all_categories(db: AsyncSession):
    return await db_get_all_categories(db=db)

async def service_create_category(db: AsyncSession, category: RequestCreateCategory):
    try:
        category = await db_create_category(db=db, category=category)
        await db.commit()
        await db.refresh(category)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Category already exists")
    return category

async def service_get_all_products_via_category(db: AsyncSession, id_category: int):
    return await db_get_all_products_via_category(db=db, id_category=id_category)
