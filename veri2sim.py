import argparse
from src.lexer import lexer
from src.parser import parser
from src.simulide import Component
import os
import shutil

description = '''
veri2sim is a tool for converting Verilog files to SimulIDE component blocks.\n
Create a SimulIDE's component block for `file.v` as these 3 files:
`file.package`, `file.mcu` and `file.as` (AngelScript).
'''


# Set up argument parser
cli = argparse.ArgumentParser(description=description)
cli.add_argument('-c', '--compile', dest='command', action='store_const', const='compile', help='Compile the Verilog file')
cli.add_argument('-cl', '--clean', dest='command', action='store_const', const='clean', help='Clean the output directory')
cli.add_argument('file', type=str, nargs='?', help='Path to the Verilog file (required for the compile command)')

# Parse arguments
args = cli.parse_args()

# Handle the 'clean' command
if args.command == 'clean':
    if os.path.exists('output'):
        shutil.rmtree('output')
        print("Output directory cleaned.")
    else:
        print("No output directory to clean.")
    exit(0)

# Handle the 'compile' command
if args.command == 'compile':
    if not args.file:
        print("Error: The 'compile' command requires a Verilog file path.")
        exit(1)

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
        exit(1)

    # Create the SimulIDE component
    component = Component(result.name,
                          result.symbols,
                          result.statements)

    # Generate the output files
    component.create_package()
    component.create_mcu()
    component.create_script()
    print("\nCompilation completed.")
