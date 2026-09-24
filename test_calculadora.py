"""
Suite de Pruebas Unitarias para Análisis de Precedencia y Asociatividad
Universidad Sergio Arboleda - Lenguajes de Programación
Grupo 5: Andrés Sebastián Coral Vallejo y Carol Arenas Cardona

Requisitos validados:
1. Asociatividad por la izquierda
2. Asociatividad por la derecha
3. Precedencia mayor: Multiplicación y División
4. Precedencia mayor: Suma y Resta
"""

import unittest
from src.gramaticas import (
    ParserG1_Izq_MulDiv,
    ParserG2_Der_MulDiv,
    ParserG3_Izq_SumRes,
    ParserG4_Der_SumRes,
)
from src.evaluador import analizar_expresion


class TestPrecedenciaYAsociatividad(unittest.TestCase):

    # =========================================================================
    # REQUISITO 1: ASOCIATIVIDAD POR LA IZQUIERDA
    # =========================================================================
    def test_01_asociatividad_izquierda_resta(self):
        """En G1 (asoc. izquierda), 8 - 3 - 2 debe agruparse como ((8 - 3) - 2) = 3"""
        res = analizar_expresion("8 - 3 - 2", ParserG1_Izq_MulDiv)
        self.assertEqual(res["agrupacion"], "((8 - 3) - 2)")
        self.assertEqual(res["valor"], 3)

    def test_02_asociatividad_izquierda_division(self):
        """En G1 (asoc. izquierda), 24 / 4 / 2 debe agruparse como ((24 / 4) / 2) = 3"""
        res = analizar_expresion("24 / 4 / 2", ParserG1_Izq_MulDiv)
        self.assertEqual(res["agrupacion"], "((24 / 4) / 2)")
        self.assertEqual(res["valor"], 3)

    def test_03_asociatividad_izquierda_cadena_larga(self):
        """En G1, 20 - 5 - 3 - 2 debe ser (((20 - 5) - 3) - 2) = 10"""
        res = analizar_expresion("20 - 5 - 3 - 2", ParserG1_Izq_MulDiv)
        self.assertEqual(res["agrupacion"], "(((20 - 5) - 3) - 2)")
        self.assertEqual(res["valor"], 10)

    # =========================================================================
    # REQUISITO 2: ASOCIATIVIDAD POR LA DERECHA
    # =========================================================================
    def test_04_asociatividad_derecha_resta(self):
        """En G2 (asoc. derecha), 8 - 3 - 2 debe agruparse como (8 - (3 - 2)) = 7"""
        res = analizar_expresion("8 - 3 - 2", ParserG2_Der_MulDiv)
        self.assertEqual(res["agrupacion"], "(8 - (3 - 2))")
        self.assertEqual(res["valor"], 7)

    def test_05_asociatividad_derecha_division(self):
        """En G2 (asoc. derecha), 24 / 4 / 2 debe agruparse como (24 / (4 / 2)) = 12"""
        res = analizar_expresion("24 / 4 / 2", ParserG2_Der_MulDiv)
        self.assertEqual(res["agrupacion"], "(24 / (4 / 2))")
        self.assertEqual(res["valor"], 12)

    def test_06_asociatividad_derecha_cadena_larga(self):
        """En G2, 20 - 5 - 3 - 2 debe ser (20 - (5 - (3 - 2))) = 20 - (5 - 1) = 16"""
        res = analizar_expresion("20 - 5 - 3 - 2", ParserG2_Der_MulDiv)
        self.assertEqual(res["agrupacion"], "(20 - (5 - (3 - 2)))")
        self.assertEqual(res["valor"], 16)

    # =========================================================================
    # REQUISITO 3: PRECEDENCIA MAYOR MULTIPLICACIÓN Y DIVISIÓN (*, / > +, -)
    # =========================================================================
    def test_07_precedencia_estandar_suma_multiplicacion(self):
        """En G1, 2 + 3 * 4 debe evaluar primero la multiplicación: 2 + (3 * 4) = 14"""
        res = analizar_expresion("2 + 3 * 4", ParserG1_Izq_MulDiv)
        self.assertEqual(res["agrupacion"], "(2 + (3 * 4))")
        self.assertEqual(res["valor"], 14)

    def test_08_precedencia_estandar_resta_division(self):
        """En G1, 20 - 6 / 2 debe evaluar primero la división: 20 - (6 / 2) = 17"""
        res = analizar_expresion("20 - 6 / 2", ParserG1_Izq_MulDiv)
        self.assertEqual(res["agrupacion"], "(20 - (6 / 2))")
        self.assertEqual(res["valor"], 17)

    def test_09_precedencia_estandar_mixta_con_ambos_lados(self):
        """En G1, 2 * 3 + 4 * 5 debe agrupar ((2 * 3) + (4 * 5)) = 26"""
        res = analizar_expresion("2 * 3 + 4 * 5", ParserG1_Izq_MulDiv)
        self.assertEqual(res["agrupacion"], "((2 * 3) + (4 * 5))")
        self.assertEqual(res["valor"], 26)

    # =========================================================================
    # REQUISITO 4: PRECEDENCIA MAYOR SUMA Y RESTA (+, - > *, /)
    # =========================================================================
    def test_10_precedencia_invertida_suma_multiplicacion(self):
        """En G3 (Suma > Mult), 2 + 3 * 4 debe evaluar primero la suma: (2 + 3) * 4 = 20"""
        res = analizar_expresion("2 + 3 * 4", ParserG3_Izq_SumRes)
        self.assertEqual(res["agrupacion"], "((2 + 3) * 4)")
        self.assertEqual(res["valor"], 20)

    def test_11_precedencia_invertida_resta_multiplicacion(self):
        """En G3 (Resta > Mult), 10 - 2 * 3 debe evaluar primero la resta: (10 - 2) * 3 = 24"""
        res = analizar_expresion("10 - 2 * 3", ParserG3_Izq_SumRes)
        self.assertEqual(res["agrupacion"], "((10 - 2) * 3)")
        self.assertEqual(res["valor"], 24)

    def test_12_precedencia_invertida_division_suma(self):
        """En G3 (Suma > Div), 20 / 2 + 3 debe evaluar primero la suma: 20 / (2 + 3) = 4"""
        res = analizar_expresion("20 / 2 + 3", ParserG3_Izq_SumRes)
        self.assertEqual(res["agrupacion"], "(20 / (2 + 3))")
        self.assertEqual(res["valor"], 4)

    def test_13_precedencia_invertida_mixta_asociatividad_izquierda(self):
        """En G3, 2 * 3 + 4 * 5 -> ((2 * (3 + 4)) * 5) = 70"""
        res = analizar_expresion("2 * 3 + 4 * 5", ParserG3_Izq_SumRes)
        self.assertEqual(res["agrupacion"], "((2 * (3 + 4)) * 5)")
        self.assertEqual(res["valor"], 70)

    def test_14_precedencia_invertida_mixta_asociatividad_derecha(self):
        """En G4, 2 * 3 + 4 * 5 -> (2 * ((3 + 4) * 5)) = 70"""
        res = analizar_expresion("2 * 3 + 4 * 5", ParserG4_Der_SumRes)
        self.assertEqual(res["agrupacion"], "(2 * ((3 + 4) * 5))")
        self.assertEqual(res["valor"], 70)

    # =========================================================================
    # PRUEBAS ADICIONALES: PARÉNTESIS Y ERRORES SEMÁNTICOS / SINTÁCTICOS
    # =========================================================================
    def test_15_parentesis_fuerzan_orden_en_precedencia_estandar(self):
        """En G1, (2 + 3) * 4 fuerza la suma primero dando 20"""
        res = analizar_expresion("(2 + 3) * 4", ParserG1_Izq_MulDiv)
        self.assertEqual(res["valor"], 20)

    def test_16_parentesis_fuerzan_orden_en_precedencia_invertida(self):
        """En G3, 2 + (3 * 4) fuerza la multiplicación primero dando 14"""
        res = analizar_expresion("2 + (3 * 4)", ParserG3_Izq_SumRes)
        self.assertEqual(res["valor"], 14)

    def test_17_error_division_por_cero(self):
        """División por cero debe lanzar ZeroDivisionError"""
        with self.assertRaises(ZeroDivisionError):
            analizar_expresion("10 / 0", ParserG1_Izq_MulDiv)

    def test_18_error_lexico(self):
        """Caracteres no permitidos como '$' deben lanzar SyntaxError"""
        with self.assertRaises(SyntaxError):
            analizar_expresion("2 + $ 3", ParserG1_Izq_MulDiv)

    def test_19_error_sintactico_operadores_consecutivos(self):
        """Expresiones mal formadas como '2 + * 3' deben lanzar SyntaxError"""
        with self.assertRaises(SyntaxError):
            analizar_expresion("2 + * 3", ParserG1_Izq_MulDiv)


if __name__ == "__main__":
    unittest.main()
