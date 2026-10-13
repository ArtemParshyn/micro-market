from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import Column, Integer, Numeric, ForeignKey, Table, Boolean
from sqlalchemy.orm import mapped_column, Mapped, relationship

from services.catalog.db.database import Base


product_modifiers = Table(
    "product_modifiers",
    Base.metadata,
    Column("product_id", Integer, ForeignKey("products.id", ondelete="CASCADE"), primary_key=True),
    Column("modifier_id", Integer, ForeignKey("modifiers.id", ondelete="CASCADE"), primary_key=True),
)


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    products: Mapped[list["Product"]] = relationship("Product", back_populates="category")


class Modifier(Base):
    """Модификатор / соус / дополнение к суши или заказу (соевый соус, васаби, палочки, сыр и т.д.)."""
    __tablename__ = 'modifiers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0.00"), server_default="0.00")
    weight_grams: Mapped[Optional[int]] = mapped_column(nullable=True)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true")

    products: Mapped[list["Product"]] = relationship(
        "Product",
        secondary=product_modifiers,
        back_populates="modifiers",
    )


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    description: Mapped[str] = mapped_column()
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category: Mapped["Category"] = relationship("Category", back_populates="products")

    # Специфика суши/роллов
    weight_grams: Mapped[Optional[int]] = mapped_column(nullable=True)
    pieces_count: Mapped[Optional[int]] = mapped_column(nullable=True)
    calories: Mapped[Optional[int]] = mapped_column(nullable=True)
    spicy: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    vegetarian: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true")

    # Медиа в MinIO
    image_object_name: Mapped[Optional[str]] = mapped_column(nullable=True)
    image_mime: Mapped[Optional[str]] = mapped_column(nullable=True)
    image_size_bytes: Mapped[Optional[int]] = mapped_column(nullable=True)

    # Доступные модификаторы
    modifiers: Mapped[list["Modifier"]] = relationship(
        "Modifier",
        secondary=product_modifiers,
        back_populates="products",
        lazy="selectin",
    )
