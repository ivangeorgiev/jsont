from unittest.mock import patch, Mock

from jsont import create_path_map

def test_create_path_map():
    definition = {'city': 'address/city'}
    result = create_path_map(definition)
    value = 'something'
    assert result[0][0] == 'city'
    assert value is result[0][1]({'address':{'city':value}})
