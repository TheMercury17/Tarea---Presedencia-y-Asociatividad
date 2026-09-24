"""
Módulo de Nodos del Árbol de Sintaxis Abstracta (AST)
Universidad Sergio Arboleda
Materia: Lenguajes de Programación y Transducción
Docente: Joaquin F. Sanchez
Grupo 5: Andrés Sebastián Coral Vallejo y Carol Arenas Cardona
"""

from abc import ABC, abstractmethod


class ASTNode(ABC):
    """Clase base abstracta para todos los nodos del AST."""

    @abstractmethod
    def evaluate(self) -> float:
        """Evalúa el valor semántico del subárbol."""
        pass

    @abstractmethod
    def to_tree_str(self, prefix: str = "", is_tail: bool = True) -> str:
        """Genera una representación visual en árbol jerárquico."""
        pass

    @abstractmethod
    def to_parenthesized(self) -> str:
        """Genera la expresión con paréntesis explícitos que reflejan la asociatividad y precedencia."""
        pass


class NumberNode(ASTNode):
    """Nodo que representa un valor numérico (literal)."""

    def __init__(self, value: float):
        self.value = float(value)

    def evaluate(self) -> float:
        return self.value

    def to_tree_str(self, prefix: str = "", is_tail: bool = True) -> str:
        val_str = f"{int(self.value)}" if self.value.is_integer() else f"{self.value}"
        return f"{prefix}{'└── ' if is_tail else '├── '}Num({val_str})\n"

    def to_parenthesized(self) -> str:
        return f"{int(self.value)}" if self.value.is_integer() else f"{self.value}"

    def __repr__(self):
        val_str = f"{int(self.value)}" if self.value.is_integer() else f"{self.value}"
        return f"Num({val_str})"


class BinaryOpNode(ASTNode):
    """Nodo que representa una operación binaria (+, -, *, /)."""

    def __init__(self, left: ASTNode, op: str, right: ASTNode):
        self.left = left
        self.op = op
        self.right = right

    def evaluate(self) -> float:
        left_val = self.left.evaluate()
        right_val = self.right.evaluate()

        if self.op == '+':
            return left_val + right_val
        elif self.op == '-':
            return left_val - right_val
        elif self.op == '*':
            return left_val * right_val
        elif self.op == '/':
            if right_val == 0:
                raise ZeroDivisionError("Error semántico: División por cero")
            return left_val / right_val
        else:
            raise ValueError(f"Operador desconocido: {self.op}")

    def to_tree_str(self, prefix: str = "", is_tail: bool = True) -> str:
        connector = '└── ' if is_tail else '├── '
        res = f"{prefix}{connector}Op({self.op})\n"
        new_prefix = prefix + ('    ' if is_tail else '│   ')
        res += self.left.to_tree_str(new_prefix, is_tail=False)
        res += self.right.to_tree_str(new_prefix, is_tail=True)
        return res

    def to_parenthesized(self) -> str:
        return f"({self.left.to_parenthesized()} {self.op} {self.right.to_parenthesized()})"

    def __repr__(self):
        return f"({self.left!r} {self.op} {self.right!r})"
