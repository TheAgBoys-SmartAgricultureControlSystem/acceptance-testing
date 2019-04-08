# import log_mod
# from pathlib import Path

# log_folderstream = Path("D:/MyDocuments/Dropbox/University/Fall_18/Capstone/code/acceptance-testing/gui/log/")
# irrigation_logger = log_mod.setup_logger('irrigation_logger', log_mod.irrigation_log)

numValves = 3
pump_status = False
valve_status = [False for i in range(numValves)]
valve_pins = [2, 3, 4, 14, 15, 17, 18, 27, 22, 23, 24, 10, 9, 25, 11, 8, 7, 0, 1, 5, 6, 12, 13, 19, 16, 26, 20, 21]


def toggle_pump():
	global pump_status
	try:
		if not pump_status:
			pump_status = True
			# pump_pin = ON
			# irrigation_logger.info("Pump has been turned ON")
		else:
			pump_status = False
			# pump_pin = OFF
			# irrigation_logger.info("Pump has been turned OFF")
	except IOError:
		pump_status = False
		# irrigation_logger.critical("Error in switching pump")

	return pump_status


def toggle_valve(valvenum):
	global valve_status
	try:
		if not valve_status[valvenum]:
			valve_status[valvenum] = True
			helper_toggle_valve(valve_status[valvenum], valvenum)
		else:
			valve_status[valvenum] = False
			helper_toggle_valve(valve_status[valvenum], valvenum)
	except IOError:
		valve_status[valvenum] = False
		print("Error in switching valve ", valvenum)
		# irrigation_logger.critical("Error in switching valve " + str(valvenum))

	return valve_status[valvenum]


def helper_toggle_valve(status, valvenum):
	# match valvenum to valve pin index relating to appropriate BCM pin
	global valve_pins
	if status:
		valve_pin = "valve_pins[valvenum] ON"
		# positive pulse
		print("Solenoid " + str(valvenum) + " has been turned ON")
		# irrigation_logger.info("Solenoid " + str(valvenum) + " has been turned ON")
	else:
		valve_pin = "valve_pins[valvenum] OFF"
		print("Solenoid " + str(valvenum) + " has been turned OFF")
		# irrigation_logger.info("Solenoid " + str(valvenum) + " has been turned OFF")


# print(toggle_pump())
# print(toggle_pump())
# print(toggle_valve(0))
# print(toggle_valve(0))
# print(toggle_valve(1))
# print(toggle_valve(2))
# print(toggle_valve(1))
# print(toggle_valve(2))

