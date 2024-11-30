from sqlalchemy.ext.asyncio import AsyncSession

from crud.basket import BasketCRUD
from models.basket import BasketBase, BasketModel
from models.basket_mushroom import (BasketMushroomId, BasketMushroomModel,
                                    BasketMushroomsModel)
from models.exceptions import ErrorCode
from services.basket_mushroom import BasketMushroomService


class BasketService:
    def __init__(self, basket_crud: BasketCRUD):
        self.basket_crud = basket_crud

    async def create_basket(self, db: AsyncSession, data: BasketBase) -> BasketModel:
        return await self.basket_crud.create_basket(db, data=data)

    async def get_basket_mushroom(
        self,
        db: AsyncSession,
        data: BasketMushroomId,
        basket_mushroom_service: BasketMushroomService,
    ) -> BasketMushroomModel:
        result = BasketMushroomModel()

        result.basket = await self.get_basket(db=db, basket_id=data.basket_id)
        if result.basket is None:
            raise ErrorCode.ITEM_NOT_FOUND.as_http_exception("Корзина не найдена")

        result.mushroom = await basket_mushroom_service.get_mushroom(
            db=db, mushroom_id=data.mushroom_id
        )
        if result.mushroom is None:
            raise ErrorCode.ITEM_NOT_FOUND.as_http_exception("Гриб не найден")

        return result

    async def put_mushroom(
        self,
        db: AsyncSession,
        data: BasketMushroomId,
        basket_mushroom_service: BasketMushroomService,
    ) -> BasketMushroomsModel:
        basket_mushroom = await self.get_basket_mushroom(
            db=db, data=data, basket_mushroom_service=basket_mushroom_service
        )
        basket_params = await basket_mushroom_service.get_basket_params(
            mushrooms=basket_mushroom.basket.mushrooms,
            mushroom_id=basket_mushroom.mushroom.id,
        )

        if basket_params.mushroom_index is not None:
            raise ErrorCode.UNPROCESSABLE_ENTITY.as_http_exception("Гриб уже в корзине")
        elif (
            basket_params.summary_weight + basket_mushroom.mushroom.weight
            > basket_mushroom.basket.volume
        ):
            raise ErrorCode.UNPROCESSABLE_ENTITY.as_http_exception(
                "Гриб не поместится в корзину"
            )

        basket_mushroom.basket.mushrooms.append(basket_mushroom.mushroom)
        return await self.basket_crud.update_basket(db=db, data=basket_mushroom.basket)

    async def delete_mushroom(
        self,
        db: AsyncSession,
        data: BasketMushroomId,
        basket_mushroom_service: BasketMushroomService,
    ) -> BasketMushroomsModel:
        basket_mushroom = await self.get_basket_mushroom(
            db=db, data=data, basket_mushroom_service=basket_mushroom_service
        )
        basket_params = await basket_mushroom_service.get_basket_params(
            mushrooms=basket_mushroom.basket.mushrooms,
            mushroom_id=basket_mushroom.mushroom.id,
        )

        if basket_params.mushroom_index is None:
            raise ErrorCode.ITEM_NOT_FOUND.as_http_exception(
                "Гриб отсутствует в корзине или уже был удален"
            )

        basket_mushroom.basket.mushrooms.pop(basket_params.mushroom_index)
        return await self.basket_crud.update_basket(db=db, data=basket_mushroom.basket)

    async def get_basket(
        self, db: AsyncSession, basket_id: int
    ) -> BasketMushroomsModel:
        basket = await self.basket_crud.get_basket(db=db, basket_id=basket_id)
        if basket is None:
            raise ErrorCode.ITEM_NOT_FOUND.as_http_exception("Корзина не найдена")

        return basket


basket_service = BasketService(basket_crud=BasketCRUD())
