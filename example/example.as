IoPin@ aPin = component.getPin("a");
IoPin@ bPin = component.getPin("b");

// ___global_definitions___
double w = 0.0;

void setup()
{
	print("example setup()");
}

void reset()
{
	print("example reset()");

	aPin.setPinMode( 1 ); // Input
	bPin.setPinMode( 3 ); // Output

	aPin.changeCallBack( element, true );

	bPin.setVoltage( 0 );
}

void voltChanged()
{
	// ___implementation___
	w = (~a);
	bPin.setVoltage( w );
}
