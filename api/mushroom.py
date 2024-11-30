from fastapi import APIRouter, Depends
from pydantic import conint
from sqlalchemy.ext.asyncio import AsyncSession

from models.mushroom import MushroomBase, MushroomModel
from services.basket_mushroom import basket_mushroom_service
from services.mushroom import mushroom_service
from settings import settings

router = APIRouter(prefix="/mushroom")


@router.post("/create_mushroom", response_model=MushroomModel)
async def create_mushroom(
    data: MushroomBase, db: AsyncSession = Depends(settings.db.get_session)
) -> MushroomModel:
    """
    Создаем новый гриб:

    - **name**: Обязательный параметр - Название гриба
    - **eatable**: Необязательный параметр - Съедобность гриба
    - **weight**: Обязательный параметр - Вес гриба в граммах
    - **freshness**: Необязательный параметр - Свежесть гриба в процентах
    """
    return await mushroom_service.create_mushroom(db=db, data=data)


@router.put("/update_mushroom", response_model=MushroomModel)
async def update_mushroom(
    data: MushroomModel, db: AsyncSession = Depends(settings.db.get_session)
) -> MushroomModel:
    """
    Обновляем существующий гриб:

    - **id**: Обязательный параметр - Id гриба
    - **name**: Обязательный параметр - Название гриба
    - **eatable**: Необязательный параметр - Съедобность гриба
    - **weight**: Необязательный параметр - Вес гриба в граммах
    - **freshness**: Необязательный параметр - Свежесть гриба в процентах

    Если гриб с таким id не найден, то получим 404 ошибку;

    Если гриб найден, но из-за увеличения веса он не будет помещаться в корзины, в которые он помещен, то получим 422 ошибку;
    """
    return await mushroom_service.update_mushroom(
        db=db, data=data, basket_mushroom_service=basket_mushroom_service
    )


@router.get("/get_mushroom/{mushroom_id}", response_model=MushroomModel)
async def get_mushroom(
    mushroom_id: conint(gt=0), db: AsyncSession = Depends(settings.db.get_session)
) -> MushroomModel:
    """
    Получаем гриб по id

    Если гриб с таким id не найден, то получим 404 ошибку;
    """
    return await basket_mushroom_service.get_mushroom(db=db, mushroom_id=mushroom_id)
