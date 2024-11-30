from sqlalchemy.ext.asyncio import AsyncSession

from crud.mushroom import MushroomCRUD
from models.exceptions import ErrorCode
from models.mushroom import MushroomBase, MushroomModel
from services.basket_mushroom import BasketMushroomService


class MushroomService:
    def __init__(self, mushroom_crud: MushroomCRUD):
        self.mushroom_crud = mushroom_crud

    async def create_mushroom(
        self, db: AsyncSession, data: MushroomBase
    ) -> MushroomModel:
        return await self.mushroom_crud.create_mushroom(db=db, data=data)

    async def update_mushroom(
        self,
        db: AsyncSession,
        data: MushroomModel,
        basket_mushroom_service: BasketMushroomService,
    ) -> MushroomModel:
        mushroom = await basket_mushroom_service.get_mushroom(
            db=db, mushroom_id=data.id
        )
        if mushroom is None:
            raise ErrorCode.ITEM_NOT_FOUND.as_http_exception("Гриб не найден")

        if data.weight is not None:
            baskets = await basket_mushroom_service.get_baskets_by_mushroom(
                db=db, mushroom_id=mushroom.id
            )
            if baskets:
                for basket in baskets:
                    param = await basket_mushroom_service.get_basket_params(
                        mushrooms=basket.mushrooms
                    )
                    if (
                        param.summary_weight - mushroom.weight + data.weight
                        > basket.volume
                    ):
                        raise ErrorCode.UNPROCESSABLE_ENTITY.as_http_exception(
                            "Гриб не поместится в корзину"
                        )

        data = data.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(mushroom, key, value)

        return await self.mushroom_crud.update_mushroom(db=db, data=mushroom)


mushroom_service = MushroomService(mushroom_crud=MushroomCRUD())
