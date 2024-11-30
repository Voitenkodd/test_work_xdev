from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from models.basket import BasketBase
from models.basket_mushroom import BasketMushroomsModel
from models.tables import Baskets
from settings import db_handler


class BasketCRUD:

    @db_handler
    async def create_basket(self, db: AsyncSession, data: BasketBase) -> Baskets:
        data = Baskets(**data.model_dump(exclude_unset=True))
        db.add(data)
        await db.commit()
        return data

    @db_handler
    async def update_basket(
        self, db: AsyncSession, data: BasketMushroomsModel
    ) -> Baskets:
        await db.commit()
        await db.refresh(data)
        return data

    @db_handler
    async def get_basket(self, db: AsyncSession, basket_id: int) -> Optional[Baskets]:
        query = (
            select(Baskets)
            .options(joinedload(Baskets.mushrooms))
            .filter_by(id=basket_id)
        )
        basket = await db.execute(query)
        basket = basket.unique().scalar_one_or_none()
        return basket
