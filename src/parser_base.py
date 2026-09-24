"""
Módulo Base para Analizadores Sintácticos (Parsers)
Universidad Sergio Arboleda - Lenguajes de Programación
Grupo 5: Andrés Sebastián Coral Vallejo y Carol Arenas Cardona
"""

from typing import List
from .lexer import Token, Lexer
from .ast_nodes import ASTNode, NumberNode


class BaseParser:
    """Clase base con métodos auxiliares para el análisis sintáctico."""

    def __init__(self, tokens: List[Token], text: str = ""):
        self.tokens = tokens
        self.pos = 0
        self.text = text

    @classmethod
    def from_text(cls, text: str):
        lexer = Lexer(text)
        tokens = lexer.tokenize()
        return cls(tokens, text)

    @property
    def current(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]

    def consume(self, expected_type: str = None) -> Token:
        token = self.current
        if expected_type and token.type != expected_type:
            raise SyntaxError(
                f"Error sintáctico: Se esperaba '{expected_type}' pero se encontró '{token.type}' ('{token.value}') "
                f"en la posición {token.pos}"
            )
        self.pos += 1
        return token

    def match(self, *expected_types: str) -> bool:
        return self.current.type in expected_types

    def parse_factor(self, start_rule_fn) -> ASTNode:
        """
        Regla Factor común:
        F -> NUM | '(' E ')'
        """
        tok = self.current
        if self.match('NUM'):
            self.consume('NUM')
            return NumberNode(float(tok.value))
        elif self.match('LPAREN'):
            self.consume('LPAREN')
            expr_node = start_rule_fn()
            self.consume('RPAREN')
            return expr_node
        else:
            raise SyntaxError(
                f"Error sintáctico en Factor: Token inesperado '{tok.type}' ('{tok.value}') en posición {tok.pos}"
            )
