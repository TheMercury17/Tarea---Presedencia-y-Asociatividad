grammar G3_Izq_SumRes;

// =============================================================================
// Gramática G3: Precedencia Invertida (+, - > *, /), Asociatividad por la Izquierda
// Grupo 5: Andrés Sebastián Coral Vallejo y Carol Arenas Cardona
// =============================================================================

prog: stat* EOF ;

stat: expr (NEWLINE | ';')* ;

expr
    : expr op=('*' | '/') term    # MulDivLeftLower
    | term                        # ToTerm
    ;

term
    : term op=('+' | '-') factor  # AddSubLeftHigher
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
