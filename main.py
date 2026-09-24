"""
Programa Principal de Demostración y Pruebas
Tarea: Análisis de Precedencia y Asociatividad
Universidad Sergio Arboleda - Lenguajes de Programación

Grupo 5:
- Andrés Sebastián Coral Vallejo
- Carol Arenas Cardona
"""

import sys
from src.evaluador import comparar_todas, formatear_tabla_comparativa, analizar_expresion
from src.gramaticas import ALL_PARSERS

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


EJEMPLOS_DEMO = [
    {
        "titulo": "1. ASOCIATIVIDAD POR LA IZQUIERDA (Resta y División sucesivas)",
        "descripcion": (
            "Se evalúa '8 - 3 - 2' y '24 / 4 / 2'.\n"
            "En asociatividad izquierda (G1, G3), se agrupa de izquierda a derecha: ((8 - 3) - 2) = 3 y ((24 / 4) / 2) = 3.\n"
            "En asociatividad derecha (G2, G4), se agrupa de derecha a izquierda: (8 - (3 - 2)) = 7 y (24 / (4 / 2)) = 12."
        ),
        "expresiones": ["8 - 3 - 2", "24 / 4 / 2"]
    },
    {
        "titulo": "2. PRECEDENCIA MAYOR: MULTIPLICACIÓN Y DIVISIÓN (*, / > +, -)",
        "descripcion": (
            "Se evalúa '2 + 3 * 4' y '20 - 6 / 2'.\n"
            "Con precedencia estándar (G1, G2), el operador '*' se evalúa primero: 2 + (3 * 4) = 14.\n"
            "Con precedencia invertida (G3, G4), el operador '+' se evalúa primero: (2 + 3) * 4 = 20."
        ),
        "expresiones": ["2 + 3 * 4", "20 - 6 / 2"]
    },
    {
        "titulo": "3. PRECEDENCIA MAYOR: SUMA Y RESTA (+, - > *, /)",
        "descripcion": (
            "Se evalúa '10 - 2 * 3' y '20 / 2 + 3'.\n"
            "Con precedencia invertida (G3, G4), la resta y suma ligan con mayor fuerza:\n"
            "(10 - 2) * 3 = 24 y 20 / (2 + 3) = 4.\n"
            "En contraste con la estándar (G1, G2): 10 - (2 * 3) = 4 y (20 / 2) + 3 = 13."
        ),
        "expresiones": ["10 - 2 * 3", "20 / 2 + 3"]
    },
    {
        "titulo": "4. INTERACCIÓN COMPLEJA: PRECEDENCIA Y ASOCIATIVIDAD COMBINADAS",
        "descripcion": (
            "Se evalúa '2 * 3 + 4 * 5' y '16 / 4 / 2 + 3 * 2'.\n"
            "Permite observar cómo la jerarquía de operadores y la dirección de recursión moldean el árbol sintáctico."
        ),
        "expresiones": ["2 * 3 + 4 * 5", "16 / 4 / 2 + 3 * 2"]
    }
]


def imprimir_encabezado():
    print("=" * 80)
    print(" UNIVERSIDAD SERGIO ARBOLEDA - ESCUELA DE CIENCIAS EXACTAS E INGENIERÍA")
    print(" TALLER: ANÁLISIS DE PRECEDENCIA Y ASOCIATIVIDAD EN GRAMÁTICAS")
    print(" Materia: Lenguajes de Programación")
    print(" Grupo 5:")
    print("   - Andrés Sebastián Coral Vallejo")
    print("   - Carol Arenas Cardona")
    print("=" * 80)


def ejecutar_demostracion():
    imprimir_encabezado()
    print("\nIniciando demostración sistemática de los 4 requerimientos del enunciado...\n")

    for idx, seccion in enumerate(EJEMPLOS_DEMO, 1):
        print("\n" + "#" * 80)
        print(f" CASO {idx}: {seccion['titulo']}")
        print("#" * 80)
        print(f"Explicación teórica:\n{seccion['descripcion']}\n")

        for expr in seccion["expresiones"]:
            print(f"\n>>> Expresión de prueba: '{expr}'")
            resultados = comparar_todas(expr)
            print(formatear_tabla_comparativa(resultados))

            # Mostrar un árbol AST de muestra representativo
            print("\nÁrbol AST resultante bajo Precedencia Estándar (G1):")
            print(resultados[0]["arbol"])
            print("Árbol AST resultante bajo Precedencia Invertida (G3):")
            print(resultados[2]["arbol"])


def modo_interactivo():
    print("\n" + "=" * 80)
    print(" MODO INTERACTIVO: Evaluador de Expresiones Aritméticas")
    print(" Ingrese una expresión matemática con +, -, *, /, números y paréntesis.")
    print(" Escriba 'salir' o 'exit' para terminar.")
    print("=" * 80)

    while True:
        try:
            expr = input("\nIngrese expresión > ").strip()
            if not expr:
                continue
            if expr.lower() in ("salir", "exit", "quit"):
                print("Saliendo del evaluador. ¡Hasta pronto!")
                break

            resultados = comparar_todas(expr)
            print("\nResultados comparativos en las 4 Gramáticas:")
            print(formatear_tabla_comparativa(resultados))

            print("\n¿Desea ver los árboles sintácticos detallados? (s/n): ", end="")
            opc = input().strip().lower()
            if opc in ("s", "si", "y", "yes"):
                for r in resultados:
                    print(f"\n--- {r['parser_name']} ---")
                    print(f"Agrupación: {r['agrupacion']} = {r['valor']}")
                    print(r['arbol'])

        except Exception as e:
            print(f"Error procesando expresión: {e}")


def main():
    ejecutar_demostracion()
    if len(sys.argv) > 1 and sys.argv[1] == "--interactivo":
        modo_interactivo()


if __name__ == "__main__":
    main()
