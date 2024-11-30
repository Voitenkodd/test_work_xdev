from typing import Optional, Sequence

from sqlalchemy import Row, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from models.tables import Baskets, Mushrooms, basket_mushrooms
from settings import db_handler


class BasketMushroomCRUD:

    @db_handler
    async def get_baskets_by_mushroom(
        self, db: AsyncSession, mushroom_id: int
    ) -> Sequence[Row[Optional[Baskets]]]:
        query = (
            select(Baskets)
            .join(basket_mushrooms)
            .filter(basket_mushrooms.c.mushroom_id == mushroom_id)
            .options(joinedload(Baskets.mushrooms))
        )
        result = await db.execute(query)
        baskets = result.unique().scalars().all()
        return baskets

    @db_handler
    async def get_mushroom(
        self, db: AsyncSession, mushroom_id: int
    ) -> Optional[Mushrooms]:
        return await db.get(Mushrooms, mushroom_id)
