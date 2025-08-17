import ply.yacc as yacc
from src.lexer import tokens


# Class to store Verilog module information
class VerilogModule:
    def __init__(self, name):
        self.name = name
        self.statements = []
        self.symbols = symbol_table.symbols

    def __str__(self):
        out = f"Module:\n\t{self.name}\n\n"
        print(f"Module: {self.statements}")
        out += "Statements:\n\t" + ''.join(self.statements).replace('\n', '\n\t') + "\n\n"
        out += "Symbols:\n\t" + '\n\t'.join([f'{value}' for _, value in self.symbols.items()])
        return out


# Class for a symbol in the symbol table
class Symbol:
    def __init__(self, name, sym_type, value1=None, value2=None, value3=None):
        self.name = name
        self.type = sym_type
        self.value1 = value1
        self.value2 = value2
        self.value3 = value3

    def __str__(self):
        return f"Symbol(name={self.name}, type={self.type}, value1={self.value1}, value2={self.value2}, value3={self.value3})"


# Class for the symbol table
class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def add_symbol(self, name, sym_type, value1=None, value2=None, value3=None):
        if name not in self.symbols:
            self.symbols[name] = Symbol(name, sym_type, value1, value2, value3)
        else:
            print(f"Warning: Symbol {name} already exists in the symbol table.")

    def modify_symbol(self, name, sym_type=None, value1=None, value2=None, value3=None):
        if name in self.symbols:
            if sym_type is not None:
                self.symbols[name].type = sym_type
            if value1 is not None:
                self.symbols[name].value1 = value1
            if value2 is not None:
                self.symbols[name].value2 = value2
            if value3 is not None:
                self.symbols[name].value3 = value3
        else:
            print(f"Error: Symbol {name} does not exist in the symbol table.")

    def __str__(self):
        return "\n".join(str(symbol) for symbol in self.symbols.values())


# Create an instance of the symbol table
symbol_table = SymbolTable()

# initial_commands = ''


# Grammar definition
def p_module(p):
    """module : MODULE IDENTIFIER parameter_port_list LPAREN port_list RPAREN SEMI module_items ENDMODULE
              | MODULE IDENTIFIER LPAREN port_list RPAREN SEMI module_items ENDMODULE"""
    if len(p) == 9:
        p[0] = VerilogModule(p[2])
        p[0].statements = p[7]["statements"]
    else:
        p[0] = VerilogModule(p[2])
        p[0].statements = p[8]["statements"]

    # Add the module to the symbol table
    symbol_table.add_symbol(p[2], "module")
    # print(symbol_table)
    # print("module:\t", p[2])


def p_port_list(p):
    """port_list    : port
                    | port_list COMMA port"""
    if len(p) == 2:
        p[0] = p[1]
        # print("port_list:\t", p[1]) 
    else:
        p[0] = f"{p[1], p[3]}"
        # print("port_list:\t", f"{p[1], p[3]}") 
    


def p_port(p):
    """port     : range IDENTIFIER
                | INPUT range IDENTIFIER
                | OUTPUT range IDENTIFIER
                | INPUT WIRE range IDENTIFIER
                | OUTPUT REG range IDENTIFIER"""
    # print("port:\t", p[1:])
    if len(p) == 5:  # WIRE or REG defined
        port_type = p[1]
        range = p[3]
        identifier = p[4]
    elif len(p) == 4:  # INPUT or OUTPUT defined
        port_type = p[1]
        range = p[2]
        identifier = p[3]
    else:           # No INPUT or OUTPUT defined
        port_type = "unspecified"
        range = p[1]
        identifier = p[2]

    if range:
        p[0] = f"{port_type}, {identifier}"  # when bit array
        msb, lsb = range
    else:
        p[0] = f"{port_type}, {identifier}"  # when single bit
        msb, lsb = 0, 0

    # Add the port to the symbol table
    symbol_table.add_symbol(identifier, port_type, msb, lsb)
    # print("port:\t", identifier) 


def p_range(p):
    """range    : LSQUARE expression COLON expression RSQUARE
                | empty"""
    print(f"range:\t {p[2]} {p[4]}")
    if len(p) == 6:
        p[0] = [eval(str(p[2])), eval(str(p[4]))]
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
    """module_item  : wire_declaration
                    | identifier_definition
                    | assign_block
                    | always_block
                    | localparam_declaration"""
    p[0] = p[1]


def p_identifier_definition(p):
    """identifier_definition    : INPUT identifier_list SEMI
                                | OUTPUT identifier_list SEMI
                                | REG identifier_list SEMI"""
    port_type = p[1]
    identifiers = p[2]
    for identifier in identifiers:
        symbol_table.modify_symbol(identifier, port_type, 0, 0)


def p_identifier_list(p):
    """identifier_list  : IDENTIFIER
                        | identifier_list COMMA IDENTIFIER"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_wire_declaration(p):
    """wire_declaration : WIRE range IDENTIFIER SEMI"""
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


def p_assignment_concat(p):
    """assignment   : LBRACE concat_list RBRACE EQ expression
                    | LBRACE concat_list RBRACE LE expression"""
    bit_index = 0
    n_bits = 1
    p[0] = "\n"
    print(f"expression_concat: {p[2]} : {type(p[2])}")
    for identifier in list(reversed(p[2])):
        if identifier in symbol_table.symbols:  # identifier in symbol table
            msb = symbol_table.symbols[identifier].value1
            lsb = symbol_table.symbols[identifier].value2
            n_bits = msb - lsb + 1
            if symbol_table.symbols[identifier].type == "output":
                if msb == lsb:  # single bit input
                    var = f"{identifier}Pin.setOutState"
                else:           # multi-bit input
                    var = f"{identifier}Port.setOutState"
            else:
                var = f"{identifier}"
        else:                               # identifier not in symbol table
            print(f"Warning: Identifier {identifier} not found in symbol table.")

        mask = '0b' + '0'*(64 - n_bits) + '1'*n_bits
        if "setOutState" in var:  # if it's an output
            p[0] += f"{var}(({p[5]} & {hex(int(mask, 2))})"
            p[0] += f" >> {bit_index});\n" if bit_index != 0 else f");\n"
        else: # if it's a wire
            p[0] += f"{var} = ({p[5]} & {hex(int(mask, 2))})"
            p[0] += f" >> {bit_index};\n" if bit_index != 0 else f";\n"
        bit_index += n_bits
    p[0] = p[0][:-2]

def p_assignment(p):
    """assignment   : IDENTIFIER EQ expression
                    | IDENTIFIER LE expression"""
    # print(f"assignment: {p[1]} = {p[3]}")
    if p[1] in symbol_table.symbols:
        if symbol_table.symbols[p[1]].type == "output":  # output <= statement
            if symbol_table.symbols[p[1]].value1 == symbol_table.symbols[p[1]].value2:
                p[0] = f"{p[1]}Pin.setOutState({p[3]})"
            else:
                p[0] = f"{p[1]}Port.setOutState({p[3]})"
        else:  # wire <= statement
            p[0] = f"{p[1]} = {p[3]}"

def p_expression_binop(p):
    """expression   : expression PLUS expression
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
    print(f"expression_binop: {p[1]} {p[2]} {p[3]}")
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
    ("right", "NOT", "BITNOT", "POSEDGE", "NEGEDGE" ),
)


def p_expression_unop(p):
    """expression   : MINUS expression %prec NOT
                    | NOT expression
                    | BITNOT expression"""
    exp = p[2].replace("Pin.getInpState()", "")
    if exp in symbol_table.symbols:
        if (
            symbol_table.symbols[exp].value1 == symbol_table.symbols[exp].value2
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
    p[0] = convert_to_number(p[1])


def p_expression_identifier(p):
    """expression : IDENTIFIER"""
    print(f"expression_identifier: {p[1]}")
    if p[1] in symbol_table.symbols:
        if symbol_table.symbols[p[1]].type == "input":
            if symbol_table.symbols[p[1]].value1 == symbol_table.symbols[p[1]].value2:
                p[0] = f"{p[1]}Pin.getInpState()"
            else:
                p[0] = f"{p[1]}Port.getInpState()"
        else:
            p[0] = p[1]


def p_always_block(p):
    """always_block : ALWAYS AT sensitivity_list statement"""
    edged_vars = []
    # print(f"always_block: {p[3]}")
    for identifier in p[3]:
        if identifier == "*":
            break
        try:
            # print(f"always_block: id={identifier}")
            if symbol_table.symbols[identifier].value3 != None: # detect the edge type
                edged_vars.append({'name': identifier, 'edge': symbol_table.symbols[identifier].value3})
        except KeyError:
            print(f"Warning: Identifier {identifier} not found in symbol table.")
    p[0] = f'// --- always ---\n// @('
    if len(edged_vars) == 0:            # combinational always block
        p[0] += ",".join(p[3]) + ')\n'
        for stmt in p[4]:
            p[0] += f"{stmt};\n"
    else:                               # sequential always block       
        for var in edged_vars:
            p[0] += f"{var['edge']} {var['name']} ,"
        p[0] = p[0][:-2] + ')\nif ('
        for var in edged_vars:
            p[0] += f"{var['name']}.getInpState() == "
            p[0] += f"1 || " if var['edge'] == "posedge" else f"0 || "
        p[0] = p[0][:-4] + ") {\n"    
        for stmt in p[4]:
            p[0] += f"{stmt};\n"
        p[0] += '}\n'
    p[0] += '// --------------'

def p_sensitivity_list(p):
    """sensitivity_list : LPAREN sensitivity_items RPAREN
                        | LPAREN TIMES RPAREN"""
    p[0] = p[2] # "".join(f"{id}, " for id in p[2])[:-2]

def p_sensitivity_items(p):
    """sensitivity_items    : TIMES
                            | IDENTIFIER
                            | NEGEDGE IDENTIFIER
                            | POSEDGE IDENTIFIER
                            | sensitivity_items OR_KW IDENTIFIER
                            | sensitivity_items COMMA IDENTIFIER"""
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:    
        symbol_table.modify_symbol(p[2], sym_type=None, value1=None, value2=None, value3=p[1])
        p[0] = [p[2]]
    else:
        p[0] = p[1] + [p[3]]

def p_statement_block(p):
    """statement_block : BEGIN statement_list END"""
    # print("statement_block:\t", p[2])
    p[0] = p[2]

def p_statement_list(p):
    """statement_list   : statement
                        | statement_list statement"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement(p):
    """statement    : assignment SEMI
                    | if_block
                    | case_block
                    | statement_block"""
    
                    # | reg_assignment SEMI
    p[0] = p[1]

def p_if_block(p):
    """if_block : IF LPAREN expression RPAREN statement else_block_opt"""
    if isinstance(p[5], list):
        body = "{\n" + "".join(f"{stmt};\n" for stmt in p[5]) + "}"
    else:
        body = f"{p[5]}"
    p[0] = f"if ({p[3]}) {body};\n{p[6]}"

def p_else_block_opt(p):
    """else_block_opt   : ELSE statement
                        | empty"""
    if len(p) == 3:
        if isinstance(p[2], list):
            body = "{\n" + "".join(f"{stmt};\n" for stmt in p[2]) + "}"
        else:
            body = f"{p[2]}"
        p[0] = f"else {body}"
    else:
        p[0] = ""

def p_case_block(p):
    """case_block : CASE LPAREN expression RPAREN case_item_list ENDCASE"""
    body = "".join(p[5])
    p[0] = f"switch ({p[3]}) {{\n{body}}}"

def p_case_item_list(p):
    """case_item_list : case_item
                      | case_item_list case_item"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_case_item(p):
    """case_item : number_or_id COLON statement
                 | DEFAULT COLON statement"""
    statements = ';\n\t'.join(p[3]) if isinstance(p[3], list) else p[3]
    if p[1] == 'default':
        p[0] = f"default:\n\t{statements}"   
    else:
        p[0] = f"case {p[1]}:\n\t{statements}" 
    p[0] += ";\n\tbreak;\n"

def p_number_or_id(p):
    """number_or_id : NUMBER
                    | IDENTIFIER"""
    p[0] = p[1]

def p_expression_concat(p):
    """expression : LBRACE concat_list RBRACE"""
    bit_index = 0
    p[0] = "\n"
    print(f"expression_concat: {p[2]} : {type(p[2])}")
    for identifier in list(reversed(p[2])):
        if identifier in symbol_table.symbols:  # identifier in symbol table
            msb = symbol_table.symbols[identifier].value1
            lsb = symbol_table.symbols[identifier].value2
            n_bits = msb - lsb + 1
            if symbol_table.symbols[identifier].type == "input":
                if msb == lsb:  # single bit input
                    var = f"{identifier}Pin.getInpState()"
                else:           # multi-bit input
                    var = f"{identifier}Port.getInpState()"
            else:
                var = f"{identifier}"
        elif "'" in identifier:             # number with base and bits
            nb, _ = identifier.split("'")    
            n_bits = int(nb)
            var = f"{convert_to_number(identifier)}"
        else:                               # identifier not in symbol table
            print(f"Warning: Identifier {identifier} not found in symbol table, or number without base.")
        mask = '0b' + '0'*(64 - n_bits) + '1'*n_bits
        p[0] += f"\t({var} & {hex(int(mask, 2))}) "
        p[0] += f"<< {bit_index} |\n" if bit_index != 0 else f"|\n"
        bit_index += n_bits
    p[0] = p[0][:-3] + "\n"

def p_concat_list(p):
    """concat_list  : number_or_id
                    | concat_list COMMA number_or_id"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_localparam_declaration(p):
    """localparam_declaration   : PARAMETER IDENTIFIER EQ expression SEMI
                                | LOCALPARAM IDENTIFIER EQ expression SEMI"""
    # print(f"localparam_declaration: {p[2]} = {p[4]}")
    param_type = detect_number_type(p[4])
    symbol_table.add_symbol(p[2], 'parameter', p[4], param_type)
    globals()[p[2]] = eval(str(p[4]))   # set the parameter as a global variable in Python
    p[0] = ''
    
def p_parameter_port_list(p):
    """parameter_port_list : POUND LPAREN parameter_port_items RPAREN"""
    # Puedes guardar los parámetros aquí si lo deseas
    p[0] = p[3]

def p_parameter_port_items(p):
    """parameter_port_items : parameter_port_item
                            | parameter_port_items COMMA parameter_port_item"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_parameter_port_item(p):
    """parameter_port_item : PARAMETER IDENTIFIER EQ expression"""
    param_type = detect_number_type(p[4])
    symbol_table.add_symbol(p[2], 'parameter', p[4], param_type)
    globals()[p[2]] = eval(str(p[4]))   # set the parameter as a global variable in Python
    p[0] = ''


# Error handling
def p_error(p):
    print("Syntax error in input!")


def convert_to_number(value):
    if "'" in value:
        width, base_and_digits = value.split("'")
        base = base_and_digits[0].lower()
        digits = base_and_digits[1:]
        if base == 'b':
            num = int(digits.replace('_', ''), 2)
        elif base == 'o':
            num = int(digits.replace('_', ''), 8)
        elif base == 'd':
            num = int(digits.replace('_', ''), 10)
        elif base == 'h':
            num = int(digits.replace('_', ''), 16)
        else:
            num = int(digits.replace('_', ''), 10)
    else:
        num = int(value)
    
    return num

def detect_number_type(input_string):
    try:
        _ = int(input_string)
        return "Integer"
    except ValueError:
        try:
            _ = float(input_string)
            return "Float"
        except ValueError:
            return "Not a number"

# Build the parser
parser = yacc.yacc()