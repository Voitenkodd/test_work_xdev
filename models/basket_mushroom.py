from typing import Optional

from pydantic import BaseModel, Field

from models.basket import BasketModel
from models.mushroom import MushroomModel


class BasketParams(BaseModel):
    summary_weight: int = Field(default=0)
    mushroom_index: Optional[int] = Field(default=None)
    mushroom_ids: list = Field(default=[])


class BasketMushroomModel(BaseModel):
    basket: Optional[BasketModel] = Field(default=None)
    mushroom: Optional[MushroomModel] = Field(default=None)


class BasketMushroomsModel(BasketModel):
    mushrooms: Optional[list[MushroomModel]] = Field(default=None)


class BasketMushroomId(BaseModel):
    basket_id: int = Field(gt=0)
    mushroom_id: int = Field(gt=0)
