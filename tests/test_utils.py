import unittest
from unittest.mock import MagicMock, mock_open, patch

from src.utils import load_json_operations


@patch('src.utils.os.path.exists')
def test_file_not_found(mock_exists: unittest.mock.Mock) -> None:
    """Тест: файл не существует"""
    mock_exists.return_value = False
    result = load_json_operations('data/operations.json')
    assert result == []
    mock_exists.assert_called_once_with('data/operations.json')

@patch('src.utils.os.path.getsize')
@patch('src.utils.os.path.isfile')
@patch('src.utils.os.path.exists')
def test_empty_file(mock_exists: unittest.mock.Mock, mock_isfile: unittest.mock.Mock,
                    mock_getsize: unittest.mock.Mock) -> None:
    """Тест: файл пустой"""
    mock_exists.return_value = True
    mock_isfile.return_value = True
    mock_getsize.return_value = 0
    result = load_json_operations('data/operations.json')
    assert result == []
    mock_getsize.assert_called_once_with('data/operations.json')


@patch('src.utils.json.load')
@patch('builtins.open', new_callable=mock_open, read_data='{}')
@patch('src.utils.os.path.getsize')
@patch('src.utils.os.path.isfile')
@patch('src.utils.os.path.exists')
def test_file_contains_not_list(mock_exists, mock_isfile,
                                mock_getsize, mock_file, mock_json_load: unittest.mock.Mock) -> None:
    """Тест: файл содержит не список"""
    mock_exists.return_value = True
    mock_isfile.return_value = True
    mock_getsize.return_value = 100
    mock_json_load.return_value = {"key": "value"}  # словарь, а не список

    result = load_json_operations('data/operations.json')
    assert result == []
    mock_file.assert_called_once_with('data/operations.json', 'r', encoding='utf-8')

