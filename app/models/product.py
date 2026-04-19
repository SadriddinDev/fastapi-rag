from sqlalchemy import String, Integer, ForeignKey, DateTime, Enum, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.models.enums import ProductCategory


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    name: Mapped[str] = mapped_column(String, index=True)
    price: Mapped[int] = mapped_column(Integer)

    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    category: Mapped[ProductCategory] = mapped_column(
        Enum(ProductCategory),
        default=ProductCategory.other
    )

    definition: Mapped[str | None] = mapped_column(Text, nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    created_at: Mapped[str] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[str] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    images = relationship(
        "ProductImage",
        back_populates="product",
        cascade="all, delete",
        lazy="selectin"
    )
