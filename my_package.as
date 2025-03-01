IoPin@ APin = component.getPin("A");
IoPin@ BPin = component.getPin("B");
IoPin@ CPin = component.getPin("C");
IoPin@ DPin = component.getPin("D");

void block_implementation(void);

void setup()
{
	print("my_package setup()");
}

void reset()
{
	print("my_package reset()");

	APin.setPinMode( 1 ); // Input
	BPin.setPinMode( 1 ); // Input
	CPin.setPinMode( 3 ); // Output
	DPin.setPinMode( 3 ); // Output

	APin.changeCallBack( element, true );
	BPin.changeCallBack( element, true );

	CPin.setVoltage( 0 )
	DPin.setVoltage( 0 )
}


void voltChanged()
{
	block_implementation();
}

