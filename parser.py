import ply.yacc as yacc
from lexer import tokens

# Clase para almacenar la información del módulo Verilog
class VerilogModule:
    def __init__(self, name):
        self.name = name
        self.inputs = []
        self.outputs = []
        self.wires = []
        self.statements = []

    def __str__(self):
        return f"Module: {self.name}\nInputs: {self.inputs}\nOutputs: {self.outputs}\nWires: {self.wires}\nStatements: {self.statements}"

# Clase para un símbolo en la tabla de símbolos
class Symbol:
    def __init__(self, name, sym_type):
        self.name = name
        self.type = sym_type

    def __str__(self):
        return f"Symbol(name={self.name}, type={self.type})"

# Clase para la tabla de símbolos
class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def add_symbol(self, name, sym_type):
        if name not in self.symbols:
            self.symbols[name] = Symbol(name, sym_type)
        else:
            print(f"Warning: Symbol {name} already exists in the symbol table.")

    def __str__(self):
        return "\n".join(str(symbol) for symbol in self.symbols.values())

# Crear una instancia de la tabla de símbolos
symbol_table = SymbolTable()


# Definición de la gramática
def p_module(p):
    '''module : MODULE IDENTIFIER LPAREN port_list RPAREN SEMI module_items ENDMODULE'''
    p[0] = VerilogModule(p[2])
    p[0].inputs = p[4]['inputs']
    p[0].outputs = p[4]['outputs']
    p[0].wires = p[7]['wires']
    p[0].statements = p[7]['statements']

    # Agregar el módulo a la tabla de símbolos
    symbol_table.add_symbol(p[2], 'module')
    print(symbol_table)

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

    # Agregar el puerto a la tabla de símbolos
    symbol_table.add_symbol(p[2], p[1])

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

    # Agregar el wire a la tabla de símbolos
    symbol_table.add_symbol(p[2], 'wire')

def p_assignment(p):
    '''assignment : ASSIGN IDENTIFIER EQ expression SEMI'''
    if p[2] in symbol_table.symbols:
        if symbol_table.symbols[p[2]].type == 'output': # output <= statement
            p[0] = f'{p[2]}Pin.setVoltage( {p[4]} );\n'
        else:                                           # wire <= statement
            p[0] = f'{p[2]} = {p[4]};\n' 

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
    p[0] = f'{p[2]} {p[1]} {p[3]}'

# Definición de la precedencia de los operadores
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'AND', 'OR'),
    ('left', 'EQEQ', 'NEQ'),
    ('left', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'BITAND', 'BITOR', 'BITXOR'),
    ('left', 'LSHIFT', 'RSHIFT'),
    ('right', 'NOT', 'BITNOT'),
)

def p_expression_unop(p):
    '''expression : MINUS expression %prec NOT
                  | NOT expression
                  | BITNOT expression'''
    p[0] = f'{p[1]}{p[2]}'

def p_expression_group(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = f'({p[2]})'

def p_expression_number(p):
    '''expression : NUMBER'''
    p[0] = p[1]

def p_expression_identifier(p):
    '''expression : IDENTIFIER'''
    if p[1] in symbol_table.symbols:
        if symbol_table.symbols[p[1]].type == 'input':
            p[0] = f'{p[1]}Pin.getVoltage()'
        else:
            p[0] = p[1]

# Manejo de errores
def p_error(p):
    print("Syntax error in input!")

# Construir el parser
parser = yacc.yacc()