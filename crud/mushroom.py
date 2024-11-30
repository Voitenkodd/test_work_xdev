from sqlalchemy.ext.asyncio import AsyncSession

from models.mushroom import MushroomBase, MushroomModel
from models.tables import Mushrooms
from settings import db_handler


class MushroomCRUD:

    @db_handler
    async def create_mushroom(self, db: AsyncSession, data: MushroomBase) -> Mushrooms:
        data = Mushrooms(**data.model_dump(exclude_unset=True))
        db.add(data)
        await db.commit()
        return data

    @db_handler
    async def update_mushroom(self, db: AsyncSession, data: MushroomModel) -> Mushrooms:
        await db.commit()
        await db.refresh(data)
        return data
