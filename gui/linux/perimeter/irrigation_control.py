import log_mod
# from pathlib import Path
import time
import RPi.GPIO as GPIO

# log_folderstream = Path("D:/MyDocuments/Dropbox/University/Fall_18/Capstone/code/acceptance-testing/gui/log/")
irrigation_logger = log_mod.setup_logger('irrigation_logger', log_mod.irrigation_log)

numValves = 3
pump_status = False
valve_status = [False for i in range(numValves)]
control_pins = [2, 3, 4, 14, 15, 17, 18, 27, 22, 23, 24, 10, 9, 25, 11, 8, 7, 0, 1, 5, 6, 12, 13, 19, 16, 26, 20, 21]
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(control_pins, GPIO.OUT)

def toggle_pump():
	global pump_status
	try:
		if not pump_status:
			pump_status = True
			# pump_pin = ON
			GPIO.output(control_pins[27], 1)
			print("Pump has been turned ON")
			irrigation_logger.info("Pump has been turned ON")
		else:
			pump_status = False
			# pump_pin = OFF
			GPIO.output(control_pins[27], 0)
			print("Pump has been turned OFF")
			irrigation_logger.info("Pump has been turned OFF")
	except IOError:
		pump_status = False
		print("Error in switching pump")
		irrigation_logger.critical("Error in switching pump")

	return pump_status


def toggle_valve(valvenum, power_pin):
	global valve_status
	try:
		if not valve_status[valvenum]:
			valve_status[valvenum] = True
			helper_toggle_valve(valve_status[valvenum], valvenum, power_pin)
		else:
			valve_status[valvenum] = False
			helper_toggle_valve(valve_status[valvenum], valvenum, power_pin)
	except IOError:
		valve_status[valvenum] = False
		print("Error in switching valve ", valvenum)
		irrigation_logger.critical("Error in switching valve " + str(valvenum))

	return valve_status[valvenum]


def helper_toggle_valve(status, valvenum, power_pin):
	# match valvenum to valve pin index relating to appropriate BCM pin
	global control_pins
	if status:
		valve_pin = "control_pins[valvenum] ON"
		# set polarity relay ON +
		GPIO.output(control_pins[power_pin], 1)
		# pulse from power relay (250ms)
		# pulse ON
		GPIO.output(control_pins[valvenum], 1)
		time.sleep(0.25)
		GPIO.output(control_pins[valvenum], 0)
		# pulse OFF
		print("Solenoid " + str(valvenum) + " has been turned ON")
		irrigation_logger.info("Solenoid " + str(valvenum) + " has been turned ON")
	else:
		valve_pin = "valve_pins[valvenum] OFF"
		# set polarity relay OFF -
		GPIO.output(control_pins[power_pin], 0)
		# pulse from power relay (250ms)
		# pulse ON
		GPIO.output(control_pins[valvenum], 1)
		time.sleep(0.25)
		GPIO.output(control_pins[valvenum], 0)
		# pulse OFF
		print("Solenoid " + str(valvenum) + " has been turned OFF")
		irrigation_logger.info("Solenoid " + str(valvenum) + " has been turned OFF")


# print(toggle_pump())
# print(toggle_pump())
# print(toggle_valve(0))
# print(toggle_valve(0))
# print(toggle_valve(1))
# print(toggle_valve(2))
# print(toggle_valve(1))
# print(toggle_valve(2))

