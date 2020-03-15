####################
#                  #
# Turn the LED on. #
#                  #
####################

import RPi.GPIO as GPIO
import json
import sys

CONFIG_FILE = "wphone.config"

def getConfigurationItem(key, default):
	with open(CONFIG_FILE, 'r') as config:
		wphoneConfig = json.load(config)
	return wphoneConfig.get(key, default)

def turnPinOn(pin):
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(pin,  GPIO.OUT)
	GPIO.output(pin, GPIO.HIGH)

def main():
	pin = getConfigurationItem("led", -1)
	if(pin == -1):
		print("Item 'led' not configured in %s" %(CONFIG_FILE))
		return
	print("GPIO-pin %d will be used to turn the LED on." %(pin))
	turnPinOn(pin)
		
main()
