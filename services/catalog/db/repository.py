from typing import Sequence
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from services.catalog.app.schemes import RequestCreateProduct, RequestCreateCategory, RequestCreateModifier
from services.catalog.db.models import Product, Category, Modifier


# --- Товары ---

async def db_get_product(db: AsyncSession, id_product: int) -> Product | None:
    result = await db.execute(
        select(Product)
        .options(selectinload(Product.modifiers))
        .where(Product.id == id_product)
    )
    return result.scalar_one_or_none()


async def db_get_all_products(
    db: AsyncSession,
    available_only: bool = False,
    category_id: int | None = None,
) -> list[Product]:
    stmt = select(Product).options(selectinload(Product.modifiers))
    if available_only:
        stmt = stmt.where(Product.is_available.is_(True))
    if category_id is not None:
        stmt = stmt.where(Product.category_id == category_id)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def db_create_products(
    db: AsyncSession,
    product: RequestCreateProduct,
    modifiers: Sequence[Modifier] = (),
) -> Product:
    product_new = Product(
        name=product.name,
        price=product.price,
        description=product.description,
        category_id=product.category_id,
        weight_grams=product.weight_grams,
        pieces_count=product.pieces_count,
        calories=product.calories,
        spicy=product.spicy,
        vegetarian=product.vegetarian,
        is_available=product.is_available,
        modifiers=list(modifiers),
    )
    db.add(product_new)
    await db.flush()
    return product_new


async def db_update_product_availability(db: AsyncSession, id_product: int, is_available: bool) -> Product | None:
    product = await db_get_product(db=db, id_product=id_product)
    if product:
        product.is_available = is_available
        await db.flush()
    return product


# --- Категории ---

async def db_get_all_categories(db: AsyncSession) -> list[Category]:
    categories = await db.execute(select(Category))
    return list(categories.scalars().all())


async def db_get_category(db: AsyncSession, id_category: int) -> Category | None:
    result = await db.execute(select(Category).where(Category.id == id_category))
    return result.scalar_one_or_none()


async def db_create_category(db: AsyncSession, category: RequestCreateCategory) -> Category:
    category_new = Category(name=category.name)
    db.add(category_new)
    await db.flush()
    return category_new


async def db_get_all_products_via_category(
    db: AsyncSession,
    id_category: int,
    available_only: bool = False,
) -> list[Product]:
    return await db_get_all_products(db=db, available_only=available_only, category_id=id_category)


# --- Модификаторы и соусы ---

async def db_get_modifier(db: AsyncSession, id_modifier: int) -> Modifier | None:
    result = await db.execute(select(Modifier).where(Modifier.id == id_modifier))
    return result.scalar_one_or_none()


async def db_get_modifiers_by_ids(db: AsyncSession, modifier_ids: list[int]) -> Sequence[Modifier]:
    if not modifier_ids:
        return []
    result = await db.execute(select(Modifier).where(Modifier.id.in_(modifier_ids)))
    return result.scalars().all()


async def db_get_all_modifiers(db: AsyncSession, available_only: bool = False) -> list[Modifier]:
    stmt = select(Modifier)
    if available_only:
        stmt = stmt.where(Modifier.is_available.is_(True))
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def db_create_modifier(db: AsyncSession, modifier: RequestCreateModifier) -> Modifier:
    mod_new = Modifier(
        name=modifier.name,
        price=modifier.price,
        weight_grams=modifier.weight_grams,
        is_available=modifier.is_available,
    )
    db.add(mod_new)
    await db.flush()
    return mod_new


async def db_update_modifier_availability(db: AsyncSession, id_modifier: int, is_available: bool) -> Modifier | None:
    modifier = await db_get_modifier(db=db, id_modifier=id_modifier)
    if modifier:
        modifier.is_available = is_available
        await db.flush()
    return modifier

