# Tarea: Análisis de Precedencia y Asociatividad en Gramáticas

**Universidad Sergio Arboleda**  
**Escuela de Ciencias Exactas e Ingeniería**  
**Materia:** Lenguajes de Programación y Transducción  
**Docente:** Joaquin F. Sanchez  
**Grupo 5:**
- **Andrés Sebastián Coral Vallejo**
- **Carol Arenas Cardona**

---

## Tabla de Contenidos
1. [Descripción General y Objetivos](#descripción-general-y-objetivos)
2. [Fundamento Teórico](#fundamento-teórico)
   - [El Problema de la Ambigüedad](#el-problema-de-la-ambigüedad)
   - [Mecanismo de Asociatividad en Gramáticas Libres de Contexto](#mecanismo-de-asociatividad-en-gramáticas-libres-de-contexto)
   - [Mecanismo de Precedencia Mediante Estratificación](#mecanismo-de-precedencia-mediante-estratificación)
3. [Definición Formal de las 4 Gramáticas Evaluadas](#definición-formal-de-las-4-gramáticas-evaluadas)
   - [Gramática G1: Precedencia Estándar (*, / > +, -) | Asociatividad Izquierda](#gramática-g1-precedencia-estándar---+-asociatividad-izquierda)
   - [Gramática G2: Precedencia Estándar (*, / > +, -) | Asociatividad Derecha](#gramática-g2-precedencia-estándar---+-asociatividad-derecha)
   - [Gramática G3: Precedencia Invertida (+, - > *, /) | Asociatividad Izquierda](#gramática-g3-precedencia-invertida-+---asociatividad-izquierda)
   - [Gramática G4: Precedencia Invertida (+, - > *, /) | Asociatividad Derecha](#gramática-g4-precedencia-invertida-+---asociatividad-derecha)
4. [Batería de Pruebas y Matriz Comparativa](#batería-de-pruebas-y-matriz-comparativa)
   - [1. Demostración de Asociatividad por la Izquierda](#1-demostración-de-asociatividad-por-la-izquierda)
   - [2. Demostración de Asociatividad por la Derecha](#2-demostración-de-asociatividad-por-la-derecha)
   - [3. Demostración de Precedencia Mayor: Multiplicación y División](#3-demostración-de-precedencia-mayor-multiplicación-y-división)
   - [4. Demostración de Precedencia Mayor: Suma y Resta](#4-demostración-de-precedencia-mayor-suma-y-resta)
   - [5. Caso de Interacción Completa (Precedencia + Asociatividad Mixta)](#5-caso-de-interacción-completa-precedencia--asociatividad-mixta)
5. [Estructura del Proyecto](#estructura-del-proyecto)
6. [Instrucciones de Ejecución y Validación](#instrucciones-de-ejecución-y-validación)
7. [Conclusiones del Análisis](#conclusiones-del-análisis)

---

## Descripción General y Objetivos

El presente taller tiene como propósito diseñar, formalizar, implementar y contrastar empíricamente las diferentes formas en las que una **Gramática Libre de Contexto (CFG)** para una calculadora aritmética con las operaciones `+`, `-`, `*` y `/` modela:
- **Asociatividad por la izquierda** vs. **Asociatividad por la derecha**.
- **Precedencia mayor de Multiplicación y División** (`*`, `/` > `+`, `-`) vs. **Precedencia mayor de Suma y Resta** (`+`, `-` > `*`, `/`).

El proyecto incluye:
1. Especificación formal en notación **BNF/EBNF** y especificación en **ANTLR4** (`.g4`).
2. Implementación algorítmica en **Python** de analizadores sintácticos descendentes, constructores de Árboles de Sintaxis Abstracta (AST) y evaluadores semánticos.
3. Suite de **19 pruebas unitarias automatizadas (`unittest`)** que certifican el cumplimiento de cada requisito.
4. CLI interactivo y demostrador con generación de árboles en texto jerárquico.

---

## Fundamento Teórico

### El Problema de la Ambigüedad
Una gramática ingenua o clásica no estratificada para una calculadora:
$$E \to E + E \mid E - E \mid E * E \mid E / E \mid \text{num}$$
es **ambigua**, ya que una misma cadena como `8 - 3 - 2` o `2 + 3 * 4` admite múltiples árboles de derivación con interpretaciones semánticas contradictorias.

### Mecanismo de Asociatividad en Gramáticas Libres de Contexto
La asociatividad determina cómo se agrupan operadores de la misma jerarquía cuando aparecen en secuencia:

1. **Asociatividad por la Izquierda (Left-Associativity):**
   - Una operación binaria $\odot$ es asociativa por la izquierda si $a \odot b \odot c$ equivale a $(a \odot b) \odot c$.
   - En una gramática formal, se modela mediante **recursión por la izquierda**:
     $$A \to A \odot B \mid B$$
     El símbolo recursivo $A$ está a la izquierda del operador, lo que hace que el árbol crezca hacia abajo y a la izquierda. En una evaluación ascendente (*bottom-up*) o evaluación de subárboles, el operando izquierdo se reduce primero.
   - **Ejemplo en Resta:** `8 - 3 - 2` $\implies$ `(8 - 3) - 2 = 5 - 2 = 3`.
   - **Ejemplo en División:** `24 / 4 / 2` $\implies$ `(24 / 4) / 2 = 6 / 2 = 3`.

2. **Asociatividad por la Derecha (Right-Associativity):**
   - Una operación binaria $\odot$ es asociativa por la derecha si $a \odot b \odot c$ equivale a $a \odot (b \odot c)$.
   - En una gramática formal, se modela mediante **recursión por la derecha**:
     $$A \to B \odot A \mid B$$
     El símbolo recursivo $A$ está a la derecha del operador, lo que hace que el árbol crezca hacia abajo y a la derecha. El operando derecho se evalúa primero.
   - **Ejemplo en Resta:** `8 - 3 - 2` $\implies$ `8 - (3 - 2) = 8 - 1 = 7`.
   - **Ejemplo en División:** `24 / 4 / 2` $\implies$ `24 / (4 / 2) = 24 / 2 = 12`.

### Mecanismo de Precedencia Mediante Estratificación
La precedencia entre distintos operadores se logra dividiendo la gramática en **niveles jerárquicos (estratificación de no terminales)**:
- **Regla de oro de compiladores:** El operador que debe evaluarse **primero** (mayor precedencia) debe ubicarse en el nivel más **profundo** del árbol sintáctico (más próximo a los factores u operandos atómicos).
- El operador que debe evaluarse **al final** (menor precedencia) debe ubicarse en el nivel más **alto** (más cercano al símbolo inicial $E$).

---

## Definición Formal de las 4 Gramáticas Evaluadas

Para cubrir el $100\%$ de las combinaciones solicitadas en el enunciado, se definen cuatro gramáticas exactas:

### Gramática G1: Precedencia Estándar (*, / > +, -) | Asociatividad Izquierda
- **Precedencia:** `*`, `/` > `+`, `-`
- **Asociatividad:** Izquierda para todos los operadores.
- **Producciones BNF:**
  $$E \to E + T \mid E - T \mid T$$
  $$T \to T * F \mid T / F \mid F$$
  $$F \to \text{NUM} \mid ( E )$$

### Gramática G2: Precedencia Estándar (*, / > +, -) | Asociatividad Derecha
- **Precedencia:** `*`, `/` > `+`, `-`
- **Asociatividad:** Derecha para todos los operadores.
- **Producciones BNF:**
  $$E \to T + E \mid T - E \mid T$$
  $$T \to F * T \mid F / T \mid F$$
  $$F \to \text{NUM} \mid ( E )$$

### Gramática G3: Precedencia Invertida (+, - > *, /) | Asociatividad Izquierda
- **Precedencia:** `+`, `-` > `*`, `/`
- **Asociatividad:** Izquierda para todos los operadores.
- **Producciones BNF:**
  $$E \to E * T \mid E / T \mid T$$
  $$T \to T + F \mid T - F \mid F$$
  $$F \to \text{NUM} \mid ( E )$$

### Gramática G4: Precedencia Invertida (+, - > *, /) | Asociatividad Derecha
- **Precedencia:** `+`, `-` > `*`, `/`
- **Asociatividad:** Derecha para todos los operadores.
- **Producciones BNF:**
  $$E \to T * E \mid T / E \mid T$$
  $$T \to F + T \mid F - T \mid F$$
  $$F \to \text{NUM} \mid ( E )$$

---

## Batería de Pruebas y Matriz Comparativa

A continuación se presentan los resultados exactos arrojados por los analizadores sintácticos y evaluadores implementados:

### 1. Demostración de Asociatividad por la Izquierda

| Expresión de Entrada | G1 (Asoc. Izquierda) | G2 (Asoc. Derecha) | Justificación Teórica |
| :--- | :--- | :--- | :--- |
| `8 - 3 - 2` | `((8 - 3) - 2)` = **3** | `(8 - (3 - 2))` = **7** | En G1 la resta izquierda `(8-3)` se evalúa primero. En G2 la resta derecha `(3-2)=1` se evalúa primero, dando `8-1=7`. |
| `24 / 4 / 2` | `((24 / 4) / 2)` = **3** | `(24 / (4 / 2))` = **12** | En G1: `6 / 2 = 3`. En G2: `24 / 2 = 12`. Demuestra que la división no es conmutativa ni asociativa por defecto sin definir la gramática. |
| `20 - 5 - 3 - 2` | `(((20 - 5) - 3) - 2)` = **10** | `(20 - (5 - (3 - 2)))` = **16** | Cadena de 3 restas sucesivas: colapso lineal a la izquierda vs. a la derecha. |

#### Visualización del Árbol AST para `8 - 3 - 2`
```text
[G1 - Asociatividad Izquierda]           [G2 - Asociatividad Derecha]
         Op(-)                                    Op(-)
        /     \                                  /     \
     Op(-)    Num(2)                          Num(8)   Op(-)
    /     \                                           /     \
 Num(8)  Num(3)                                    Num(3)  Num(2)
```

---

### 2. Demostración de Asociatividad por la Derecha
Al evaluar `100 / 10 / 2 / 5`:
- **Bajo Asociatividad Izquierda (G1):**
  $$(((100 / 10) / 2) / 5) = ((10 / 2) / 5) = (5 / 5) = \mathbf{1}$$
- **Bajo Asociatividad Derecha (G2):**
  $$(100 / (10 / (2 / 5))) = (100 / (10 / 0.4)) = (100 / 25) = \mathbf{4}$$

---

### 3. Demostración de Precedencia Mayor: Multiplicación y División

| Expresión de Entrada | G1 / G2 (Precedencia Estándar: `*`, `/` > `+`, `-`) | G3 / G4 (Precedencia Invertida: `+`, `-` > `*`, `/`) | Diferencia Conceptual |
| :--- | :--- | :--- | :--- |
| `2 + 3 * 4` | `(2 + (3 * 4))` = **14** | `((2 + 3) * 4)` = **20** | En G1/G2 la multiplicación está más abajo en el árbol y se computa antes. En G3/G4 la suma está en el nivel inferior y absorbe los operandos primero. |
| `20 - 6 / 2` | `(20 - (6 / 2))` = **17** | `((20 - 6) / 2)` = **7** | En G1/G2: `20 - 3 = 17`. En G3/G4: `14 / 2 = 7`. |
| `2 * 3 + 4 * 5` | `((2 * 3) + (4 * 5))` = **26** | Ver interacción mixta más abajo | En G1/G2 ambos productos se realizan antes de la adición central (`6 + 20 = 26`). |

#### Visualización del Árbol AST para `2 + 3 * 4`
```text
[G1 - Precedencia Estándar: * > +]       [G3 - Precedencia Invertida: + > *]
         Op(+)                                    Op(*)
        /     \                                  /     \
     Num(2)   Op(*)                           Op(+)    Num(4)
             /     \                         /     \
          Num(3)  Num(4)                  Num(2)  Num(3)
```

---

### 4. Demostración de Precedencia Mayor: Suma y Resta

| Expresión de Entrada | G3 (Invertida, Izq) | G4 (Invertida, Der) | Comparación con G1 (Estándar) |
| :--- | :--- | :--- | :--- |
| `10 - 2 * 3` | `((10 - 2) * 3)` = **24** | `((10 - 2) * 3)` = **24** | En G1 estándar daría `10 - 6 = 4`. En G3/G4 la resta se realiza primero: `8 * 3 = 24`. |
| `20 / 2 + 3` | `(20 / (2 + 3))` = **4** | `(20 / (2 + 3))` = **4** | En G1 estándar daría `10 + 3 = 13`. En G3/G4 la suma se realiza primero: `20 / 5 = 4`. |

---

### 5. Caso de Interacción Completa (Precedencia + Asociatividad Mixta)

Expresión analizada: **`16 / 4 / 2 + 3 * 2`**

| Gramática | Agrupación Sintáctica Generada | Cálculo Paso a Paso | Resultado |
| :--- | :--- | :--- | :--- |
| **G1** (Prec: `*, /` > `+, -` \| Asoc: Izquierda) | `(((16 / 4) / 2) + (3 * 2))` | `(4 / 2) + 6 = 2 + 6` | **8** |
| **G2** (Prec: `*, /` > `+, -` \| Asoc: Derecha) | `((16 / (4 / 2)) + (3 * 2))` | `(16 / 2) + 6 = 8 + 6` | **14** |
| **G3** (Prec: `+, -` > `*, /` \| Asoc: Izquierda) | `(((16 / 4) / (2 + 3)) * 2)` | `(4 / 5) * 2 = 0.8 * 2` | **1.6** |
| **G4** (Prec: `+, -` > `*, /` \| Asoc: Derecha) | `(16 / (4 / ((2 + 3) * 2)))` | `16 / (4 / (5 * 2)) = 16 / (4 / 10) = 16 / 0.4` | **40** |

> **Conclusión Clave:** Una misma expresión aritmética produce **4 resultados completamente diferentes** ($8$, $14$, $1.6$, $40$) demostrando de forma contundente cómo la formulación de la gramática libre de contexto gobierna tanto la precedencia como la asociatividad del lenguaje.

---

## Estructura del Proyecto

```text
Tarea - Presedencia y Asociatividad/
├── README.md                      # Documentación teórica y reporte formal de resultados
├── requirements.txt               # Dependencias del proyecto
├── main.py                        # Demostrador interactivo y ejecutor de casos de prueba
├── test_calculadora.py            # Suite de 19 pruebas unitarias automatizadas (unittest)
├── src/
│   ├── __init__.py                # Inicializador del paquete
│   ├── ast_nodes.py               # Definición de clases de nodos AST y evaluador recursivo
│   ├── lexer.py                   # Analizador léxico (tokenizador basado en expresiones regulares)
│   ├── parser_base.py             # Clase base de parsing con utilidades sintácticas
│   ├── gramaticas.py              # Implementación formal de los 4 Parsers (G1, G2, G3, G4)
│   └── evaluador.py               # Orquestador de análisis, comparación y formateo
└── antlr/
    ├── G1_Izq_MulDiv.g4           # Gramática ANTLR4: Prec estándar, Asoc Izquierda
    ├── G2_Der_MulDiv.g4           # Gramática ANTLR4: Prec estándar, Asoc Derecha
    ├── G3_Izq_SumRes.g4           # Gramática ANTLR4: Prec invertida, Asoc Izquierda
    └── G4_Der_SumRes.g4           # Gramática ANTLR4: Prec invertida, Asoc Derecha
```

---

## Instrucciones de Ejecución y Validación

### 1. Clonar el repositorio
```bash
git clone https://github.com/TheMercury17/Tarea---Presedencia-y-Asociatividad.git
cd Tarea---Presedencia-y-Asociatividad
```

### 2. Ejecutar la Suite de Pruebas Unitarias
Para validar automáticamente el 100% de los requisitos del enunciado:
```bash
python -m unittest test_calculadora.py -v
```

Salida esperada:
```text
test_01_asociatividad_izquierda_resta ... ok
test_02_asociatividad_izquierda_division ... ok
test_03_asociatividad_izquierda_cadena_larga ... ok
test_04_asociatividad_derecha_resta ... ok
test_05_asociatividad_derecha_division ... ok
test_06_asociatividad_derecha_cadena_larga ... ok
test_07_precedencia_estandar_suma_multiplicacion ... ok
test_08_precedencia_estandar_resta_division ... ok
test_09_precedencia_estandar_mixta_con_ambos_lados ... ok
test_10_precedencia_invertida_suma_multiplicacion ... ok
test_11_precedencia_invertida_resta_multiplicacion ... ok
test_12_precedencia_invertida_division_suma ... ok
test_13_precedencia_invertida_mixta_asociatividad_izquierda ... ok
test_14_precedencia_invertida_mixta_asociatividad_derecha ... ok
test_15_parentesis_fuerzan_orden_en_precedencia_estandar ... ok
test_16_parentesis_fuerzan_orden_en_precedencia_invertida ... ok
test_17_error_division_por_cero ... ok
test_18_error_lexico ... ok
test_19_error_sintactico_operadores_consecutivos ... ok

----------------------------------------------------------------------
Ran 19 tests in 0.003s

OK
```

### 3. Ejecutar la Demostración General
Para visualizar las comparaciones tabulares y los árboles AST impresos en terminal:
```bash
python main.py
```

### 4. Ejecutar el Modo Interactivo
Para evaluar expresiones personalizadas ingresadas por el usuario:
```bash
python main.py --interactivo
```

---

## Conclusiones del Análisis

1. **La asociatividad es una propiedad de la dirección de recursión:**
   - La recursión izquierda (`E -> E op T | T`) fuerza a que los árboles crezcan hacia la izquierda, agrupando las operaciones anteriores antes de procesar las posteriores.
   - La recursión derecha (`E -> T op E | T`) pospone la reducción del operador actual hasta que toda la subexpresión derecha haya sido analizada.

2. **La precedencia es una propiedad de la profundidad sintáctica:**
   - La estratificación de no terminales permite definir prioridades sin ambigüedad. Al colocar `+` y `-` en el no terminal `term` (más cercano a `factor`) en G3 y G4, se invierte por completo el comportamiento algebraico estándar, obligando al analizador a resolver sumas y restas antes de las multiplicaciones y divisiones.

3. **Inmunidad del uso de paréntesis:**
   - En las cuatro gramáticas, la producción de factor $F \to ( E )$ permite al usuario o programador alterar arbitrariamente el orden natural de la gramática, garantizando consistencia con la notación matemática universal.
