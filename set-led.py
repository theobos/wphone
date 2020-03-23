#######################
#                     #
# Set the LED on/off. #
#                     #
#######################

import RPi.GPIO as GPIO
import sys

SCRIPT_ARGUMENT_NUMBER = 0
PIN_ARGUMENT_NUMBER    = 1
VALUE_ARGUMENT_NUMBER  = 2

def setPin(pin, on):
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(pin,  GPIO.OUT)
	GPIO.output(pin, GPIO.HIGH if on else GPIO.LOW)

def getScriptName():
	return str(sys.argv[SCRIPT_ARGUMENT_NUMBER])
		
def getPin():
	return int(sys.argv[PIN_ARGUMENT_NUMBER])
	
def getValue():
	value = str(sys.argv[VALUE_ARGUMENT_NUMBER]).lower()
	if value == "off":
		return 0
	if value == "on":
		return 1
	return int(value)

def validArguments():
	argCount =  len(sys.argv)
	if argCount != 3:
		printUsage()
		return False
	if argCount >= 2:
		try:
			getPin()
		except ValueError:
			print("The GPIO-pin-number must be an integer.")
			printUsage()
			return False
	if argCount >= 3:
		try:
			getValue()
		except ValueError:
			print("The value for the LED must be an integer.")
			printUsage()
			return False
	return True
	
def printUsage():
	print("Usage: %s nn v|on|On|off|Off " %(getScriptName()))
	print("       nn - the GPIO-pin-number as in GPIOnn using BCM")
	print("       v  - the value for on/off: 0 or 'Off' turns the LED off, any other integer value or 'On' turns the LED on")

def main():
	if validArguments():
		pin = getPin()
		value = getValue()
		print("GPIO%s will be used to turn the LED %s." %(pin, "off" if value == 0 else "on"))
		setPin(pin, value)

main()
