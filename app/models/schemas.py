from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class Color(str, Enum):
    RED = "red"
    BLUE = "blue"
    GREEN = "green"
    BLACK = "black"
    WHITE = "white"
    SILVER = "silver"
    GRAY = "gray"
    OTHER = "other"

class CarSaleBase(BaseModel):
    license_plate: str = Field(..., min_length=6, max_length=10, description="License plate of the vehicle")
    brand: str = Field(..., min_length=2, max_length=50, description="Brand of the vehicle")
    color: Color = Field(..., description="Color of the vehicle")
    price: float = Field(..., gt=0, description="Price of the vehicle in USD")
    sale_date: datetime = Field(default_factory=datetime.now, description="Date and time of the sale")

class CarSaleCreate(CarSaleBase):
    pass

class CarSaleUpdate(BaseModel):
    brand: Optional[str] = Field(None, min_length=2, max_length=50)
    color: Optional[Color] = None
    price: Optional[float] = Field(None, gt=0)

class CarSale(CarSaleBase):
    id: int

    class Config:
        orm_mode = True

class TreeStats(BaseModel):
    height: int
    total_nodes: int
    leaf_count: int
    nodes_per_level: dict[int, int]
