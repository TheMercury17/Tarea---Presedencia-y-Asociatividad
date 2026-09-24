"""
Paquete src para Tarea - Precedencia y Asociatividad
Grupo 5: Andrés Sebastián Coral Vallejo y Carol Arenas Cardona
"""

from .ast_nodes import ASTNode, NumberNode, BinaryOpNode
from .lexer import Lexer, Token
from .parser_base import BaseParser
from .gramaticas import (
    ParserG1_Izq_MulDiv,
    ParserG2_Der_MulDiv,
    ParserG3_Izq_SumRes,
    ParserG4_Der_SumRes,
    ALL_PARSERS
)
from .evaluador import analizar_expresion, comparar_todas, formatear_tabla_comparativa
