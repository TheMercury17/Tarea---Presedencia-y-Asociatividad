grammar G1_Izq_MulDiv;

// =============================================================================
// Gramática G1: Precedencia Estándar (*, / > +, -), Asociatividad por la Izquierda
// Universidad Sergio Arboleda - Lenguajes de Programación y Transducción
// Docente: Joaquin F. Sanchez
// Grupo 5: Andrés Sebastián Coral Vallejo y Carol Arenas Cardona
// =============================================================================

prog: stat* EOF ;

stat: expr (NEWLINE | ';')* ;

expr
    : expr op=('+' | '-') term    # AddSubLeft
    | term                        # ToTerm
    ;

term
    : term op=('*' | '/') factor  # MulDivLeft
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
