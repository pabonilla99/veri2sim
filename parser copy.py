import ply.yacc as yacc
from lexer import tokens
from simulide import Component


# declare a SimulIDE component
component = Component('component1', [], [])

# precedence rules 
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'AND', 'OR'),
    ('left', 'EQEQ', 'NEQ', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'BITAND', 'BITOR', 'BITXOR'),
    ('left', 'LSHIFT', 'RSHIFT'),
    ('right', 'NOT', 'BITNOT'),
)

# Definición de la gramática
def p_module(p):
    '''module : MODULE IDENTIFIER LPAREN port_list RPAREN SEMI module_items ENDMODULE'''
    print('module >> ')
    p[0] = ('module', p[2], p[4], p[7])

def p_port_list(p):
    '''port_list : port
                 | port_list COMMA port'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_port(p):
    '''port : INPUT IDENTIFIER
            | OUTPUT IDENTIFIER'''
    if p[1] == 'input':
        component.inputs.append(p[2])
    elif p[1] == 'output':
        component.outputs.append(p[2])
    p[0] = (p[1], p[2])

def p_module_items(p):
    '''module_items : module_item
                    | module_items module_item'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_module_item(p):
    '''module_item : statement
                   | declaration'''
    p[0] = p[1]

def p_declaration(p):
    '''declaration : WIRE IDENTIFIER SEMI
                   | REG IDENTIFIER SEMI'''
    p[0] = (p[1], p[2])

def p_statement(p):
    '''statement : assignment
                 | if_statement
                 | always_statement'''
    
                #  | case_statement
    p[0] = p[1]

def p_assignment(p):
    '''assignment : ASSIGN IDENTIFIER EQ expression SEMI'''
    p[0] = ('assign', p[2], p[4])

def p_if_statement(p):
    '''if_statement : IF LPAREN expression RPAREN statement
                    | IF LPAREN expression RPAREN statement ELSE statement'''
    if len(p) == 6:
        p[0] = ('if', p[3], p[5])
    else:
        p[0] = ('if', p[3], p[5], p[7])

# def p_case_statement(p):
#     '''case_statement : CASE expression case_items ENDCASE'''
#     p[0] = ('case', p[2], p[3])

# def p_case_items(p):
#     '''case_items : case_item
#                   | case_items case_item'''
#     if len(p) == 2:
#         p[0] = [p[1]]
#     else:
#         p[0] = p[1] + [p[2]]

# def p_case_item(p):
#     '''case_item : expression COLON statement
#                  | DEFAULT COLON statement'''
#     if len(p) == 4:
#         p[0] = (p[1], p[3])
#     else:
#         p[0] = ('default', p[3])

def p_always_statement(p):
    '''always_statement : ALWAYS statement'''
    p[0] = ('always', p[2])

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression AND expression
                  | expression OR expression
                  | expression EQEQ expression
                  | expression NEQ expression
                  | expression LT expression
                  | expression LE expression
                  | expression GT expression
                  | expression GE expression
                  | expression BITAND expression
                  | expression BITOR expression
                  | expression BITXOR expression
                  | expression LSHIFT expression
                  | expression RSHIFT expression'''
    p[0] = (p[2], p[1], p[3])

def p_expression_unop(p):
    '''expression : MINUS expression %prec NOT
                  | NOT expression
                  | BITNOT expression'''
    p[0] = (p[1], p[2])

def p_expression_group(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]

def p_expression_number(p):
    '''expression : NUMBER'''
    p[0] = p[1]

def p_expression_identifier(p):
    '''expression : IDENTIFIER'''
    p[0] = p[1]

# Manejo de errores
def p_error(p):
    print("Syntax error in input!")

# Construir el parser
parser = yacc.yacc()