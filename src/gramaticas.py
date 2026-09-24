"""
Implementación de las 4 Gramáticas del Taller
Universidad Sergio Arboleda
Materia: Lenguajes de Programación y Transducción
Docente: Joaquin F. Sanchez
Grupo 5: Andrés Sebastián Coral Vallejo y Carol Arenas Cardona

Gramáticas evaluadas:
1. G1: Precedencia estándar (*, / > +, -) con Asociatividad por la Izquierda.
2. G2: Precedencia estándar (*, / > +, -) con Asociatividad por la Derecha.
3. G3: Precedencia invertida (+, - > *, /) con Asociatividad por la Izquierda.
4. G4: Precedencia invertida (+, - > *, /) con Asociatividad por la Derecha.
"""

from .parser_base import BaseParser
from .ast_nodes import ASTNode, BinaryOpNode


# ==============================================================================
# GRAMÁTICA 1: Precedencia Estándar (*, / > +, -), Asociatividad por la Izquierda
# ==============================================================================
class ParserG1_Izq_MulDiv(BaseParser):
    """
    Gramática formal G1:
      E -> E + T | E - T | T       (Asociatividad Izquierda para + y -)
      T -> T * F | T / F | F       (Asociatividad Izquierda para * y /)
      F -> NUM | '(' E ')'
    """
    NAME = "G1: Precedencia (*, / > +, -) | Asociatividad IZQUIERDA"

    def parse(self) -> ASTNode:
        node = self.parse_E()
        self.consume('EOF')
        return node

    def parse_E(self) -> ASTNode:
        node = self.parse_T()
        while self.match('PLUS', 'MINUS'):
            op_tok = self.consume()
            right = self.parse_T()
            node = BinaryOpNode(left=node, op=op_tok.value, right=right)
        return node

    def parse_T(self) -> ASTNode:
        node = self.parse_F()
        while self.match('MUL', 'DIV'):
            op_tok = self.consume()
            right = self.parse_F()
            node = BinaryOpNode(left=node, op=op_tok.value, right=right)
        return node

    def parse_F(self) -> ASTNode:
        return self.parse_factor(self.parse_E)


# ==============================================================================
# GRAMÁTICA 2: Precedencia Estándar (*, / > +, -), Asociatividad por la Derecha
# ==============================================================================
class ParserG2_Der_MulDiv(BaseParser):
    """
    Gramática formal G2:
      E -> T + E | T - E | T       (Asociatividad Derecha para + y -)
      T -> F * T | F / T | F       (Asociatividad Derecha para * y /)
      F -> NUM | '(' E ')'
    """
    NAME = "G2: Precedencia (*, / > +, -) | Asociatividad DERECHA"

    def parse(self) -> ASTNode:
        node = self.parse_E()
        self.consume('EOF')
        return node

    def parse_E(self) -> ASTNode:
        node = self.parse_T()
        if self.match('PLUS', 'MINUS'):
            op_tok = self.consume()
            right = self.parse_E()  # Recursión a la derecha
            return BinaryOpNode(left=node, op=op_tok.value, right=right)
        return node

    def parse_T(self) -> ASTNode:
        node = self.parse_F()
        if self.match('MUL', 'DIV'):
            op_tok = self.consume()
            right = self.parse_T()  # Recursión a la derecha
            return BinaryOpNode(left=node, op=op_tok.value, right=right)
        return node

    def parse_F(self) -> ASTNode:
        return self.parse_factor(self.parse_E)


# ==============================================================================
# GRAMÁTICA 3: Precedencia Invertida (+, - > *, /), Asociatividad por la Izquierda
# ==============================================================================
class ParserG3_Izq_SumRes(BaseParser):
    """
    Gramática formal G3:
      E -> E * T | E / T | T       (Asociatividad Izquierda para * y /; menor precedencia)
      T -> T + F | T - F | F       (Asociatividad Izquierda para + y -; mayor precedencia)
      F -> NUM | '(' E ')'
    """
    NAME = "G3: Precedencia (+, - > *, /) | Asociatividad IZQUIERDA"

    def parse(self) -> ASTNode:
        node = self.parse_E()
        self.consume('EOF')
        return node

    def parse_E(self) -> ASTNode:
        # Nivel inferior de precedencia: Multiplicación y División
        node = self.parse_T()
        while self.match('MUL', 'DIV'):
            op_tok = self.consume()
            right = self.parse_T()
            node = BinaryOpNode(left=node, op=op_tok.value, right=right)
        return node

    def parse_T(self) -> ASTNode:
        # Mayor nivel de precedencia: Suma y Resta
        node = self.parse_F()
        while self.match('PLUS', 'MINUS'):
            op_tok = self.consume()
            right = self.parse_F()
            node = BinaryOpNode(left=node, op=op_tok.value, right=right)
        return node

    def parse_F(self) -> ASTNode:
        return self.parse_factor(self.parse_E)


# ==============================================================================
# GRAMÁTICA 4: Precedencia Invertida (+, - > *, /), Asociatividad por la Derecha
# ==============================================================================
class ParserG4_Der_SumRes(BaseParser):
    """
    Gramática formal G4:
      E -> T * E | T / E | T       (Asociatividad Derecha para * y /; menor precedencia)
      T -> F + T | F - T | F       (Asociatividad Derecha para + y -; mayor precedencia)
      F -> NUM | '(' E ')'
    """
    NAME = "G4: Precedencia (+, - > *, /) | Asociatividad DERECHA"

    def parse(self) -> ASTNode:
        node = self.parse_E()
        self.consume('EOF')
        return node

    def parse_E(self) -> ASTNode:
        # Menor nivel de precedencia: Multiplicación y División (derecha)
        node = self.parse_T()
        if self.match('MUL', 'DIV'):
            op_tok = self.consume()
            right = self.parse_E()  # Recursión a la derecha
            return BinaryOpNode(left=node, op=op_tok.value, right=right)
        return node

    def parse_T(self) -> ASTNode:
        # Mayor nivel de precedencia: Suma y Resta (derecha)
        node = self.parse_F()
        if self.match('PLUS', 'MINUS'):
            op_tok = self.consume()
            right = self.parse_T()  # Recursión a la derecha
            return BinaryOpNode(left=node, op=op_tok.value, right=right)
        return node

    def parse_F(self) -> ASTNode:
        return self.parse_factor(self.parse_E)


ALL_PARSERS = [
    ParserG1_Izq_MulDiv,
    ParserG2_Der_MulDiv,
    ParserG3_Izq_SumRes,
    ParserG4_Der_SumRes
]
