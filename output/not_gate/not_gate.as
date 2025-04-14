// This file was generated by veri2sim

IoPin@ aPin = component.getPin("a");
IoPin@ bPin = component.getPin("b");

// ___global_definitions___
bool w = false;

void setup()
{
	print("not_gate setup()");
}

void reset()
{
	print("not_gate reset()");

	aPin.setPinMode(1); // Input
	aPin.changeCallBack(element, true);
	bPin.setPinMode(3); // Output
	bPin.setOutState(false);
}

void voltChanged()
{
	// ___implementation___
	w = !aPin.getInpState();
	bPin.setOutState(w);
}
