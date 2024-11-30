from decimal import Decimal

from sqlalchemy import (Boolean, Column, ForeignKey, Integer, Numeric, String,
                        Table)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship

Base = declarative_base()

basket_mushrooms = Table(
    "basket_mushrooms",
    Base.metadata,
    Column("basket_id", ForeignKey("baskets.id"), primary_key=True),
    Column("mushroom_id", ForeignKey("mushrooms.id"), primary_key=True),
)


class Mushrooms(Base):
    __tablename__ = "mushrooms"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    eatable: Mapped[bool] = mapped_column(Boolean, nullable=True)
    weight: Mapped[int] = mapped_column(Integer, nullable=False)
    freshness: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=True)

    baskets = relationship(
        "Baskets", secondary=basket_mushrooms, back_populates="mushrooms"
    )


class Baskets(Base):
    __tablename__ = "baskets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    owner_name: Mapped[str] = mapped_column(String(64), nullable=False)
    volume: Mapped[int] = mapped_column(Integer, nullable=False)

    mushrooms = relationship(
        "Mushrooms", secondary=basket_mushrooms, back_populates="baskets"
    )
