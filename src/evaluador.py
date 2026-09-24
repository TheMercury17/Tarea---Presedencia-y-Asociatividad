"""
Módulo de Evaluación y Formateo de Expresiones
Universidad Sergio Arboleda
Materia: Lenguajes de Programación y Transducción
Docente: Joaquin F. Sanchez
Grupo 5: Andrés Sebastián Coral Vallejo y Carol Arenas Cardona
"""

from typing import Dict, Any, List
from .gramaticas import ALL_PARSERS


def analizar_expresion(expr: str, parser_cls) -> Dict[str, Any]:
    """Analiza y evalúa una expresión aritmética usando la gramática seleccionada."""
    parser = parser_cls.from_text(expr)
    ast = parser.parse()
    valor = ast.evaluate()
    agrupacion = ast.to_parenthesized()
    arbol = ast.to_tree_str()

    return {
        "parser_name": parser_cls.NAME,
        "expr": expr,
        "valor": valor,
        "agrupacion": agrupacion,
        "arbol": arbol,
        "ast": ast
    }


def comparar_todas(expr: str) -> List[Dict[str, Any]]:
    """Ejecuta y compara una expresión bajo las 4 gramáticas."""
    resultados = []
    for parser_cls in ALL_PARSERS:
        res = analizar_expresion(expr, parser_cls)
        resultados.append(res)
    return resultados


def formatear_tabla_comparativa(resultados: List[Dict[str, Any]]) -> str:
    """Genera una tabla en texto formateada con los resultados comparativos."""
    header = f"{'Gramática':<55} | {'Agrupación (Árbol AST)':<30} | {'Resultado':<12}"
    separator = "-" * len(header)
    lines = [separator, header, separator]

    for r in resultados:
        val = r['valor']
        val_str = f"{int(val)}" if isinstance(val, (int, float)) and val.is_integer() else f"{val:.4g}"
        lines.append(f"{r['parser_name']:<55} | {r['agrupacion']:<30} | {val_str:<12}")

    lines.append(separator)
    return "\n".join(lines)
