from pydantic import BaseModel


class ProductionDTO(BaseModel):
    id: int | None = None
    name: str
    quantity: int | None
    year: int
    category_id: int