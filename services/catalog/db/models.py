from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import Column, Integer, Numeric, ForeignKey, Null
from sqlalchemy.orm import mapped_column, Mapped, relationship

from services.catalog.db.database import Base

class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    products: Mapped[list["Product"]] = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    description: Mapped[str] = mapped_column()
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category: Mapped["Category"] = relationship("Category", back_populates="products")
    image_object_name: Mapped[Optional[str]] = mapped_column()
    image_mime: Mapped[Optional[str]] = mapped_column()
    image_size_bytes: Mapped[Optional[int]] = mapped_column()


#class ProductImage(Base):
#    __tablename__ = 'products_images'
#
#    id: Mapped[int] = mapped_column(primary_key=True)
#    product_id = mapped_column(ForeignKey("products.id"))
#    file_name: Mapped[str] = mapped_column()
#    size_bytes: Mapped[Decimal] = mapped_column()
#    is_primary: Mapped[bool] = mapped_column()
#    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
#    product: Mapped["Product"] = relationship("Product", back_populates="images")
