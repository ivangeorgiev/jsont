from jsont import get_deep_attr_getter, map_rows

def test_map_rows_can_map_list_elements():
    o = [1,2]
    map = [('index', get_deep_attr_getter(''))]
    result = map_rows(o, map)
    assert [{'index':1}, {'index':2}] == result

def test_map_rows_returns_list_of_mapped_items():
    o = {'value':[{'id':1,'address':{'city':'New York'}},]}
    expect = [{'id':1, 'city':'New York'},]
    map = [
        ('id', get_deep_attr_getter('id')),
        ('city', get_deep_attr_getter('address/city'))
    ]
    result = map_rows(o, map, 'value')
    assert expect == result