import pytest
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session
from dtos import ProcessingDTOResponse, ProcessingDTO
from models.category import Category
from models.processing import Processing
from ucs.processing import find_processing_items, find_processing_item, add_new_processing_item, __to_dto, __to_dto_list

mock_session = Mock(spec=Session)


@pytest.fixture
def test_processing():
    return Processing(id=42, cultivation='Cultivation', year=2024, quantity=100, grape_class_id=17,
                      grape_class=Category(id=10, name='Grape Class', meta_name='meta_grape'), category_id=66,
                      category=Category(id=100, name='Juice', meta_name='meta_juice'))


@pytest.fixture
def test_processings(test_processing):
    return [test_processing, test_processing]


@pytest.mark.asyncio
@patch('repositories.processing_repository.find_all')
async def test_find_processing_items_all(find_all_mock, test_processings):
    find_all_mock.return_value = test_processings

    result = await find_processing_items(mock_session, None, None, None)

    find_all_mock.assert_called_once_with(mock_session)
    assert result == __to_dto_list(test_processings)


@pytest.mark.asyncio
@patch('repositories.processing_repository.find_one')
async def test_find_processing_item(find_one_mock, test_processing):
    find_one_mock.return_value = test_processing

    result = await find_processing_item(mock_session, 12345)

    find_one_mock.assert_called_once_with(mock_session, 12345)
    assert result == __to_dto(test_processing)


@patch('repositories.processing_repository.create_new')
def test_add_new_processing_item(create_new_mock, test_processing):
    dto = ProcessingDTO(id=42, cultivation='Cultivation', year=2024, quantity=100, grape_class_id=17, category_id=66)
    create_new_mock.return_value = test_processing

    result = add_new_processing_item(mock_session, dto)

    create_new_mock.assert_called_once_with(mock_session, dto)
    assert result == __to_dto(test_processing)


def test___to_dto(test_processing):
    result = __to_dto(test_processing)

    assert result.__class__ == ProcessingDTOResponse


def test___to_dto_list(test_processings):
    print(test_processings)
    result = __to_dto_list(test_processings)

    assert len(result) == len(test_processings)
