from pydantic import BaseModel


# Categories
class CategoryDTO(BaseModel):
    name: str
    meta_name: str


class CategoryWithIdDTO(CategoryDTO):
    id: int


# Country
class CountryDTO(BaseModel):
    name: str

# Product
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


# Processing
class ProcessingDTO(BaseModel):
    id: int | None = None
    cultivation: str
    quantity: int | None
    year: int
    category_id: int
    grape_class_id: int


class ProcessingDTOResponse(BaseModel):
    id: int | None = None
    cultivation: str
    quantity: int | None
    year: int
    category: CategoryDTO
    grape_class: CategoryDTO

# Sale
class SaleDTO(BaseModel):
    id: int | None = None
    name: str
    quantity: int | None
    year: int
    category_id: int


class SaleDTOResponse(BaseModel):
    id: int | None = None
    name: str
    quantity: int | None
    year: int
    category: CategoryDTO

# Exports
class ExportDTO(BaseModel):
    id: int | None = None
    quantity: int | None
    value: float | None
    year: int
    category_id: int
    country_id: int


class ExportDTOResponse(BaseModel):
    id: int | None = None
    country: str
    quantity: int | None
    year: int
    category: CategoryDTO