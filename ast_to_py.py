"""Generate Python objects from AST"""

# TODO
# handle different types (currently everything is converted to str) 
# unhardcode __str__() generation (should loop over object's attributes);
# handle nested objects;
# how to name objects without a label?

from _ast_ import *
from parser import produce_ast

json = '{"name": "foo", "age": 69}'

def gen_obj(obj: Object):
    assert isinstance(obj, Object), f"{obj} is not of type Object"
    attrs = {attr.label: attr.value for attr in obj.body}
    py_attrs = dict()
    for label, value in attrs.items():
        assert isinstance(value, Literal), "We don't handle non-literal values yet"
        py_attrs[label.strip('"')] = value.value
    print(py_attrs)
    # Unhardcode
    py_attrs['__str__'] = lambda self: f"name: {self.name}, age: {self.age}"
    SomeObject = type('SomeObject', (object,), py_attrs)
    return SomeObject()

def main():
    ast = produce_ast(json)
    obj = gen_obj(ast)
    print(obj)

if __name__ == '__main__':
    main()

