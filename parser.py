"""Produce AST using tokens"""

from typing import cast

from _ast_ import *
from lexer import *

tokens: list[Token] = list()
prev: Token | None = None

def at() -> Token:
    return tokens[0]

def eat() -> Token:
    prev = tokens.pop(0)
    return prev

def expect(ttype: TokenType, err: str) -> Token:
    prev = eat()
    if prev.ttype != ttype:
        print(f"Parser Error: {prev.pos}\n", err, f"Expected: {ttype};", f"Found: {prev}")
        exit(1)
    return prev

def produce_ast(json: str) -> Expr:
    global tokens
    lexer = Lexer(json)
    tokens = lexer.tokenize()

    return parse_expr()

def parse_expr() -> Expr:
    match at().ttype:
        case TokenType.String | TokenType.Number | TokenType.Null | TokenType.Boolean:
            return parse_literal()
        case TokenType.Lbracket:
            eat()
            return parse_list()
        case TokenType.Lbrace:
            eat()
            return parse_object()
        case _:
            print(f"Parser Error\n", "Unexpected token: {at()}")
            exit(1)

def parse_list() -> List:
    content: list[Expr] = list()
    _list = List(content)

    while (at().ttype != TokenType.Rbracket):
        if len(content) > 0:
            expect(TokenType.Comma, "Comma must separate list elements.")
        content.append(parse_expr())
    eat() # eat ']'

    return _list

def parse_object() -> Object:
    # expect(TokenType.Lbrace, "Object must start with left brace.")
    attributes: list[Attribute] = list()
    _object = Object(attributes)

    while (at().ttype != TokenType.Rbrace):
        if len(attributes) > 0:
            expect(TokenType.Comma, "Comma must separate object attributes.")
        attributes.append(parse_attribute())
    eat() # eat '}'

    return _object

def parse_attribute() -> Attribute:
    label = parse_literal()
    if label.literal_type != LiteralType.Str:
        print("Parser Error\n", "Object attribute name must be a string.", prev)
        exit(1)

    expect(TokenType.Colon, "Colon must follow the object attribute name.")
    value = parse_expr()

    return Attribute(value, cast(str, label.value))

def parse_literal() -> Literal:
    token = eat()
    match token.ttype:
        case TokenType.String:
            return Literal(LiteralType.Str, token.value)
        case TokenType.Number:
            return Literal(LiteralType.Num, token.value)
        case TokenType.Boolean:
            return Literal(LiteralType.Bool, token.value)
        case TokenType.Null:
            return Literal(LiteralType.Null, None)
        case _:
            print("Parser Error\n", "Unexpected token found during parsing:", at())
            exit(1)


if __name__ == '__main__':
    # json = open('mock.json').read()
    json = '[{ "1": null, \n"2": [{}] }]'
    print(json)
    ast = produce_ast(json)
    print(ast)

