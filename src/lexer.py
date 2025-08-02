import ply.lex as lex

# Reserved words list
reserved = {
    "module": "MODULE",
    "endmodule": "ENDMODULE",
    "input": "INPUT",
    "output": "OUTPUT",
    "wire": "WIRE",
    'reg': 'REG',
    'always': 'ALWAYS',
    # 'begin': 'BEGIN',
    # 'end': 'END',
    # 'if': 'IF',
    # 'else': 'ELSE',
    # 'case': 'CASE',
    # 'endcase': 'ENDCASE',
    # 'default': 'DEFAULT',
    "assign": "ASSIGN",
    # 'initial': 'INITIAL',
    # 'posedge': 'POSEDGE',
    # 'negedge': 'NEGEDGE',
    # 'for': 'FOR',
    # 'while': 'WHILE',
    # 'repeat': 'REPEAT',
    # 'forever': 'FOREVER',
    # 'function': 'FUNCTION',
    # 'endfunction': 'ENDFUNCTION',
    # 'task': 'TASK',
    # 'endtask': 'ENDTASK'
}

# Tokens list
tokens = [
    "IDENTIFIER",
    "NUMBER",
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "LPAREN",
    "RPAREN",
    'LBRACE',
    'RBRACE',
    "SEMI",
    "COMMA",
    "EQ",
    "EQEQ",
    "NEQ",
    "LT",
    "GT",
    "LE",
    "GE",
    "AND",
    "OR",
    "NOT",
    "BITAND",
    "BITOR",
    "BITXOR",
    "BITNOT",
    "LSHIFT",
    "RSHIFT",
    "COLON",
    "RSQUARE",
    "LSQUARE",
    "AT",         
    "BEGIN",      
    "END",        
] + list(reserved.values())

# Regular expression rules for simple tokens
t_PLUS = r"\+"
t_MINUS = r"-"
t_TIMES = r"\*"
t_DIVIDE = r"/"
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMI = r";"
t_COMMA = r","
t_EQ = r"="
t_EQEQ = r"=="
t_NEQ = r"!="
t_LT = r"<"
t_GT = r">"
t_LE = r"<="
t_GE = r">="
t_AND = r"&&"
t_OR = r"\|\|"
t_NOT = r"!"
t_BITAND = r"&"
t_BITOR = r"\|"
t_BITXOR = r"\^"
t_BITNOT = r"~"
t_LSHIFT = r"<<"
t_RSHIFT = r">>"
t_COLON = r":"
t_RSQUARE = r"\]"
t_LSQUARE = r"\["
t_AT = r"@"
t_BEGIN = r"begin"
t_END = r"end"


# Rule to ignore Verilog comments
def t_COMMENT(t):
    r"//.*|/\*[\s\S]*?\*/"
    pass


# Rule for numbers
def t_NUMBER(t):
    r"\d+"
    t.value = int(t.value)
    return t


# Rule for identifiers and reserved words
def t_IDENTIFIER(t):
    r"[a-zA-Z_][a-zA-Z_0-9]*"
    t.type = reserved.get(t.value, "IDENTIFIER")
    return t


# Rule to ignore whitespace, tabs and newlines
t_ignore = " \t\n"


# Error handling
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()
