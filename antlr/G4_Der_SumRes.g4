grammar G4_Der_SumRes;

// =============================================================================
// Gramática G4: Precedencia Invertida (+, - > *, /), Asociatividad por la Derecha
// Universidad Sergio Arboleda - Lenguajes de Programación y Transducción
// Docente: Joaquin F. Sanchez
// Grupo 5: Andrés Sebastián Coral Vallejo y Carol Arenas Cardona
// =============================================================================

prog: stat* EOF ;

stat: expr (NEWLINE | ';')* ;

expr
    : term op=('*' | '/') expr    # MulDivRightLower
    | term                        # ToTerm
    ;

term
    : factor op=('+' | '-') term  # AddSubRightHigher
    | factor                      # ToFactor
    ;

factor
    : NUM                         # Number
    | '(' expr ')'                # Parens
    ;

NUM     : [0-9]+ ('.' [0-9]+)? ;
PLUS    : '+' ;
MINUS   : '-' ;
MUL     : '*' ;
DIV     : '/' ;
LPAREN  : '(' ;
RPAREN  : ')' ;
NEWLINE : '\r'? '\n' ;
WS      : [ \t]+ -> skip ;
