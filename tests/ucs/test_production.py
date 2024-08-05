import pytest
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session
from dtos import ProductionDTOResponse, CategoryDTO
from models.category import Category
from models.production import Production
from ucs.production import find_production_items, find_production_item, __to_dto, __to_dto_list

mock_session = Mock(spec=Session)


@pytest.fixture
def test_production():
    return Production(id=42, name='Production', year=2024, quantity=100, category_id=66,
                      category=Category(id=100, name='Red', meta_name='meta_red'))


@pytest.fixture
def test_productions(test_production):
    return [test_production, test_production, test_production]


@pytest.mark.asyncio
@patch('repositories.production_repository.find_all')
async def test_find_production_items_all(find_all_mock, test_productions):
    find_all_mock.return_value = test_productions

    result = await find_production_items(mock_session, None, None)

    find_all_mock.assert_called_once_with(mock_session)
    assert result == __to_dto_list(test_productions)


@pytest.mark.asyncio
@patch('repositories.production_repository.find_one')
async def test_find_production_item(find_one_mock, test_production):
    find_one_mock.return_value = test_production

    result = await find_production_item(mock_session, 12345)

    find_one_mock.assert_called_once_with(mock_session, 12345)
    assert result == __to_dto(test_production)


def test___to_dto(test_production):
    result = __to_dto(test_production)

    assert result.__class__ == ProductionDTOResponse
    assert result.year == test_production.year
    assert result.id == test_production.id



def test___to_dto_list(test_productions):
    result = __to_dto_list(test_productions)

    assert len(result) == len(test_productions)
