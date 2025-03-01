from lexer import lexer
from parser import parser

# Ejemplo de entrada de Verilog
data = '''
module example (input a, output b);
    wire w;
    assign w = a;
    assign b = w;
endmodule
'''

# Analizar la entrada
result = parser.parse(data, lexer=lexer)
print(result)