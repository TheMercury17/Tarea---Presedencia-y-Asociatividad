"""
Módulo del Analizador Léxico (Lexer)
Universidad Sergio Arboleda
Materia: Lenguajes de Programación y Transducción
Docente: Joaquin F. Sanchez
Grupo 5: Andrés Sebastián Coral Vallejo y Carol Arenas Cardona
"""

import re
from typing import List, NamedTuple


class Token(NamedTuple):
    type: str
    value: str
    pos: int


class Lexer:
    """Tokenizador para expresiones aritméticas de la calculadora."""

    TOKEN_SPECIFICATION = [
        ('NUM',     r'\d+(\.\d+)?'),       # Números enteros o decimales
        ('PLUS',    r'\+'),                # Suma
        ('MINUS',   r'-'),                 # Resta
        ('MUL',     r'\*'),                # Multiplicación
        ('DIV',     r'/'),                 # División
        ('LPAREN',  r'\('),                # Paréntesis izquierdo
        ('RPAREN',  r'\)'),                # Paréntesis derecho
        ('WS',      r'[ \t\r\n]+'),        # Espacios en blanco
        ('MISMATCH', r'.'),                 # Cualquier otro caracter no reconocido
    ]

    def __init__(self, text: str):
        self.text = text
        self.regex = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.TOKEN_SPECIFICATION))

    def tokenize(self) -> List[Token]:
        tokens: List[Token] = []
        for match in self.regex.finditer(self.text):
            kind = match.lastgroup
            val = match.group()
            pos = match.start()

            if kind == 'WS':
                continue
            elif kind == 'MISMATCH':
                raise SyntaxError(f"Error léxico: Carácter inesperado '{val}' en posición {pos}")
            else:
                tokens.append(Token(kind, val, pos))

        tokens.append(Token('EOF', '', len(self.text)))
        return tokens
