import ply.yacc as yacc
from src.lexer import tokens


# Class to store Verilog module information
class VerilogModule:
    def __init__(self, name):
        self.name = name
        self.statements = []
        self.symbols = symbol_table.symbols

    def __str__(self):
        return f"Module: {self.name}\nStatements: {self.statements}\nSymbols: {self.symbols}"


# Class for a symbol in the symbol table
class Symbol:
    def __init__(self, name, sym_type, msb=None, lsb=None):
        self.name = name
        self.type = sym_type
        self.msb = msb
        self.lsb = lsb

    def __str__(self):
        return f"Symbol(name={self.name}, type={self.type}, msb={self.msb}, lsb={self.lsb})"


# Class for the symbol table
class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def add_symbol(self, name, sym_type, msb=None, lsb=None):
        if name not in self.symbols:
            self.symbols[name] = Symbol(name, sym_type, msb, lsb)
        else:
            print(f"Warning: Symbol {name} already exists in the symbol table.")

    def modify_symbol(self, name, sym_type=None, msb=None, lsb=None):
        if name in self.symbols:
            if sym_type is not None:
                self.symbols[name].type = sym_type
            if msb is not None:
                self.symbols[name].msb = msb
            if lsb is not None:
                self.symbols[name].lsb = lsb
        else:
            print(f"Error: Symbol {name} does not exist in the symbol table.")

    def __str__(self):
        return "\n".join(str(symbol) for symbol in self.symbols.values())


# Create an instance of the symbol table
symbol_table = SymbolTable()


# Grammar definition
def p_module(p):
    """module : MODULE IDENTIFIER LPAREN port_list RPAREN SEMI module_items ENDMODULE"""
    p[0] = VerilogModule(p[2])
    p[0].statements = p[7]["statements"]

    # Add the module to the symbol table
    symbol_table.add_symbol(p[2], "module")
    # print(symbol_table)
    print("module:\t", p[2])


def p_port_list(p):
    """port_list    : port
                    | port_list COMMA port"""
    if len(p) == 2:
        p[0] = p[1]
        print("port_list:\t", p[1]) 
    else:
        p[0] = f"{p[1], p[3]}"
        print("port_list:\t", f"{p[1], p[3]}") 
    


def p_port(p):
    """port     : INPUT range_opt IDENTIFIER
                | OUTPUT range_opt IDENTIFIER
                | range_opt IDENTIFIER"""
    if len(p) == 4:  # INPUT or OUTPUT defined
        port_type = p[1]
        range_opt = p[2]
        identifier = p[3]
    else:  # No INPUT or OUTPUT defined
        port_type = "unspecified"
        range_opt = p[1]
        identifier = p[2]

    if range_opt:
        p[0] = f"{port_type}, {identifier}"  # when bit array
        msb, lsb = range_opt
    else:
        p[0] = f"{port_type}, {identifier}"  # when single bit
        msb, lsb = 0, 0

    # Add the port to the symbol table
    symbol_table.add_symbol(identifier, port_type, msb, lsb)
    print("port:\t", identifier) 


def p_range_opt(p):
    """range_opt : LSQUARE NUMBER COLON NUMBER RSQUARE
    | empty"""
    if len(p) == 6:
        p[0] = (int(p[2]), int(p[4]))
    else:
        p[0] = None


def p_empty(p):
    """empty :"""
    p[0] = '// empty'
    # pass


def p_module_items(p):
    """module_items : module_item
    | module_items module_item"""
    if len(p) == 2:
        p[0] = {"statements": []}
        # if "// wire " not in p[1]:
        p[0]["statements"].append(p[1])
    else:
        p[0] = p[1]
        # if "// wire " not in p[2]:
        p[0]["statements"].append(p[2])


def p_module_item(p):
    """module_item : wire_declaration
    | identifier_definition
    | assign_block
    | always_block
    | empty"""
    p[0] = p[1]


def p_identifier_definition(p):
    """identifier_definition : INPUT identifier_list SEMI
    | OUTPUT identifier_list SEMI"""
    port_type = p[1]
    identifiers = p[2]
    for identifier in identifiers:
        symbol_table.modify_symbol(identifier, port_type, 0, 0)


def p_identifier_list(p):
    """identifier_list : IDENTIFIER
    | identifier_list COMMA IDENTIFIER"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_wire_declaration(p):
    """wire_declaration : WIRE range_opt IDENTIFIER SEMI"""
    p[0] = f"// wire {p[3]}"
    if p[2]:
        msb, lsb = p[2]
    else:
        msb, lsb = 0, 0

        print("port_list:\t", f"{p[1], p[3]}") 
    # Add the wire to the symbol table
    symbol_table.add_symbol(p[3], "wire", msb, lsb)


def p_assign_block(p):
    """assign_block : ASSIGN assignment SEMI"""
    p[0] = f"// assign\n{p[2]};"

def p_assignment(p):
    """assignment : IDENTIFIER EQ expression"""
    print(f"assignment: {p[1]} = {p[3]}")
    if p[1] in symbol_table.symbols:
        if symbol_table.symbols[p[1]].type == "output":  # output <= statement
            if symbol_table.symbols[p[1]].msb == symbol_table.symbols[p[1]].lsb:
                p[0] = f"{p[1]}Pin.setOutState({p[3]})"
            else:
                p[0] = f"{p[1]}Port.setOutState({p[3]})"
        else:  # wire <= statement
            p[0] = f"{p[1]} = {p[3]}"


def p_expression_binop(p):
    """expression : expression PLUS expression
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
    | expression RSHIFT expression"""
    p[0] = f"{p[1]} {p[2]} {p[3]}"


# Operator precedence definition
precedence = (
    ("left", "PLUS", "MINUS"),
    ("left", "TIMES", "DIVIDE"),
    ("left", "AND", "OR"),
    ("left", "EQEQ", "NEQ"),
    ("left", "LT", "LE", "GT", "GE"),
    ("left", "BITAND", "BITOR", "BITXOR"),
    ("left", "LSHIFT", "RSHIFT"),
    ("right", "NOT", "BITNOT"),
)


def p_expression_unop(p):
    """expression : MINUS expression %prec NOT
    | NOT expression
    | BITNOT expression"""
    exp = p[2].replace("Pin.getInpState()", "")
    if exp in symbol_table.symbols:
        if (
            symbol_table.symbols[exp].msb == symbol_table.symbols[exp].lsb
            and p.slice[1].type == "BITNOT"
        ):
            # change "~" by "!" for one bit variables
            p[0] = f"!{p[2]}"
        else:
            p[0] = f"{p[1]}{p[2]}"
    else:
        p[0] = f"{p[1]}{p[2]}"


def p_expression_group(p):
    """expression : LPAREN expression RPAREN"""
    p[0] = f"({p[2]})"


def p_expression_number(p):
    """expression : NUMBER"""
    p[0] = p[1]


def p_expression_identifier(p):
    """expression : IDENTIFIER"""
    if p[1] in symbol_table.symbols:
        if symbol_table.symbols[p[1]].type == "input":
            if symbol_table.symbols[p[1]].msb == symbol_table.symbols[p[1]].lsb:
                p[0] = f"{p[1]}Pin.getInpState()"
            else:
                p[0] = f"{p[1]}Port.getInpState()"
        else:
            p[0] = p[1]


def p_always_block(p):
    """always_block : ALWAYS AT sensitivity_list statement_block"""
    p[0] = f'// --- always ---\n// {p[3]}\n'
    for stmt in p[4]:
        p[0] += f"{stmt};\n"
    p[0] += '// --------------'

def p_sensitivity_list(p):
    """sensitivity_list : LPAREN sensitivity_items RPAREN"""
    p[0] = p[2]

def p_sensitivity_items(p):
    """sensitivity_items : IDENTIFIER
    | sensitivity_items OR_KW IDENTIFIER"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_statement_block(p):
    """statement_block : BEGIN statement_list END"""
    print("statement_block:\t", p[2])
    p[0] = p[2]

def p_statement_list(p):
    """statement_list : statement
    | statement_list statement"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement(p):
    """statement : assignment SEMI
    | if_block
    | empty""" 
    p[0] = p[1]

def p_if_block(p):
    """if_block : IF LPAREN expression RPAREN statement else_block_opt
                | IF LPAREN expression RPAREN statement_block else_block_opt"""
    if isinstance(p[5], list):
        body = "{\n" + "".join(f"{stmt};\n" for stmt in p[5]) + "}"
    else:
        body = f"{p[5]}"
    p[0] = f"if ({p[3]}) {body};\n{p[6]}"

def p_else_block_opt(p):
    """else_block_opt   : ELSE statement
                        | ELSE statement_block
                        | empty"""
    if len(p) == 3:
        if isinstance(p[2], list):
            body = "{\n" + "".join(f"{stmt};\n" for stmt in p[2]) + "}"
        else:
            body = f"{p[2]}"
        p[0] = f"else {body}"
    else:
        p[0] = ""


# Error handling
def p_error(p):
    print("Syntax error in input!")


# Build the parser
parser = yacc.yacc()
