import simulide 

component = simulide.Component('my_package', ['A', 'B'], ['C', 'D'])

component.create_package()
component.create_mcu()
component.create_script()