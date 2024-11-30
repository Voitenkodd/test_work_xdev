from fastapi import APIRouter
from fastapi.params import Depends
from pydantic import conint
from sqlalchemy.ext.asyncio import AsyncSession

from models.basket import BasketBase, BasketModel
from models.basket_mushroom import BasketMushroomId, BasketMushroomsModel
from services.basket import basket_service
from services.basket_mushroom import basket_mushroom_service
from settings import settings

router = APIRouter(prefix="/basket")


@router.post("/create_basket", response_model=BasketModel)
async def create_basket(
    data: BasketBase, db: AsyncSession = Depends(settings.db.get_session)
) -> BasketModel:
    """
    Создаем новую корзину:

    - **owner_name**: Обязательный параметр - Владелец корзины
    - **volume**: Обязательный параметр - Вместительность корзины в граммах
    """
    return await basket_service.create_basket(db=db, data=data)


@router.post("/put_mushroom", response_model=BasketMushroomsModel)
async def put_mushroom(
    data: BasketMushroomId, db: AsyncSession = Depends(settings.db.get_session)
) -> BasketMushroomsModel:
    """
    Кладем гриб в корзину:

    - **basket_id**: Обязательный параметр - Id корзины
    - **mushroom_id**: Обязательный параметр - Id гриба

    Если корзина с таким id не найдена, то получим 404 ошибку;

    Если гриб с таким id не найден, то получим 404 ошибку;

    Если гриб уже находится в корзине, то получим 422 ошибку;

    Если по весу гриб не помещается в корзину, то получим 422 ошибку;
    """
    return await basket_service.put_mushroom(
        db=db, data=data, basket_mushroom_service=basket_mushroom_service
    )


@router.delete("/delete_mushroom", response_model=BasketMushroomsModel)
async def delete_mushroom(
    data: BasketMushroomId, db: AsyncSession = Depends(settings.db.get_session)
) -> BasketMushroomsModel:
    """
    Удаляем гриб из корзины:

    - **basket_id**: Обязательный параметр - Id корзины
    - **mushroom_id**: Обязательный параметр - Id гриба

    Если корзина с таким id не найдена, то получим 404 ошибку;

    Если гриб с таким id не найден, то получим 404 ошибку;

    Если гриб не найден в корзине, то получим 404 ошибку;
    """
    return await basket_service.delete_mushroom(
        db=db, data=data, basket_mushroom_service=basket_mushroom_service
    )


@router.get("/get_basket/{basket_id}", response_model=BasketMushroomsModel)
async def get_basket(
    basket_id: conint(gt=0), db: AsyncSession = Depends(settings.db.get_session)
) -> BasketMushroomsModel:
    """
    Получаем корзину по id

    Если корзина с таким id не найдена, то получим 404 ошибку;
    """
    return await basket_service.get_basket(db=db, basket_id=basket_id)
