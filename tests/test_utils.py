import unittest
from unittest.mock import MagicMock, mock_open, patch

from src.utils import load_json_operations


@patch('your_module.os.path.exists')
def test_file_not_found(self, mock_exists: unittest.mock.Mock) -> None:
    """Тест: файл не существует"""
    mock_exists.return_value = False
    result = load_json_operations('data/operations.json')
    self.assertEqual(result, [])
    mock_exists.assert_called_once_with('data/operations.json')

@patch('your_module.os.path.getsize')
@patch('your_module.os.path.isfile')
@patch('your_module.os.path.exists')
def test_empty_file(self, mock_exists: unittest.mock.Mock, mock_isfile: unittest.mock.Mock,
                    mock_getsize: unittest.mock.Mock) -> None:
    """Тест: файл пустой"""
    mock_exists.return_value = True
    mock_isfile.return_value = True
    mock_getsize.return_value = 0
    result = load_json_operations('data/operations.json')
    self.assertEqual(result, [])
    mock_getsize.assert_called_once_with('data/operations.json')


@patch('your_module.json.load')
@patch('builtins.open', new_callable=mock_open, read_data='{}')
@patch('your_module.os.path.getsize')
@patch('your_module.os.path.isfile')
@patch('your_module.os.path.exists')
def test_file_contains_not_list(self, mock_exists, mock_isfile,
                                mock_getsize, mock_file, mock_json_load: unittest.mock.Mock) -> None:
    """Тест: файл содержит не список"""
    mock_exists.return_value = True
    mock_isfile.return_value = True
    mock_getsize.return_value = 100
    mock_json_load.return_value = {"key": "value"}  # словарь, а не список

    result = load_json_operations('data/operations.json')
    self.assertEqual(result, [])
    mock_file.assert_called_once_with('data/operations.json', 'r', encoding='utf-8')

