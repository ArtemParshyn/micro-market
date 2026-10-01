from datetime import timedelta
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException
from minio import S3Error
from minio.commonconfig import CopySource
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from services.catalog.app.schemes import RequestCreateProduct, RequestCreateCategory, ImageUploadRequest, \
    ImageConfirmRequest
from services.catalog.db.models import Product
from services.catalog.db.repository import db_get_all_products, db_create_products, db_get_product, \
    db_get_all_categories, db_create_category, db_get_all_products_via_category
from services.catalog.tasks import client as minio_client

BUCKET = "catalog-images"


async def service_get_product(db: AsyncSession, id_product: int):
    product_obj = await db_get_product(db=db, id_product=id_product)
    if product_obj.image_object_name:
        product_obj.image_url = minio_client.presigned_get_object(
            bucket_name=BUCKET,
            object_name=product_obj.image_object_name,
            expires=timedelta(hours=1),
        )
    else:
        product_obj.image_url = None
    return product_obj


async def service_get_products(db: AsyncSession):
    return await db_get_all_products(db)


async def validate_image_in_minio(object_name: str, size: int, mime: str) -> None:
    """Проверяет, что файл существует в MinIO и соответствует размеру/MIME."""
    try:
        stat = minio_client.stat_object(BUCKET, object_name)
    except S3Error as e:
        if e.code == "NoSuchKey":
            raise HTTPException(404, "File not found in MinIO")
        raise

    if stat.size != size:
        raise HTTPException(400, f"Size mismatch: expected {size}, got {stat.size}")
    if stat.content_type != mime:
        raise HTTPException(400, f"MIME mismatch: expected {mime}, got {stat.content_type}")


async def service_confirm_image(image: ImageConfirmRequest) -> dict:
    await validate_image_in_minio(image.object_name, image.size, image.mime)
    return {"status": "ok", "object_name": image.object_name}


async def service_get_upload_url(uploadrequest: ImageUploadRequest) -> dict:
    """Возвращает presigned PUT URL для загрузки во временную зону."""
    ext = Path(uploadrequest.filename).suffix.lower()
    if not ext:
        ext = ".jpg"
    object_name = f"uploads/temp/{uuid4().hex}{ext}"

    upload_url = minio_client.presigned_put_object(
        bucket_name=BUCKET,
        object_name=object_name,
        expires=timedelta(minutes=10),
    )
    return {"upload_url": upload_url, "object_name": object_name}


async def service_create_products(db: AsyncSession, product: RequestCreateProduct) -> Product:
    # 1. Создаём товар
    product_obj = Product(
        name=product.name,
        price=product.price,
        description=product.description,
        category_id=product.category_id,
    )
    db.add(product_obj)
    await db.flush()  # получаем product_obj.id

    # 2. Если передано фото — обрабатываем
    if product.image:
        await validate_image_in_minio(product.image.object_name, product.image.size, product.image.mime)

        # Копируем temp → products/{id}/
        ext = Path(product.image.filename).suffix.lower()
        if not ext:
            ext = ".jpg"
        final_name = f"products/{product_obj.id}/{uuid4().hex}{ext}"

        minio_client.copy_object(
            BUCKET,
            final_name,
            CopySource(bucket_name=BUCKET, object_name=product.image.object_name),
        )
        # Удаляем временный файл
        minio_client.remove_object(BUCKET, product.image.object_name)

        # Сохраняем метаданные в товаре
        product_obj.image_object_name = final_name
        product_obj.image_mime = product.image.mime
        product_obj.image_size_bytes = product.image.size

    # 3. Коммитим
    try:
        await db.commit()
        await db.refresh(product_obj)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(400, "Product creation failed")
    except S3Error:
        await db.rollback()
        raise HTTPException(500, "Problem with image storage")

    # Генерируем presigned GET URL для фото
    if product_obj.image_object_name:
        product_obj.image_url = minio_client.presigned_get_object(
            bucket_name=BUCKET,
            object_name=product_obj.image_object_name,
            expires=timedelta(hours=1),
        )
    else:
        product_obj.image_url = None

    return product_obj


async def service_get_all_categories(db: AsyncSession):
    return await db_get_all_categories(db=db)


async def service_create_category(db: AsyncSession, category: RequestCreateCategory):
    try:
        category = await db_create_category(db=db, category=category)
        await db.commit()
        await db.refresh(category)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(400, "Category already exists")
    return category


async def service_get_all_products_via_category(db: AsyncSession, id_category: int):
    return await db_get_all_products_via_category(db=db, id_category=id_category)