import argparse
from lexer import lexer
from parser import parser
from simulide import Component


description = '''
veri2sim is a tool for converting Verilog files to SimulIDE component blocks.

Usage:
    veri2sim [input_file_name]

Examples:
    veri2sim and.v          Create a SimulIDE's component block for `and.v`, 
                            as this 3 files:
                                - and.package
                                - and.mcu
                                - and.as (AngelScript)
'''

# Set up argument parser
cli = argparse.ArgumentParser(description=description)
cli.add_argument('file', type=str, help='Path to the Verilog file')

# Parse arguments
args = cli.parse_args()

# Open the Verilog file
with open(args.file, 'r') as f:
        data = f.read()

# Parse the input file
result = parser.parse(data, lexer=lexer)

# Generate the custom output
if result:
        print(result)
else:
        print("Error analyzing the Verilog module.")

# Create the SimulIDE component
component = Component(result.name, 
                                            result.inputs,
                                            result.outputs,
                                            result.wires,
                                            result.statements)

# Generate the output files
component.create_package()
component.create_mcu()
component.create_script()
