"""Generate Python objects from AST"""

# TODO
# handle different types (currently everything is converted to str);
# unhardcode __str__() generation (should loop over object's attributes);
# handle nested objects;
# how to name objects without a label?

from _ast_ import *
from parser import produce_ast

json = '{"name": "foo", "age": 69, "some_obj": {"a": 69}}'

def gen_obj(obj: Object):
    assert isinstance(obj, Object), f"{obj} is not of type Object"
    attrs = {attr.label: attr.value for attr in obj.body}
    py_attrs = dict()
    for label, value in attrs.items():
        #match type(value):
        #    case Literal:
        #        print(value)
        if isinstance(value, Object):
            py_attrs[label.strip('"')] = gen_obj(value)
        else:
            assert isinstance(value, Literal), "We only handle Object and Literal types for now"
            py_attrs[label.strip('"')] = value.value
    # TODO Unhardcode
    py_attrs['__str__'] = lambda self: f"name: {self.name}, age: {self.age}, some_obj: {self.some_obj}"
    SomeObject = type('SomeObject', (object,), py_attrs)
    return SomeObject()

def main():
    ast = produce_ast(json)
    obj = gen_obj(ast)
    print(obj)

if __name__ == '__main__':
    main()

