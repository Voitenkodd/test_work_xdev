from pydantic import BaseModel, Field


class BasketBase(BaseModel):
    owner_name: str = Field(max_length=64, description="Владелец корзины")
    volume: int = Field(gt=0, description="Вместительность корзины в граммах")

    class Config:
        orm_mode = True


class BasketModel(BasketBase):
    id: int = Field(gt=0)
