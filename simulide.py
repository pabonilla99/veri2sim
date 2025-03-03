from lxml import etree as ET
import os


class Component():
    def __init__(self, name, symbols, statements):        
        self.name = name
        self.symbols = symbols
        self.statements = statements
        os.makedirs(f'./output/{name}', exist_ok=True)

    def single_inputs(self):
        counter = 0
        for symbol in self.symbols:
            msb   = self.symbols[symbol].msb 
            lsb   = self.symbols[symbol].lsb 
            if self.symbols[symbol].type == 'input':
                if msb == lsb:                  # single input
                    counter += 1
                else:
                    counter += (msb - lsb) + 1  # input array
        return counter

    def single_outputs(self):
        counter = 0
        for symbol in self.symbols:
            msb   = self.symbols[symbol].msb 
            lsb   = self.symbols[symbol].lsb 
            if type == 'output':
                if msb == lsb:                  # single output
                    counter += 1
                else:
                    counter += (msb - lsb) + 1  # output array
        return counter

    def create_package(self):
        # root element
        packageB = ET.Element("packageB", 
                              name="Package", 
                              width="8", 
                              height=f"{max(self.single_inputs(), self.single_outputs()) + 1}", 
                              background="", 
                              type="None")

        i = 0
        for symbol in self.symbols:
            msb   = self.symbols[symbol].msb 
            lsb   = self.symbols[symbol].lsb 
            if self.symbols[symbol].type == 'input':
                if msb == lsb:        # single input
                    pin = ET.SubElement(packageB, "pin", 
                                        type="",
                                        xpos="-8",
                                        ypos=f"{8+(i*8)}",
                                        angle="180",
                                        length="8",  
                                        space="0",   
                                        id=f"{symbol}",     
                                        label=f"{symbol}")
                    i += 1
                else:                               # input array
                    for j in range(lsb, msb+1):
                        pin = ET.SubElement(packageB, "pin", 
                                            type="",
                                            xpos="-8",
                                            ypos=f"{8+(i*8)}",
                                            angle="180",
                                            length="8",  
                                            space="0",   
                                            id=f"{symbol}_{j}",     
                                            label=f"{symbol}_{j}")
                        i += 1

        # for index, value in enumerate(self.inputs):     # inputs
        #     pin = ET.SubElement(packageB, "pin", 
        #                         type="",
        #                         xpos="-8",
        #                         ypos=f"{8+(index*8)}",
        #                         angle="180",
        #                         length="8",  
        #                         space="0",   
        #                         id=f"{value}",     
        #                         label=f"{value}")

        i = 0
        for symbol in self.symbols:
            msb   = self.symbols[symbol].msb 
            lsb   = self.symbols[symbol].lsb 
            if self.symbols[symbol].type == 'output':
                if msb == lsb:        # single output            
                    pin = ET.SubElement(packageB, "pin", 
                                        type="",
                                        xpos="72",
                                        ypos=f"{8+(i*8)}",
                                        angle="0",
                                        length="8",  
                                        space="0",   
                                        id=f"{symbol}",     
                                        label=f"{symbol}")
                    i += 1
                else:                               # output array
                    for j in range(lsb, msb+1):
                        pin = ET.SubElement(packageB, "pin", 
                                            type="",
                                            xpos="72",
                                            ypos=f"{8+(i*8)}",
                                            angle="0",
                                            length="8",  
                                            space="0",   
                                            id=f"{symbol}_{j}",     
                                            label=f"{symbol}_{j}")
                        i += 1

        # for index, value in enumerate(self.outputs):     # outputs
        #     pin = ET.SubElement(packageB, "pin", 
        #                         type="",
        #                         xpos="72",
        #                         ypos=f"{8+(index*8)}",
        #                         angle="0",
        #                         length="8",  
        #                         space="0",   
        #                         id=f"{value}",     
        #                         label=f"{value}")


        # elements tree
        tree = ET.ElementTree(packageB)

        # file's header and content
        with open(f"./output/{self.name}/{self.name}.package", "wb") as f:
            f.write(b'<!DOCTYPE SimulIDE>\n\n')
            f.write(b'<!-- This file was generated by veri2sim -->\n\n')
            tree.write(f, encoding="utf-8", xml_declaration=False, pretty_print=True)

    def create_mcu(self):
        # root element
        iou = ET.Element("iou", 
                         name=f"{self.name}", 
                         core="scripted", 
                         script=f"{self.name}.as")

        # # inputs
        # ioport = ET.SubElement(iou, "ioport", 
        #                        name="InputPort", 
        #                        pins=",".join(self.inputs))
        
        # # outputs
        # ioport = ET.SubElement(iou, "ioport", 
        #                        name="OutputPort", 
        #                        pins=",".join(self.outputs))
        
        # element tree
        tree = ET.ElementTree(iou)

        # file's header and content
        with open(f"./output/{self.name}/{self.name}.mcu", "wb") as f:
            f.write(b'<!DOCTYPE SimulIDE>\n\n')
            f.write(b'<!-- This file was generated by veri2sim -->\n\n')
            tree.write(f, encoding="utf-8", xml_declaration=False, pretty_print=True)

    def create_script(self):
        with open(f"./output/{self.name}/{self.name}.as", "w") as f:
            f.write('// This file was generated by veri2sim\n\n')

            # # inputs and outputs
            # for input in self.inputs:
            #     f.write(f'IoPin@ {input}Pin = component.getPin("{input}");\n')
            # for output in self.outputs:
            #     f.write(f'IoPin@ {output}Pin = component.getPin("{output}");\n')

            # # global variables and functions
            # f.write('\n// ___global_definitions___')
            # for wire in self.wires:
            #     f.write(f'\nuint8 {wire} = 0;')

            # # setup function
            # f.write(f'\n\nvoid setup()\n{{\n\tprint("{self.name} setup()");\n}}')
            
            # # reset function
            # f.write(f'\n\nvoid reset()\n{{\n\tprint("{self.name} reset()");\n\n')
            # for input in self.inputs:
            #     f.write(f'\t{input}Pin.setPinMode(1); // Input\n')
            # for output in self.outputs:
            #     f.write(f'\t{output}Pin.setPinMode(3); // Output\n')
            # f.write('\n')    
            # for input in self.inputs:
            #     f.write(f'\t{input}Pin.changeCallBack(element, true);\n')
            # f.write('\n')
            # for output in self.outputs:
            #     f.write(f'\t{output}Pin.setOutState(false);\n')
            # f.write('}\n')

            # # voltChanged function
            # f.write('\nvoid voltChanged()\n{\n\t// ___implementation___\n')
            # for statement in self.statements:
            #     f.write(f'\t{statement};\n')     
            # f.write('}\n')
