import pytest
from unittest.mock import MagicMock, patch
from typing import List

from dtos import CategoryDTO
from models.category import Category

import ucs.categories as sut


@pytest.fixture
def category():
    return Category(id=42, name='test category name', meta_name='teste_metaname')


@pytest.fixture
def categories(category):
    return [category]


def test_to_dto(category):
    result = sut.to_dto(category)
    assert isinstance(result, CategoryDTO)
    assert result.name == category.name
    assert result.meta_name == category.meta_name


@patch('ucs.categories.find_all')
def test_list_all_categories(mocked_find_all, categories):
    mocked_find_all.return_value = categories

    session = MagicMock()

    results = sut.list_all_categories(session)

    mocked_find_all.assert_called_once_with(session)

    assert len(results) == len(categories)
    assert all(isinstance(result, CategoryDTO) for result in results)
