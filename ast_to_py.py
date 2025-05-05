"""Generate Python objects from AST"""

# TODO
# handle different types (currently everything is converted to str);
# handle nested objects;
# how to name objects without a label?

from _ast_ import *
from parser import produce_ast

json = '{"name": "foo", "age": 69, "address": {"city": "Bar", "id": 123}}'

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

    fstring = '{{' + ', '.join([f"{attr}: {{self.{attr}}}" for attr in py_attrs]) + '}}'
    py_attrs['__str__'] = lambda self: fstring.format(self=self)

    SomeObjectType = type('SomeObject', (object,), py_attrs)
    some_object = SomeObjectType()
    return some_object

def main():
    ast = produce_ast(json)
    obj = gen_obj(ast)
    print(obj)

if __name__ == '__main__':
    main()

