from lexer import lexer
from parser import parser
from simulide import Component


# Basic Verilog file
with open('not.v', 'r') as f:
    data = f.read()

# parse the input
result = parser.parse(data, lexer=lexer)

# create the SimulIDE component
component = Component(result.name, 
                      result.inputs,
                      result.outputs,
                      result.wires,
                      result.statements)
component.create_package()
component.create_mcu()
component.create_script()

# Generar la salida personalizada
if result:
    print(result)
else:
    print("Error al analizar el módulo Verilog.")