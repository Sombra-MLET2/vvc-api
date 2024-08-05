from unittest.mock import Mock, patch

import pytest
from sqlalchemy.orm import Session

from dtos import SaleDTOResponse
from models.category import Category
from models.sale import Sale
from ucs.sale import find_sales_items, find_sales_item, __to_dto, __to_dto_list

mock_session = Mock(spec=Session)


@pytest.fixture
def test_sale():
    return Sale(id=42, name="Juice", quantity=100, year=1988,
                category=Category(id=100, name='Red', meta_name='meta_red'))


@pytest.fixture
def test_sales(test_sale):
    return [test_sale, test_sale, test_sale]


@pytest.mark.asyncio
@patch('repositories.sale_repository.find_all')
async def test_find_sales_items_all(find_all_mock, test_sales):
    find_all_mock.return_value = test_sales

    result = await find_sales_items(mock_session, None, None)

    find_all_mock.assert_called_once_with(mock_session)
    assert result == __to_dto_list(test_sales)


@pytest.mark.asyncio
@patch('repositories.sale_repository.find_one')
async def test_find_sales_item(find_one_mock, test_sale):
    find_one_mock.return_value = test_sale

    result = await find_sales_item(mock_session, 12345)

    find_one_mock.assert_called_once_with(mock_session, 12345)
    assert result == __to_dto(test_sale)


def test___to_dto(test_sale):
    result = __to_dto(test_sale)

    assert result.__class__ == SaleDTOResponse
    assert result.year == test_sale.year
    assert result.category.meta_name == test_sale.category.meta_name


def test___to_dto_list(test_sales):
    result = __to_dto_list(test_sales)

    assert len(result) == len(test_sales)
