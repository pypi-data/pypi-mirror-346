import pytest
import pandas as pd

from src.app.utils.validation_utils import (
    check_not_null,
    check_not_empty,
    check_not_duplicate
)


@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({
        'no_nulls': [1, 2, 3, 4, 5],
        'has_nulls': [1, None, 3, None, 5],
        'no_empty': ['a', 'b', 'c', 'd', 'e'],
        'has_empty': ['a', '', 'c', '', 'e'],
        'no_duplicates': [1, 2, 3, 4, 5],
        'has_duplicates': [1, 2, 2, 3, 1]
    })


@pytest.fixture
def single_row_dataframe():
    return pd.DataFrame({
        'single_value': [1],
        'single_null': [None],
        'single_empty': [''],
    })


@pytest.fixture
def empty_dataframe():
    return pd.DataFrame()

# Tests for check_not_null


def test_check_not_null_true(sample_dataframe):
    assert check_not_null(sample_dataframe, 'no_nulls')


def test_check_not_null_false(sample_dataframe):
    assert not check_not_null(sample_dataframe, 'has_nulls')

# Tests for check_not_empty


def test_check_not_empty_true(sample_dataframe):
    assert check_not_empty(sample_dataframe, 'no_empty')


def test_check_not_empty_false(sample_dataframe):
    assert not check_not_empty(sample_dataframe, 'has_empty')

# Tests for check_not_duplicate


def test_check_not_duplicate_true(sample_dataframe):
    assert check_not_duplicate(sample_dataframe, 'no_duplicates')


def test_check_not_duplicate_false(sample_dataframe):
    assert not check_not_duplicate(sample_dataframe, 'has_duplicates')

# Edge cases


def test_single_row_checks(single_row_dataframe):
    assert check_not_null(single_row_dataframe, 'single_value')
    assert not check_not_null(single_row_dataframe, 'single_null')
    assert not check_not_empty(single_row_dataframe, 'single_empty')
    assert check_not_duplicate(single_row_dataframe, 'single_value')

# Error handling tests


def test_column_not_exist(sample_dataframe):
    with pytest.raises(KeyError):
        check_not_null(sample_dataframe, 'non_existent_column')
    with pytest.raises(KeyError):
        check_not_empty(sample_dataframe, 'non_existent_column')
    with pytest.raises(KeyError):
        check_not_duplicate(sample_dataframe, 'non_existent_column')


def test_empty_dataframe(empty_dataframe):
    with pytest.raises(KeyError):
        check_not_null(empty_dataframe, 'any_column')
    with pytest.raises(KeyError):
        check_not_empty(empty_dataframe, 'any_column')
    with pytest.raises(KeyError):
        check_not_duplicate(empty_dataframe, 'any_column')
