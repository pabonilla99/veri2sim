import ply.yacc as yacc
from lexer import tokens

# Estructura de datos para almacenar la información del módulo
class VerilogModule:
    def __init__(self, name):
        self.name = name
        self.inputs = []
        self.outputs = []
        self.wires = []
        self.statements = []

    def __str__(self):
        return f"Module: {self.name}\nInputs: {self.inputs}\nOutputs: {self.outputs}\nWires: {self.wires}\nStatements: {self.statements}"

# Definición de la gramática
def p_module(p):
    '''module : MODULE IDENTIFIER LPAREN port_list RPAREN SEMI module_items ENDMODULE'''
    p[0] = VerilogModule(p[2])
    p[0].inputs = p[4]['inputs']
    p[0].outputs = p[4]['outputs']
    p[0].wires = p[7]['wires']
    p[0].statements = p[7]['statements']

def p_port_list(p):
    '''port_list : port
                 | port_list COMMA port'''
    if len(p) == 2:
        p[0] = {'inputs': [], 'outputs': []}
        if p[1][0] == 'input':
            p[0]['inputs'].append(p[1][1])
        else:
            p[0]['outputs'].append(p[1][1])
    else:
        p[0] = p[1]
        if p[3][0] == 'input':
            p[0]['inputs'].append(p[3][1])
        else:
            p[0]['outputs'].append(p[3][1])

def p_port(p):
    '''port : INPUT IDENTIFIER
            | OUTPUT IDENTIFIER'''
    p[0] = (p[1], p[2])

def p_module_items(p):
    '''module_items : module_item
                    | module_items module_item'''
    if len(p) == 2:
        p[0] = {'wires': [], 'statements': []}
        if p[1][0] == 'wire':
            p[0]['wires'].append(p[1][1])
        else:
            p[0]['statements'].append(p[1])
    else:
        p[0] = p[1]
        if p[2][0] == 'wire':
            p[0]['wires'].append(p[2][1])
        else:
            p[0]['statements'].append(p[2])

def p_module_item(p):
    '''module_item : wire_declaration
                   | assignment'''
    p[0] = p[1]

def p_wire_declaration(p):
    '''wire_declaration : WIRE IDENTIFIER SEMI'''
    p[0] = ('wire', p[2])

def p_assignment(p):
    '''assignment : ASSIGN IDENTIFIER EQ IDENTIFIER SEMI'''
    p[0] = ('assign', p[2], p[4])

# Manejo de errores
def p_error(p):
    print("Syntax error in input!")

# Construir el parser
parser = yacc.yacc()