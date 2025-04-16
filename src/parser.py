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
    print(symbol_table)


def p_port_list(p):
    """port_list : port
    | port_list COMMA port"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = f"{p[1], p[3]}"


def p_port(p):
    """port : INPUT range_opt IDENTIFIER
    | OUTPUT range_opt IDENTIFIER"""
    if p[2]:
        p[0] = f"{p[1]}, {p[3]}"  # when bit array
        msb, lsb = p[2]
    else:
        p[0] = f"{p[1]}, {p[3]}"  # when single bit
        msb, lsb = 0, 0

    # Add the port to the symbol table
    symbol_table.add_symbol(p[3], p[1], msb, lsb)


def p_range_opt(p):
    """range_opt : LSQUARE NUMBER COLON NUMBER RSQUARE
    | empty"""
    if len(p) == 6:
        p[0] = (int(p[2]), int(p[4]))
    else:
        p[0] = None


def p_empty(p):
    """empty :"""
    pass


def p_module_items(p):
    """module_items : module_item
    | module_items module_item"""
    if len(p) == 2:
        p[0] = {"statements": []}
        if "// wire " not in p[1]:
            p[0]["statements"].append(p[1])
    else:
        p[0] = p[1]
        if "// wire " not in p[2]:
            p[0]["statements"].append(p[2])


def p_module_item(p):
    """module_item : wire_declaration
    | assignment"""
    p[0] = p[1]


def p_wire_declaration(p):
    """wire_declaration : WIRE range_opt IDENTIFIER SEMI"""
    p[0] = f"// wire {p[3]}"
    if p[2]:
        msb, lsb = p[2]
    else:
        msb, lsb = 0, 0

    # Add the wire to the symbol table
    symbol_table.add_symbol(p[3], "wire", msb, lsb)


def p_assignment(p):
    """assignment : ASSIGN IDENTIFIER EQ expression SEMI"""
    if p[2] in symbol_table.symbols:
        if symbol_table.symbols[p[2]].type == "output":  # output <= statement
            if symbol_table.symbols[p[2]].msb == symbol_table.symbols[p[2]].lsb:
                p[0] = f"{p[2]}Pin.setOutState({p[4]})"
            else:
                p[0] = f"{p[2]}Port.setOutState({p[4]})"
        else:  # wire <= statement
            p[0] = f"{p[2]} = {p[4]}"


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


# Error handling
def p_error(p):
    print("Syntax error in input!")


# Build the parser
parser = yacc.yacc()
