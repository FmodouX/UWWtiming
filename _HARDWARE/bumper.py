###UnitedWorldWrestling Bumper HAT for Raspberry   by FmodouX !###
###Copyright 2019 FmodouX, Frederic MODOUX, Switzerland###
###compatible with hardware rev 1.0###

import RPi.GPIO as GPIO
from datetime import datetime
from datetime import timedelta
from random import *
import socket
import time

inPinRed = 4
inPinBlue = 17
outPinRed = 27
outPinBlue = 22
outPinAct = 10

GPIO.setmode(GPIO.BCM)
GPIO.setup(inPinRed, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(inPinBlue, GPIO.IN)
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
		sock.sendto(msg, ("255.255.255.255", 5005))
		sock.sendto(msg, ("10.0.0.30", 5005))

	except:
		print("Exception while sending UDP packet : ", msg)


#Main runction
try:
	while True:

		#Random detection between RED and Blue
		n = randint(1,2)

		if n == 1:
			valueRed = GPIO.input(inPinRed)
			valueBlue = GPIO.input(inPinBlue)
		else:
			valueBlue = GPIO.input(inPinBlue)
			valueRed = GPIO.input(inPinRed)


		#RED bump
		if valueRed:
			if RedRelease:
				RedRelease = False

				GPIO.output(outPinRed, GPIO.HIGH)

				#print("RED Bump")

				udpMsg = "cr+1"
				udpMsg = udpMsg.encode('utf-8')

				UDPsendToAll(udpMsg)
				time.sleep(0.1)

		#RED release
		else:
			if not RedRelease:
				RedRelease = True
				GPIO.output(outPinRed, GPIO.LOW)

				print("Red Released")

				udpMsg = "cr-1"
                                udpMsg = udpMsg.encode('utf-8')

				UDPsendToAll(udpMsg)

				time.sleep(0.1)



		#BLUE bump
		if valueBlue:
			if BlueRelease:
				BlueRelease = False

				GPIO.output(outPinBlue, GPIO.HIGH)

				#print("Blue Bump")

				udpMsg = "cr+2"
				udpMsg = udpMsg.encode('utf-8')

				UDPsendToAll(udpMsg)
				time.sleep(0.1)
				

		#BLUE release
		else:
			if not BlueRelease:
				BlueRelease = True
				GPIO.output(outPinBlue, GPIO.LOW)

				print("Blue Released")

				udpMsg = "cr-2"
				udpMsg = udpMsg.encode('utf-8')

				UDPsendToAll(udpMsg)

				time.sleep(0.1)



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

				UDPsendToAll("ACT")




except:
	print("Exception in the code, exit program")



finally:
	GPIO.cleanup()
