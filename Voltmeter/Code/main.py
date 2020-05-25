#Originele code - Wilfer Spaepen

#importeren van alle modules
import RPi.GPIO as GPIO
import time
from mfrc522 import SimpleMFRC522

#aanmaken van een lezer-object
reader = SimpleMFRC522()

#------------------
# globale variabelen
#------------------

#pins om de schakelaars in te lezen
pins = [8, 10, 11, 12]
#pins om de stappenmotor aan te sturen
mpins = [29, 31, 33, 35]
#de waarde die elke schakelaar voorstelt
values = [4, 1, 8, 2]
#Het minimale percentage
#om de servo aan te sturen
minper = 1.5
#Het maximale percentage
maxper = 9
#Bufferwaarde
voltprev = 0
#Het getal waarbij de puzzel opgelost is
winval = 13

#stappen per °
#180° = 1050 stappen
# -> 5.833 / graad
stepdeg = 11.6

#De mfrc522 module maakt gebruik van GPIO.BOARD
#omdat twee verschillende modi onmogelijk zijn
#gebruiken we deze ook
GPIO.setmode(GPIO.BOARD)
#Zet de servo-controle pin ip OUT
GPIO.setup(32, GPIO.OUT)

#initializeer de andere pins
for a in range(4):
	GPIO.setup(pins[a], GPIO.IN)
	GPIO.setup(mpins[a], GPIO.OUT)

#maak een PWM-object aan
indicator = GPIO.PWM(32, 50)
#start de PWM
indicator.start(0)

#functie om de positie van de
#servomotor aan te passen
def setPos(posDeg):
	percent = (posDeg/180)*(maxper - minper) + minper
	indicator.ChangeDutyCycle(percent)

#functie om de waarden van de
#schakelaars te krijgen
def getInput():
	databuf = []
	for a in range(4):
		databuf.append(GPIO.input(pins[a]))
	return databuf

#functie om cw (dicht) te draaien
def turncw(index: int) -> int:
	#print("[debug] turncw index:", index)
	if(index == 0):
		GPIO.output(mpins[2], 0)
	elif(index == 1):
		GPIO.output(mpins[3], 0)
	else:
		GPIO.output(mpins[index - 2], 0)
	GPIO.output(mpins[index], 1)
	index += 1
	if index > 3:
		index = 0
	return index

#functie om cc (open) te draaien
def turncc(index: int) -> int:
	#print("[debug] turncc index:", index)
	if(index == 3):
		GPIO.output(mpins[1], 0)
	elif(index == 2):
		GPIO.output(mpins[0], 0)
	else:
		GPIO.output(mpins[index + 2], 0)
	GPIO.output(mpins[index], 1)
	index -= 1
	if index < 0:
		index = 3
	return index

#functie om de stappenmotor een
#bepaald aantal graden te draaien
def moveDeg(index : int, deg : int, dir : bool) -> int:
	for a in range(round(stepdeg*deg)):
		if(dir):
			index = turncc(index)
		else:
			index = turncw(index)
		time.sleep(0.004)
	return index

ind = 0

try:
	while True:
		#sluit de doos
		ind = moveDeg(ind, 120, False)
		#beweeg de indicator
		setPos(180)
		#wacht even
		time.sleep(0.5)
		#beweeg opnieuw
		setPos(0)
		#wacht even
		time.sleep(0.5)
		#stop de servo
		indicator.ChangeDutyCycle(0)
		#lees de waarde van de kaart in
		id, text = reader.read()
		#kijk na of de data overeenkomt
		if(text.rstrip(' ') == "puz2"):
			print("[debug] text ok")
			#beweeg de servo 2 keer
			setPos(0)
			time.sleep(1)
			setPos(180)
			time.sleep(1)
			indicator.ChangeDutyCycle(0)
		#blijf herhalen
		while True:
			volt = 0
			#vraag de data op
			swdata = getInput()
			#update de waarde van de meter
			#gebaseerd op de schakelaars
			for a in range(4):
				if(not swdata[a]):
					volt += values[a]
			volt = 15 - volt
			#stop als de waarde overeenkomt
			#met de winnende waarde
			if(volt == winval):
				break
			#anders bewegen we de servo als
			#een van de schakelaars is gewijzigd
			if(voltprev != volt):
				print("[debug] volt:", volt)
				voltprev = volt
				setPos(((15-volt)/15)*180)
				time.sleep(0.5)
				indicator.ChangeDutyCycle(0)
		print("[debug] wincondition")
		ind = moveDeg(ind, 120, True)
		while True:
			id, text = reader.read()
			if(text.rstrip(' ') == "puz2"):
				setPos(0)
				time.sleep(0.5)
				setPos(180)
				time.sleep(10)
				break
except KeyboardInterrupt:
	print("[debug] stopping")
finally:
	for a in range(4):
		GPIO.output(mpins[a], 0)
	indicator.stop()
	GPIO.cleanup()
