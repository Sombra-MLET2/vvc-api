import pytest
from unittest.mock import MagicMock
from unittest.mock import patch
from typing import List
from dtos import CategoryDTO, ExportDTOResponse, ExportDTO
from models.category import Category
from models.country import Country
from models.exports import Export as ExportModel

import ucs.exports


@pytest.fixture
def export():
    Export = MagicMock(spec=ExportModel)
    Export.id = 1
    Export.quantity = 100
    Export.year = 2023
    Export.country.name = "country"
    Export.category.name = "name"
    Export.category.meta_name = "meta_name"

    return Export


@pytest.fixture
def exports(export):
    return [export]


def test_to_dto(export):
    result = ucs.exports.__to_dto(export)

    assert isinstance(result, ExportDTOResponse)
    assert result.id == export.id
    assert result.quantity == export.quantity
    assert result.year == export.year
    assert result.country == export.country.name
    assert isinstance(result.category, CategoryDTO)


@pytest.mark.asyncio
@patch("repositories.exports_repository.find_all")
async def test_find_exports_items_no_params(mocked_find_all, exports):
    mocked_find_all.return_value = exports

    session = MagicMock()

    results = await ucs.exports.find_exports_items(session, None, None, None)

    mocked_find_all.assert_called_once_with(session)

    assert len(results) == len(exports)
    assert all(isinstance(result, ExportDTOResponse) for result in results)


def test_add_export_item():
    session = MagicMock()
    dto = ExportDTO(id=42, quantity=100, value=20000, year=2077, country_id=123, category_id=42)
    repository_response = ExportModel(id=42, quantity=100, value=20000, year=2077, category_id=42,
                                      category=Category(id=2, name="Category", meta_name="meta_cat"), country_id=22,
                                      country=Country(id=1, name="Country"))

    with patch("ucs.exports.exports_repository.create_new", return_value=repository_response) as mock_create:
        result = ucs.exports.add_export_item(session, dto)

    mock_create.assert_called_once_with(session, dto)

    assert isinstance(result, ExportDTOResponse)
