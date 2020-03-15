###########################################################################################################
#                                                                                                         #
# This program is the python version of the t65 program (created in the Go-language) for the Wonderfoon.  #
# Information about the wonderful Wonderfoon can be found at www.wonderfoon.nl                            #
#                                                                                                         #
# This program works with all t65 models that have exactly one red, one blue and one yellow wire          #
# attached to the rotator or keyboard.                                                                    #
#                                                                                                         #                                
###########################################################################################################

import RPi.GPIO as GPIO
import json
import subprocess
import time

from os import listdir, system
from os.path import abspath, isfile, join

wphoneConfig = None

def getConfigurationItem(key, default):
	global wphoneConfig
	if(wphoneConfig is None):
		with open('wphone.config', 'r') as config:
			wphoneConfig = json.load(config)
	return wphoneConfig.get(key, default)

MUSIC_DIR        = getConfigurationItem("music-dir", "music")
POLLING_INTERVAL = getConfigurationItem("polling-interval", 0.01) # Polling interval in seconds
MAX_WAIT         = getConfigurationItem("max-wait", 3) # Maximum time in seconds needed to produce the '0' with the rotator
OFF_HOOK         = getConfigurationItem("off-hook", 16)
RED              = getConfigurationItem("red", 19)
BLUE             = getConfigurationItem("blue", 26)
MUSIC_PLAYER     = getConfigurationItem("music-player", "mplayer")

def setupGPIO():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(RED,      GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(BLUE,     GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(OFF_HOOK, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def playNewSong(digit):
	currentMusicThread = None
	dir = MUSIC_DIR
	files = [f for f in listdir(dir) if isfile(join(dir, f))]
	files.sort()
	if (digit >= 0 and digit < len(files)):
		currentMusicThread = subprocess.Popen([MUSIC_PLAYER, join(dir, files[digit])])
	return currentMusicThread

def stopCurrentSong(currentMusicThread):
	if (not (currentMusicThread is None)):
		currentMusicThread.kill()

def polling():
	currentMusicThread = None
	while True:
		digit     = -1
		dialling  =  False
		startTime =  None
		while True:
			time.sleep(POLLING_INTERVAL)
			RedIn     = GPIO.input(RED)
			BlueIn    = GPIO.input(BLUE)
			OffHookIn = GPIO.input(OFF_HOOK)
			if(OffHookIn == 0):
				stopCurrentSong(currentMusicThread)
				currentMusicThread = None
			if (RedIn == 1 and BlueIn == 0):
				dialling = True
				if (startTime is None):
					startTime = time.time() # Start waiting for MAX_WAIT when dialling started.
			else:
				if dialling:
					digit += 1
				dialling = False
			if ( digit > -1 and (time.time() - startTime) > MAX_WAIT):
				print("Dialled: " + str((digit + 1) % 10))  # Mapping of the rotator-digits to digit: 1-9 => 0-8, 0 => 9
				stopCurrentSong(currentMusicThread)
				currentMusicThread = playNewSong(digit)
				break
			
def printConfiguration():
	print("Configuration:")
	print("  Music Directory . . . . . . . : %s"         %(MUSIC_DIR))
	print("  Music Player  . . . . . . . . : %s"         %(MUSIC_PLAYER))
	print("  Maximum time to produce '0' . : %d seconds" %(MAX_WAIT))
	print("  Polling interval  . . . . . . : %f seconds" %(POLLING_INTERVAL))
	print("  Red wire is connected to  . . : GPIO%d"     %(RED))
	print("  Blue wire is connected to . . : GPIO%d"     %(BLUE))
	print("  Off Hook is connected to  . . : GPIO%d"     %(OFF_HOOK))
	print("Dial a number...")
	
def main():
	printConfiguration()
	setupGPIO()
	polling()

main()