from sqlalchemy import Row, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Optional

from crud.basket_mushroom import BasketMushroomCRUD
from models.basket_mushroom import BasketMushroomsModel, BasketParams
from models.exceptions import ErrorCode
from models.mushroom import MushroomModel
from models.tables import Mushrooms


class BasketMushroomService:
    def __init__(self, basket_mushroom_crud: BasketMushroomCRUD):
        self.basket_mushroom_crud = basket_mushroom_crud

    async def get_baskets_by_mushroom(
        self, db: AsyncSession, mushroom_id: int
    ) -> Sequence[Row[Optional[BasketMushroomsModel]]]:
        return await self.basket_mushroom_crud.get_baskets_by_mushroom(
            db=db, mushroom_id=mushroom_id
        )

    @staticmethod
    async def get_basket_params(
        mushrooms: list[Mushrooms], mushroom_id: Optional[int] = None
    ) -> BasketParams:
        basket_params = BasketParams()
        for index, mushroom in enumerate(mushrooms):
            basket_params.mushroom_ids.append(index)
            basket_params.summary_weight += mushroom.weight
            if mushroom_id == mushroom.id:
                basket_params.mushroom_index = index

        return basket_params

    async def get_mushroom(self, db: AsyncSession, mushroom_id: int) -> MushroomModel:
        mushroom = await self.basket_mushroom_crud.get_mushroom(
            db=db, mushroom_id=mushroom_id
        )
        if mushroom is None:
            raise ErrorCode.ITEM_NOT_FOUND.as_http_exception("Гриб не найден")

        return mushroom


basket_mushroom_service = BasketMushroomService(
    basket_mushroom_crud=BasketMushroomCRUD()
)
