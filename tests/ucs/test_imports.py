from unittest.mock import Mock, patch, MagicMock

import pytest
from sqlalchemy.orm import Session

from dtos import ImportDTOResponse, ImportDTO
from models.imports import Import
from ucs.imports import find_imports_items, find_imports_item, add_import_item, __to_dto, __to_dto_list

mock_session = Mock(spec=Session)


@pytest.fixture
def test_import():
    import_model = MagicMock(spec=Import)
    import_model.id = 1
    import_model.quantity = 100
    import_model.year = 2023
    import_model.country.name = "country"
    import_model.category.name = "name"
    import_model.category.meta_name = "meta_name"

    return import_model


@pytest.fixture
def test_imports(test_import):
    return [test_import, test_import]


@pytest.mark.asyncio
@patch('repositories.imports_repository.find_all')
async def test_find_imports_items_all(find_all_mock, test_imports):
    find_all_mock.return_value = test_imports

    result = await find_imports_items(mock_session, None, None, None)

    find_all_mock.assert_called_once_with(mock_session)
    assert result == __to_dto_list(test_imports)


@pytest.mark.asyncio
@patch('repositories.imports_repository.find_one')
async def test_find_imports_item(find_one_mock, test_import):
    find_one_mock.return_value = test_import

    result = await find_imports_item(mock_session, 12345)

    find_one_mock.assert_called_once_with(mock_session, 12345)
    assert result == __to_dto(test_import)


@patch('repositories.imports_repository.create_new')
def test_add_import_item(create_new_mock, test_import):
    dto = ImportDTO(id=42, quantity=100, value=3050.00, year=2023, country_id=22, category_id=71)
    create_new_mock.return_value = test_import

    result = add_import_item(mock_session, dto)

    create_new_mock.assert_called_once_with(mock_session, dto)
    assert result == __to_dto(test_import)


def test___to_dto(test_import):
    result = __to_dto(test_import)

    assert result.__class__ == ImportDTOResponse
    assert result.year == test_import.year
    assert result.category.meta_name == test_import.category.meta_name


def test___to_dto_list(test_imports):
    result = __to_dto_list(test_imports)

    assert len(result) == len(test_imports)
