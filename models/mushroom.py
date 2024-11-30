from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class MushroomBase(BaseModel):
    name: str = Field(max_length=64, description="Название гриба")
    eatable: Optional[bool] = Field(default=None, description="Съедобность гриба")
    weight: int = Field(gt=0, description="Вес гриба в граммах")
    freshness: Optional[Decimal] = Field(
        default=None, ge=0, le=100, description="Свежесть гриба в процентах"
    )

    class Config:
        orm_mode = True


class MushroomModel(MushroomBase):
    id: int = Field(gt=0)
    weight: Optional[int] = Field(default=None, gt=0, description="Вес гриба в граммах")
