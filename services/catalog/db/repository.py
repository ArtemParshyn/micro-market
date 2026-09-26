from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from services.catalog.app.schemes import RequestCreateProduct, RequestCreateCategory
from services.catalog.db.models import Product, Category

async def db_get_product(db: AsyncSession, id_product: int):
    product = await db.execute(select(Product).where(Product.id == id_product))
    return product.scalars().one()

async def db_get_all_products(db: AsyncSession):
    products = await db.execute(select(Product))
    return list(products.scalars().all())

async def db_create_products(db: AsyncSession, product: RequestCreateProduct):
    product = Product(
        name=product.name,
        price=product.price,
        description=product.description,
        category_id=product.category_id
    )
    db.add(product)
    await db.flush()
    return product

async def db_get_all_categories(db: AsyncSession):
    categories = await db.execute(select(Category))
    return list(categories.scalars().all())

async def db_create_category(db: AsyncSession, category: RequestCreateCategory):
    category = Category(name=category.name)
    db.add(category)
    await db.flush()
    return category

async def db_get_all_products_via_category(db: AsyncSession, id_category: int):
    products = await db.execute(select(Product).where(Product.category_id == id_category))
    return list(products.scalars().all())

