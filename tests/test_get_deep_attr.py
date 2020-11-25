from unittest.mock import Mock, patch
import pytest

from jsont import get_deep_attr, get_deep_attr_getter

def test_get_deep_attr_should_return_object_if_path_empty():
    o = 'something'
    assert o is get_deep_attr(o, '')

def test_get_deep_attr_should_return_element_if_path_to_element():
    value = 'something'
    o = { 'key': value } 
    assert value is get_deep_attr(o, 'key')

def test_get_deep_attr_should_return_attribute_if_path_to_attribute():
    value = 'something'
    o = Mock()
    o.key = value 
    assert value is get_deep_attr(o, 'key')

def test_get_deep_attr_should_return_default_if_path_not_found_and_default_passed():
    value = 'something'
    o = {}
    assert value is get_deep_attr(o, 'key', default=value)

def test_get_deep_attr_should_raise_KeyError_if_path_not_found_and_no_default_passed():
    value = 'something'
    o = {}
    with pytest.raises(KeyError) as excinfo:
        _ = get_deep_attr(o, 'key')

def test_get_deep_attr_should_return_deep_value():
    value = 'something'
    o = { 'path': {'to': value}}
    assert value is get_deep_attr(o, 'path/to')

def test_get_deep_attr_getter_should_return_callable():
    result = get_deep_attr_getter('path')
    assert callable(result)

@patch('jsont.get_deep_attr')
def test_get_deep_attr_getter_should_calls_get_deep_attr(get_deep_attr_mock):
    value = 'something'
    get_deep_attr_mock.return_value = value
    getter = get_deep_attr_getter('path', default='default')
    o = {}
    _ = getter(o)
    get_deep_attr_mock.assert_called_with(o,'path',default='default')

@patch('jsont.get_deep_attr')
def test_get_deep_attr_getter_should_return_result_from_get_deep_attr(get_deep_attr_mock):
    value = 'something'
    get_deep_attr_mock.return_value = value
    getter = get_deep_attr_getter('path', default='default')
    o = {}
    result = getter(o)
    assert value is result
