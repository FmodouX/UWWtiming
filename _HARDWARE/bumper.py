###UnitedWorldWrestling Bumper HAT for Raspberry   by FmodouX !###
###Copyright 2019-2024 FmodouX, Frederic MODOUX, Switzerland###
###compatible with hardware rev 2.x###

import RPi.GPIO as GPIO
from datetime import datetime
from datetime import timedelta
from random import *
import socket
import time

inPinRed = 5
inPinBlue = 6
outPinRed = 19
outPinBlue = 26
outPinAct = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(inPinRed, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(inPinBlue, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(outPinRed, GPIO.OUT)
GPIO.setup(outPinBlue, GPIO.OUT)
GPIO.setup(outPinAct, GPIO.OUT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

RedSend = True
BlueSend = True
ActDate = datetime.now()
RedRelease = False
BlueRelease = False
ActSend = False


#UDP send function
def UDPsendToAll(msg):
	try:
		sock.sendto(msg, ("255.255.255.255", 5005)) # Broadcast channel
		sock.sendto(msg, ("10.0.0.30", 33000)) # Mat Scoring PC

	except:
		print("Exception while sending UDP packet : ", msg)


#MAIN FUNCTION
try:
	while True:

		#Random reading detection between RED and BLUE
		n = randint(1,2)

		if n == 1: # RED first after random
			valueRed = GPIO.input(inPinRed)
			valueBlue = GPIO.input(inPinBlue)
		else: # BLUE first after random
			valueBlue = GPIO.input(inPinBlue)
			valueRed = GPIO.input(inPinRed)


		#RED bump
		if valueRed:
			if RedRelease:
				RedRelease = False

				GPIO.output(outPinRed, GPIO.HIGH)

				print("RED Bumped")

				udpMsg = "cr+1"
				udpMsg = udpMsg.encode('utf-8')

				UDPsendToAll(udpMsg)
#				time.sleep(0.1)

		#RED release
		else:
			if not RedRelease:
				RedRelease = True
				GPIO.output(outPinRed, GPIO.LOW)

				print("RED Released")

				udpMsg = "cr-1"
				udpMsg = udpMsg.encode('utf-8')

				UDPsendToAll(udpMsg)

#				time.sleep(0.1)



		#BLUE bump
		if valueBlue:
			if BlueRelease:
				BlueRelease = False

				GPIO.output(outPinBlue, GPIO.HIGH)

				print("BLUE Bumped")

				udpMsg = "cr+2"
				udpMsg = udpMsg.encode('utf-8')

				UDPsendToAll(udpMsg)
#				time.sleep(0.1)


		#BLUE release
		else:
			if not BlueRelease:
				BlueRelease = True
				GPIO.output(outPinBlue, GPIO.LOW)

				print("BLUE Released")

				udpMsg = "cr-2"
				udpMsg = udpMsg.encode('utf-8')

				UDPsendToAll(udpMsg)

#				time.sleep(0.1)



		#ACTivity heartbeat
		delt = datetime.now() - ActDate

		if delt.microseconds > 500000:
			ActDate = datetime.now()
			if ActSend:
				ActSend = False
				GPIO.output(outPinAct, GPIO.LOW)
			else:
				ActSend = True
				GPIO.output(outPinAct, GPIO.HIGH)

				udpMsg = "ACT"
				udpMsg = udpMsg.encode('utf-8')
				UDPsendToAll(udpMsg)


		time.sleep(0.01)

except:
	print("Exception in the code, exit program")



finally:
	GPIO.cleanup()
