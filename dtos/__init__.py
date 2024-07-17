from pydantic import BaseModel


class CategoryDTO(BaseModel):
    name: str
    meta_name: str

class ProductionDTO(BaseModel):
    id: int | None = None
    name: str
    quantity: int | None
    year: int
    category_id: int

class ProductionDTOResponse(BaseModel):
    id: int | None = None
    name: str
    quantity: int | None
    year: int
    category: CategoryDTO

