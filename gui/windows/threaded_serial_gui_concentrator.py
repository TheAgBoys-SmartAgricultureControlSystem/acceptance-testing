import collections
import logging
import threading
from tkinter import *
from tkinter import ttk

import serial
from apscheduler.schedulers.background import BackgroundScheduler

import entryvalidation as entr
import geofencing
import irrigation_control as irr
import log_mod
import uploader as tx


# logging.basicConfig(level=logging.DEBUG, filename='gui.log', filemode='a',
# 					format='%(asctime)s - %(processName)s:%(levelname)s - %(funcName)s: %(message)s')


class Nodes:
	# sets and initializes named tuples to store packet data for each sensor node
	Node = collections.namedtuple('node', ['nodeid', 'rssi', 'lat', 'lng', 'soil'])
	node0 = Node(nodeid=0, rssi=0, lat=0.0, lng=0.0, soil=0)
	node0_center = geofencing.Geofence(40.010000, -105.260000)

	node1 = Node(nodeid=0, rssi=0, lat=0.0, lng=0.0, soil=0)
	node1_center = geofencing.Geofence(40.010000, -105.260000)

	node2 = Node(nodeid=0, rssi=0, lat=0.0, lng=0.0, soil=0)
	node2_center = geofencing.Geofence(40.010000, -105.260000)

	node3 = Node(nodeid=0, rssi=0, lat=0.0, lng=0.0, soil=0)
	node3_center = geofencing.Geofence(40.010000, -105.260000)

	log_mod.gui_logger.debug("Node named tuples initialized")


class Window(Frame):
	def __init__(self, master=None):
		super(Window, self).__init__()
		Frame.__init__(self, master)

		self.init_logger = log_mod.setup_logger('init_logger', log_mod.init_log, level=logging.DEBUG)
		self.nodeStatus_logger = log_mod.setup_logger('nodeStatus_logger', log_mod.nodeStatus_log)
		self.stream_logger = log_mod.setup_logger('stream_logger', log_mod.stream_log)
		self.settings_logger = log_mod.setup_logger('settings_logger', log_mod.settings_log)

		self.init_logger.debug("Window instance created")

		self.port = 'COM7'
		self.baud = 9600
		# attempt serial connection with receiver
		try:
			self.serial_port = serial.Serial(
				port=self.port,
				baudrate=self.baud,
				parity="N",
				stopbits=1,
				bytesize=8,
				timeout=8
			)
			print("Connection Successful")
			self.init_logger.info("Connection to %s at %d baud Successful", self.port, self.baud)
		except serial.SerialException:
			print("Error connecting")
			self.init_logger.critical("Failed to connect to %s at %d baud", self.port, self.baud)
			sys.exit()

		self.latitude = 40.011234
		self.latitude_str0 = str(self.latitude)
		self.latitude_str1 = str(self.latitude)
		self.latitude_str2 = str(self.latitude)
		self.latitude_str3 = str(self.latitude)
		self.longitude = -105.261234
		self.longitude_str0 = str(self.longitude)
		self.longitude_str1 = str(self.longitude)
		self.longitude_str2 = str(self.longitude)
		self.longitude_str3 = str(self.longitude)
		self.rssi_min = -103

		self.node0id = '10'
		self.node1id = '11'
		self.node2id = '12'
		self.node3id = '13'

		self.node0soil = 1000
		self.node1soil = 1100
		self.node2soil = 1200
		self.node3soil = 1300

		# start scheduler for background tasks (i.e. refresh)
		self.scheduler = BackgroundScheduler()
		self.init_logger.info("Background Scheduler Started")

		# general pump_status frame
		self.genstatus = LabelFrame(master, width=640, height=240, text="General Status")
		self.genstatus.pack()
		# subsystem pump_status frame
		self.substatus = LabelFrame(master, width=640, height=240, text="Subsystem Status")
		self.substatus.pack()

		# notebook
		self.notebook = ttk.Notebook(self.substatus)
		self.notebook.pack()
		# set frames for notebook
		self.sensorstatus = ttk.Frame(self.notebook)
		self.notebook.add(self.sensorstatus, text='Sensor Status')
		self.irrigationstatus = ttk.Frame(self.notebook)
		self.notebook.add(self.irrigationstatus, text='Irrigation Status')
		self.settings = ttk.Frame(self.notebook)
		self.notebook.add(self.settings, text='Settings')
		self.serialout = ttk.Frame(self.notebook)
		self.notebook.add(self.serialout, text='Serial Output')

		# set pump_status frames and labels for 4 sensor nodes

		# node 0 pump_status frame
		self.nodeframe0 = ttk.LabelFrame(self.sensorstatus, text='Node 0')
		self.nodeframe0.grid(column=0, row=0)
		self.node0labelnodeid = ttk.Label(self.nodeframe0, text='NodeID')
		self.node0labelnodeid.grid(column=0, row=0)
		self.node0labelnodeidres = ttk.Label(self.nodeframe0, text='999')
		self.node0labelnodeidres.grid(column=1, row=0)
		self.node0labelrssi = ttk.Label(self.nodeframe0, text='RSSI')
		self.node0labelrssi.grid(column=0, row=1)
		self.node0labelrssires = ttk.Label(self.nodeframe0, text='999')
		self.node0labelrssires.grid(column=1, row=1)
		self.node0labellat = ttk.Label(self.nodeframe0, text='Lat')
		self.node0labellat.grid(column=0, row=2)
		self.node0labellatres = ttk.Label(self.nodeframe0, text='999')
		self.node0labellatres.grid(column=1, row=2)
		self.node0labellng = ttk.Label(self.nodeframe0, text='Lng')
		self.node0labellng.grid(column=0, row=3)
		self.node0labellngres = ttk.Label(self.nodeframe0, text='999')
		self.node0labellngres.grid(column=1, row=3)
		self.node0labelsoil = ttk.Label(self.nodeframe0, text='Soil')
		self.node0labelsoil.grid(column=0, row=4)
		self.node0labelsoilres = ttk.Label(self.nodeframe0, text='999')
		self.node0labelsoilres.grid(column=1, row=4)
		self.node0labelstatus = ttk.Label(self.nodeframe0, text='Status')
		self.node0labelstatus.grid(column=0, row=5)
		self.node0labelstatusres = ttk.Label(self.nodeframe0, text='ERROR', background='#f00', foreground='#fff')
		self.node0labelstatusres.grid(column=1, row=5)

		# node 1 pump_status frame
		self.nodeframe1 = ttk.LabelFrame(self.sensorstatus, text='Node 1')
		self.nodeframe1.grid(column=0, row=1)
		self.node1labelnodeid = ttk.Label(self.nodeframe1, text='NodeID')
		self.node1labelnodeid.grid(column=0, row=0)
		self.node1labelnodeidres = ttk.Label(self.nodeframe1, text='999')
		self.node1labelnodeidres.grid(column=1, row=0)
		self.node1labelrssi = ttk.Label(self.nodeframe1, text='RSSI')
		self.node1labelrssi.grid(column=0, row=1)
		self.node1labelrssires = ttk.Label(self.nodeframe1, text='999')
		self.node1labelrssires.grid(column=1, row=1)
		self.node1labellat = ttk.Label(self.nodeframe1, text='Lat')
		self.node1labellat.grid(column=0, row=2)
		self.node1labellatres = ttk.Label(self.nodeframe1, text='999')
		self.node1labellatres.grid(column=1, row=2)
		self.node1labellng = ttk.Label(self.nodeframe1, text='Lng')
		self.node1labellng.grid(column=0, row=3)
		self.node1labellngres = ttk.Label(self.nodeframe1, text='999')
		self.node1labellngres.grid(column=1, row=3)
		self.node1labelsoil = ttk.Label(self.nodeframe1, text='Soil')
		self.node1labelsoil.grid(column=0, row=4)
		self.node1labelsoilres = ttk.Label(self.nodeframe1, text='999')
		self.node1labelsoilres.grid(column=1, row=4)
		self.node1labelstatus = ttk.Label(self.nodeframe1, text='Status')
		self.node1labelstatus.grid(column=0, row=5)
		self.node1labelstatusres = ttk.Label(self.nodeframe1, text='ERROR', background='#f00', foreground='#fff')
		self.node1labelstatusres.grid(column=1, row=5)

		# node 2 pump_status frame
		self.nodeframe2 = ttk.LabelFrame(self.sensorstatus, text='Node 2')
		self.nodeframe2.grid(column=1, row=0)
		self.node2labelnodeid = ttk.Label(self.nodeframe2, text='NodeID')
		self.node2labelnodeid.grid(column=0, row=0)
		self.node2labelnodeidres = ttk.Label(self.nodeframe2, text='999')
		self.node2labelnodeidres.grid(column=1, row=0)
		self.node2labelrssi = ttk.Label(self.nodeframe2, text='RSSI')
		self.node2labelrssi.grid(column=0, row=1)
		self.node2labelrssires = ttk.Label(self.nodeframe2, text='999')
		self.node2labelrssires.grid(column=1, row=1)
		self.node2labellat = ttk.Label(self.nodeframe2, text='Lat')
		self.node2labellat.grid(column=0, row=2)
		self.node2labellatres = ttk.Label(self.nodeframe2, text='999')
		self.node2labellatres.grid(column=1, row=2)
		self.node2labellng = ttk.Label(self.nodeframe2, text='Lng')
		self.node2labellng.grid(column=0, row=3)
		self.node2labellngres = ttk.Label(self.nodeframe2, text='999')
		self.node2labellngres.grid(column=1, row=3)
		self.node2labelsoil = ttk.Label(self.nodeframe2, text='Soil')
		self.node2labelsoil.grid(column=0, row=4)
		self.node2labelsoilres = ttk.Label(self.nodeframe2, text='999')
		self.node2labelsoilres.grid(column=1, row=4)
		self.node2labelstatus = ttk.Label(self.nodeframe2, text='Status')
		self.node2labelstatus.grid(column=0, row=5)
		self.node2labelstatusres = ttk.Label(self.nodeframe2, text='ERROR', background='#f00', foreground='#fff')
		self.node2labelstatusres.grid(column=1, row=5)

		# node 3 pump_status frame
		self.nodeframe3 = ttk.LabelFrame(self.sensorstatus, text='Node 3')
		self.nodeframe3.grid(column=1, row=1)
		self.node3labelnodeid = ttk.Label(self.nodeframe3, text='NodeID')
		self.node3labelnodeid.grid(column=0, row=0)
		self.node3labelnodeidres = ttk.Label(self.nodeframe3, text='999')
		self.node3labelnodeidres.grid(column=1, row=0)
		self.node3labelrssi = ttk.Label(self.nodeframe3, text='RSSI')
		self.node3labelrssi.grid(column=0, row=1)
		self.node3labelrssires = ttk.Label(self.nodeframe3, text='999')
		self.node3labelrssires.grid(column=1, row=1)
		self.node3labellat = ttk.Label(self.nodeframe3, text='Lat')
		self.node3labellat.grid(column=0, row=2)
		self.node3labellatres = ttk.Label(self.nodeframe3, text='999')
		self.node3labellatres.grid(column=1, row=2)
		self.node3labellng = ttk.Label(self.nodeframe3, text='Lng')
		self.node3labellng.grid(column=0, row=3)
		self.node3labellngres = ttk.Label(self.nodeframe3, text='999')
		self.node3labellngres.grid(column=1, row=3)
		self.node3labelsoil = ttk.Label(self.nodeframe3, text='Soil')
		self.node3labelsoil.grid(column=0, row=4)
		self.node3labelsoilres = ttk.Label(self.nodeframe3, text='999')
		self.node3labelsoilres.grid(column=1, row=4)
		self.node3labelstatus = ttk.Label(self.nodeframe3, text='Status')
		self.node3labelstatus.grid(column=0, row=5)
		self.node3labelstatusres = ttk.Label(self.nodeframe3, text='ERROR', background='#f00', foreground='#fff')
		self.node3labelstatusres.grid(column=1, row=5)

		self.init_logger.debug("Finished building gui skeleton")

		# node settings frame

		# node 0 settings frame
		self.node0settings = LabelFrame(self.settings, width=640, height=240, text="Node 0")
		self.node0settings.grid(column=0, row=0)
		# node 0 lat label
		self.node0settingslbl_lat = Label(self.node0settings, text="Latitude")
		self.node0settingslbl_lat.grid(column=1, row=2)
		self.node0settingsinp_lat = entr.FloatEntry(self.node0settings, width=11)
		self.node0settingsinp_lat.grid(column=2, row=2)
		# node 0 lng label
		self.node0settingslbl_lng = Label(self.node0settings, text="Longitude")
		self.node0settingslbl_lng.grid(column=1, row=3)
		self.node0settingsinp_lng = entr.FloatEntry(self.node0settings, width=11)
		self.node0settingsinp_lng.grid(column=2, row=3)
		# node 0 id label
		self.node0settingslbl_id = Label(self.node0settings, text="Node ID")
		self.node0settingslbl_id.grid(column=1, row=4)
		self.node0settingsinp_id = entr.StrEntry(self.node0settings, width=3)
		self.node0settingsinp_id.grid(column=2, row=4)
		# node 0 soil label
		self.node0settingslbl_soil = Label(self.node0settings, text="Soil Moisture")
		self.node0settingslbl_soil.grid(column=1, row=5)
		self.node0settingsinp_soil = entr.IntEntry(self.node0settings, width=4)
		self.node0settingsinp_soil.grid(column=2, row=5)

		# node 1 settings frame
		self.node1settings = LabelFrame(self.settings, width=640, height=240, text="Node 1")
		self.node1settings.grid(column=0, row=1)
		# node 1 lat label
		self.node1settingslbl_lat = Label(self.node1settings, text="Latitude")
		self.node1settingslbl_lat.grid(column=1, row=2)
		self.node1settingsinp_lat = entr.FloatEntry(self.node1settings, width=11)
		self.node1settingsinp_lat.grid(column=2, row=2)
		# node 1 lng label
		self.node1settingslbl_lng = Label(self.node1settings, text="Longitude")
		self.node1settingslbl_lng.grid(column=1, row=3)
		self.node1settingsinp_lng = entr.FloatEntry(self.node1settings, width=11)
		self.node1settingsinp_lng.grid(column=2, row=3)
		# node 1 id label
		self.node1settingslbl_id = Label(self.node1settings, text="Node ID")
		self.node1settingslbl_id.grid(column=1, row=4)
		self.node1settingsinp_id = entr.StrEntry(self.node1settings, width=3)
		self.node1settingsinp_id.grid(column=2, row=4)
		# node 1 soil label
		self.node1settingslbl_soil = Label(self.node1settings, text="Soil Moisture")
		self.node1settingslbl_soil.grid(column=1, row=5)
		self.node1settingsinp_soil = entr.IntEntry(self.node1settings, width=4)
		self.node1settingsinp_soil.grid(column=2, row=5)

		# node 2 settings frame
		self.node2settings = LabelFrame(self.settings, width=640, height=240, text="Node 2")
		self.node2settings.grid(column=1, row=0)
		# node 2 lat label
		self.node2settingslbl_lat = Label(self.node2settings, text="Latitude")
		self.node2settingslbl_lat.grid(column=1, row=2)
		self.node2settingsinp_lat = entr.FloatEntry(self.node2settings, width=11)
		self.node2settingsinp_lat.grid(column=2, row=2)
		# node 2 lng label
		self.node2settingslbl_lng = Label(self.node2settings, text="Longitude")
		self.node2settingslbl_lng.grid(column=1, row=3)
		self.node2settingsinp_lng = entr.FloatEntry(self.node2settings, width=11)
		self.node2settingsinp_lng.grid(column=2, row=3)
		# node 2 id label
		self.node2settingslbl_id = Label(self.node2settings, text="Node ID")
		self.node2settingslbl_id.grid(column=1, row=4)
		self.node2settingsinp_id = entr.StrEntry(self.node2settings, width=3)
		self.node2settingsinp_id.grid(column=2, row=4)
		# node 2 soil label
		self.node2settingslbl_soil = Label(self.node2settings, text="Soil Moisture")
		self.node2settingslbl_soil.grid(column=1, row=5)
		self.node2settingsinp_soil = entr.IntEntry(self.node2settings, width=4)
		self.node2settingsinp_soil.grid(column=2, row=5)

		# node 3 settings frame
		self.node3settings = LabelFrame(self.settings, width=640, height=240, text="Node 3")
		self.node3settings.grid(column=1, row=1)
		# node 3 lat label
		self.node3settingslbl_lat = Label(self.node3settings, text="Latitude")
		self.node3settingslbl_lat.grid(column=1, row=2)
		self.node3settingsinp_lat = entr.FloatEntry(self.node3settings, width=11)
		self.node3settingsinp_lat.grid(column=2, row=2)
		# node 3 lng label
		self.node3settingslbl_lng = Label(self.node3settings, text="Longitude")
		self.node3settingslbl_lng.grid(column=1, row=3)
		self.node3settingsinp_lng = entr.FloatEntry(self.node3settings, width=11)
		self.node3settingsinp_lng.grid(column=2, row=3)
		# node 3 id label
		self.node3settingslbl_id = Label(self.node3settings, text="Node ID")
		self.node3settingslbl_id.grid(column=1, row=4)
		self.node3settingsinp_id = entr.StrEntry(self.node3settings, width=3)
		self.node3settingsinp_id.grid(column=2, row=4)
		# node 3 soil label
		self.node3settingslbl_soil = Label(self.node3settings, text="Soil Moisture")
		self.node3settingslbl_soil.grid(column=1, row=5)
		self.node3settingsinp_soil = entr.IntEntry(self.node3settings, width=4)
		self.node3settingsinp_soil.grid(column=2, row=5)

		# pump and valve settings
		self.pumpsettings = LabelFrame(self.genstatus, width=320, height=240, text="Irrigation Status")
		self.pumpsettings.grid(column=2, row=0)
		self.pumpsettlingslbl = Label(self.pumpsettings, text="Pump")
		self.pumpsettlingslbl.grid(column=0, row=0)

		self.valvecontrol = LabelFrame(self.irrigationstatus, width=640, height=240, text="Valve Control")
		self.valvecontrol.grid(column=0, row=0)

		# valve control 0
		self.valveframe0 = ttk.LabelFrame(self.valvecontrol, text='Valve 0')
		self.valveframe0.grid(column=0, row=0)
		self.valve0labelstatus = ttk.Label(self.valveframe0, text='Status')
		self.valve0labelstatus.grid(column=0, row=0)
		self.valve0labelstatus = ttk.Label(self.pumpsettings, text='Valve 0: N/A')
		self.valve0labelstatus.grid(column=2, row=0)

		# valve control 1
		self.valveframe1 = ttk.LabelFrame(self.valvecontrol, text='Valve 1')
		self.valveframe1.grid(column=0, row=1)
		self.valve1labelstatus = ttk.Label(self.valveframe1, text='Status')
		self.valve1labelstatus.grid(column=0, row=0)
		self.valve1labelstatus = ttk.Label(self.pumpsettings, text='Valve 1: N/A')
		self.valve1labelstatus.grid(column=3, row=0)

		# valve control 2
		self.valveframe2 = ttk.LabelFrame(self.valvecontrol, text='Valve 2')
		self.valveframe2.grid(column=0, row=2)
		self.valve2labelstatus = ttk.Label(self.valveframe2, text='Status')
		self.valve2labelstatus.grid(column=0, row=0)
		self.valve2labelstatus = ttk.Label(self.pumpsettings, text='Valve 2: N/A')
		self.valve2labelstatus.grid(column=4, row=0)

		# initialize buttons and other gui stuff
		self.init_window()

		# daemonize and start threading for serial port reading and sensor pump_status refreshing
		self.thread = threading.Thread(target=self.read_from_port, args=())
		self.thread.daemon = True
		self.scheduler.add_job(self.refresh_sensor_status, 'interval', seconds=20)
		self.scheduler.add_job(tx.transmit_latest_stream_log, 'cron', day_of_week='mon', hour=7, minute=0)
		self.scheduler.start()
		self.thread.start()

		self.init_logger.debug("Thread daemonized and Jobs added")

	def init_window(self):
		self.master.title("Smart Agriculture Control System Interface")
		# button for refreshing sensor pump_status
		self.refreshButton = ttk.Button(self.sensorstatus, text="Refresh", command=self.refresh_sensor_status)
		self.refreshButton.grid(column=2, row=0)

		# label for serial output in serial output frame
		self.serialout = ttk.Label(self.serialout, text='999', background='#000', foreground='#fff', anchor=W, width=75)
		self.serialout.grid(column=0, row=0)

		self.quitConnection = ttk.Button(self.genstatus, text="Exit", command=self.connection_exit)
		self.quitConnection.grid(column=0, row=0)

		# node 0 coords button
		self.node0settingsbtn_coord = Button(self.node0settings, text="Set Coordinates",
											 command=lambda: self.set_coords(0))
		self.node0settingsbtn_coord.grid(column=2, row=6)
		# node 0 id button
		self.node0settingsbtn_id = Button(self.node0settings, text="Set Node ID", command=lambda: self.set_nodeids(0))
		self.node0settingsbtn_id.grid(column=1, row=7)

		# node 0 soil moisture button
		self.node0settingsbtn_soil = Button(self.node0settings, text="Set Soil Moisture",
											command=lambda: self.set_nodesoil(0))
		self.node0settingsbtn_soil.grid(column=1, row=6)

		# node 1 coords button
		self.node1settingsbtn_coord = Button(self.node1settings, text="Set Coordinates",
											 command=lambda: self.set_coords(1))
		self.node1settingsbtn_coord.grid(column=2, row=6)
		# node 1 id button
		self.node1settingsbtn_id = Button(self.node1settings, text="Set Node ID", command=lambda: self.set_nodeids(1))
		self.node1settingsbtn_id.grid(column=1, row=7)

		# node 1 soil moisture button
		self.node1settingsbtn_soil = Button(self.node1settings, text="Set Soil Moisture",
											command=lambda: self.set_nodesoil(1))
		self.node1settingsbtn_soil.grid(column=1, row=6)

		# node 2 coords button
		self.node2settingsbtn = Button(self.node2settings, text="Set Coordinates",
									   command=lambda: self.set_coords(2))
		self.node2settingsbtn.grid(column=2, row=6)
		# node 2 id button
		self.node2settingsbtn_id = Button(self.node2settings, text="Set Node ID", command=lambda: self.set_nodeids(2))
		self.node2settingsbtn_id.grid(column=1, row=7)

		# node 2 soil moisture button
		self.node2settingsbtn_soil = Button(self.node2settings, text="Set Soil Moisture",
											command=lambda: self.set_nodesoil(2))
		self.node2settingsbtn_soil.grid(column=1, row=6)

		# node 3 coords button
		self.node3settingsbtn_coord = Button(self.node3settings, text="Set Coordinates",
											 command=lambda: self.set_coords(3))
		self.node3settingsbtn_coord.grid(column=2, row=6)
		# node 3 id button
		self.node3settingsbtn_id = Button(self.node3settings, text="Set Node ID", command=lambda: self.set_nodeids(3))
		self.node3settingsbtn_id.grid(column=1, row=7)

		# node 3 soil moisture button
		self.node3settingsbtn_soil = Button(self.node3settings, text="Set Soil Moisture",
											command=lambda: self.set_nodesoil(3))
		self.node3settingsbtn_soil.grid(column=1, row=6)

		# pump button
		self.pumpsettingsbtn = Button(self.pumpsettings, text="OFF", command=lambda: self.pumptogglewrapper())
		self.pumpsettingsbtn.grid(column=1, row=0)

		# valve 0 button
		self.valve0controlbtn = Button(self.valveframe0, text="OFF", command=lambda: self.valvetogglewrapper(0))
		self.valve0controlbtn.grid(column=2, row=0)

		# valve 1 button
		self.valve1controlbtn = Button(self.valveframe1, text="OFF", command=lambda: self.valvetogglewrapper(1))
		self.valve1controlbtn.grid(column=2, row=0)

		# valve 2 button
		self.valve2controlbtn = Button(self.valveframe2, text="OFF", command=lambda: self.valvetogglewrapper(2))
		self.valve2controlbtn.grid(column=2, row=0)

		self.init_logger.debug("GUI fleshed out")

	def pumptogglewrapper(self):
		if irr.toggle_pump():
			self.pumpsettingsbtn.configure(text="ON")
			return True
		else:
			self.pumpsettingsbtn.configure(text="OFF")
			return False

	def valvetogglewrapper(self, valve):
		try:
			if valve == 0:
				if irr.toggle_valve(valve):
					self.valve0controlbtn.configure(text="ON")
					self.valve0labelstatus.configure(text="Valve 0: ON")
					return True
				else:
					self.valve0controlbtn.configure(text="OFF")
					self.valve0labelstatus.configure(text="Valve 0: OFF")
					return False
			elif valve == 1:
				if irr.toggle_valve(valve):
					self.valve1controlbtn.configure(text="ON")
					self.valve1labelstatus.configure(text="Valve 1: ON")
					return True
				else:
					self.valve1controlbtn.configure(text="OFF")
					self.valve1labelstatus.configure(text="Valve 1: OFF")
					return False
			elif valve == 2:
				if irr.toggle_valve(valve):
					self.valve2controlbtn.configure(text="ON")
					self.valve2labelstatus.configure(text="Valve 2: ON")
					return True
				else:
					self.valve2controlbtn.configure(text="OFF")
					self.valve2labelstatus.configure(text="Valve 2: OFF")
					return False
		except IOError:
			irr.irrigation_logger.error("Unable to toggle solenoid ", valve)
			pass

	def read_from_port(self):
		while True:
			# read byte lines from serial port, decode and strip bytestream
			self.reading = self.serial_port.readline().decode('utf-8')
			self.stream_logger.debug("Incoming Packet String: [%s]", self.reading)
			self.reading = self.reading.lstrip(
				chr(27) + "8" + chr(27) + "7" + chr(27) + "[10r" + chr(27) + "[1;1H" + chr(27) + "[2K" + chr(
					27) + "[2J " + chr(27) + "[0;0H")
			self.reading = self.reading.rstrip('\n')
			self.processed_data = str(self.reading)

			try:
				# ignore newline lines
				if str(self.processed_data).isspace():
					pass
				else:
					self.stream_logger.info("Processed Packet String: [%s]", self.processed_data.rstrip('\r\n'))
					# send serial output packets to serial output frame
					self.serialout.configure(text=self.processed_data)
					# split packet into variables
					self.processed_data = self.processed_data.split('#')

					# send packet data to appropriate named tuples
					if self.processed_data[0][7:] == self.node0id:
						Nodes.node0 = Nodes.node0._replace(nodeid=self.processed_data[0][7:],
														   rssi=self.processed_data[4][5:],
														   lat=self.processed_data[2][9:],
														   lng=self.processed_data[3][10:],
														   soil=self.processed_data[1][13:])
					if self.processed_data[0][7:] == self.node1id:
						Nodes.node1 = Nodes.node1._replace(nodeid=self.processed_data[0][7:],
														   rssi=self.processed_data[4][5:],
														   lat=self.processed_data[2][9:],
														   lng=self.processed_data[3][10:],
														   soil=self.processed_data[1][13:])
					if self.processed_data[0][7:] == self.node2id:
						Nodes.node2 = Nodes.node2._replace(nodeid=self.processed_data[0][7:],
														   rssi=self.processed_data[4][5:],
														   lat=self.processed_data[2][9:],
														   lng=self.processed_data[3][10:],
														   soil=self.processed_data[1][13:])
					if self.processed_data[0][7:] == self.node3id:
						Nodes.node3 = Nodes.node3._replace(nodeid=self.processed_data[0][7:],
														   rssi=self.processed_data[4][5:],
														   lat=self.processed_data[2][9:],
														   lng=self.processed_data[3][10:],
														   soil=self.processed_data[1][13:])
						self.stream_logger.debug("Packet data sent to appropriate named tuples")
			except IndexError:
				self.stream_logger.error("Index Error in filling packet named tuples with packet strings")
				pass
			except ValueError:
				self.stream_logger.error("Value Error in filling packet named tuples with packet strings")
				pass

	def refresh_sensor_status(self):
		print("Sensor Status Refreshed")
		self.nodeStatus_logger.info("Sensor Status Refreshed")
		# set node frames in sensor pump_status frame to fresh values
		self.node0labelnodeidres.configure(text=Nodes.node0.nodeid)
		self.node0labelrssires.configure(text=Nodes.node0.rssi)
		self.node0labellatres.configure(text=Nodes.node0.lat)
		self.node0labellngres.configure(text=Nodes.node0.lng)
		self.node0labelsoilres.configure(text=Nodes.node0.soil)
		self.nodeStatus_logger.debug("Node 0 refreshed")

		self.node1labelnodeidres.configure(text=Nodes.node1.nodeid)
		self.node1labelrssires.configure(text=Nodes.node1.rssi)
		self.node1labellatres.configure(text=Nodes.node1.lat)
		self.node1labellngres.configure(text=Nodes.node1.lng)
		self.node1labelsoilres.configure(text=Nodes.node1.soil)
		self.nodeStatus_logger.debug("Node 1 refreshed")

		self.node2labelnodeidres.configure(text=Nodes.node2.nodeid)
		self.node2labelrssires.configure(text=Nodes.node2.rssi)
		self.node2labellatres.configure(text=Nodes.node2.lat)
		self.node2labellngres.configure(text=Nodes.node2.lng)
		self.node2labelsoilres.configure(text=Nodes.node2.soil)
		self.nodeStatus_logger.debug("Node 2 refreshed")

		self.node3labelnodeidres.configure(text=Nodes.node3.nodeid)
		self.node3labelrssires.configure(text=Nodes.node3.rssi)
		self.node3labellatres.configure(text=Nodes.node3.lat)
		self.node3labellngres.configure(text=Nodes.node3.lng)
		self.node3labelsoilres.configure(text=Nodes.node3.soil)
		self.nodeStatus_logger.debug("Node 3 refreshed")

		# set node pump_status based on rssi, coords
		try:
			# get fresh soil
			self.node0soil = self.node0settingsinp_soil.get()
			self.node1soil = self.node1settingsinp_soil.get()
			self.node2soil = self.node2settingsinp_soil.get()
			self.node3soil = self.node3settingsinp_soil.get()

			node0_rssi = (int(Nodes.node0.rssi) >= int(self.rssi_min))
			node0_inside = Nodes.node0_center.in_geofence((float(Nodes.node0.lat), float(Nodes.node0.lng)))
			node0_soil = ((int(self.node0soil) + 100) >= int(Nodes.node0.soil) >= (int(self.node0soil) - 100))

			node1_rssi = (int(Nodes.node1.rssi) >= int(self.rssi_min))
			node1_inside = Nodes.node1_center.in_geofence((float(Nodes.node1.lat), float(Nodes.node1.lng)))
			node1_soil = ((int(self.node1soil) + 100) >= int(Nodes.node1.soil) >= (int(self.node1soil) - 100))

			node2_rssi = (int(Nodes.node2.rssi) >= int(self.rssi_min))
			node2_inside = Nodes.node2_center.in_geofence((float(Nodes.node2.lat), float(Nodes.node2.lng)))
			node2_soil = ((int(self.node2soil) + 100) >= int(Nodes.node2.soil) >= (int(self.node2soil) - 100))

			node3_rssi = (int(Nodes.node3.rssi) >= int(self.rssi_min))
			node3_inside = Nodes.node3_center.in_geofence((float(Nodes.node3.lat), float(Nodes.node3.lng)))
			node3_soil = ((int(self.node3soil) + 100) >= int(Nodes.node3.soil) >= (int(self.node3soil) - 100))

			if node0_rssi and node0_inside and node0_soil:
				self.node0labelstatusres.configure(text='OK', background='#0f0', foreground='#fff', width=10,
												   anchor=CENTER)
			elif not node0_rssi:
				self.node0labelstatusres.configure(text='CONN ERROR', background='#f00', foreground='#fff',
												   anchor=CENTER,
												   width=10)
			elif not node0_inside:
				self.node0labelstatusres.configure(text='LOC ERROR', background='#f00', foreground='#fff',
												   anchor=CENTER,
												   width=10)
			elif not node0_soil:
				self.node0labelstatusres.configure(text='SOIL ERROR', background='#f00', foreground='#fff',
												   anchor=CENTER,
												   width=10)
			else:
				self.node0labelstatusres.configure(text='WARNING', background='#f00', foreground='#fff', anchor=CENTER,
												   width=10)
			if node1_rssi and node1_inside and node1_soil:
				self.node1labelstatusres.configure(text='OK', background='#0f0', foreground='#fff', width=10,
												   anchor=CENTER)
			elif not node1_rssi:
				self.node1labelstatusres.configure(text='CONN ERROR', background='#f00', foreground='#fff',
												   anchor=CENTER,
												   width=10)
			elif not node1_inside:
				self.node1labelstatusres.configure(text='LOC ERROR', background='#f00', foreground='#fff',
												   anchor=CENTER,
												   width=10)
			elif not node1_soil:
				self.node1labelstatusres.configure(text='SOIL ERROR', background='#f00', foreground='#fff',
												   anchor=CENTER,
												   width=10)
			else:
				self.node1labelstatusres.configure(text='WARNING', background='#f00', foreground='#fff', anchor=CENTER,
												   width=10)
			if node2_rssi and node2_inside and node2_soil:
				self.node2labelstatusres.configure(text='OK', background='#0f0', foreground='#fff', width=10,
												   anchor=CENTER)
			elif not node2_rssi:
				self.node2labelstatusres.configure(text='CONN ERROR', background='#f00', foreground='#fff',
												   anchor=CENTER,
												   width=10)
			elif not node2_inside:
				self.node2labelstatusres.configure(text='LOC ERROR', background='#f00', foreground='#fff',
												   anchor=CENTER,
												   width=10)
			elif not node2_soil:
				self.node2labelstatusres.configure(text='SOIL ERROR', background='#f00', foreground='#fff',
												   anchor=CENTER,
												   width=10)
			else:
				self.node2labelstatusres.configure(text='WARNING', background='#f00', foreground='#fff', anchor=CENTER,
												   width=10)
			if node3_rssi and node3_inside and node3_soil:
				self.node3labelstatusres.configure(text='OK', background='#0f0', foreground='#fff', width=10,
												   anchor=CENTER)
			elif not node3_rssi:
				self.node3labelstatusres.configure(text='CONN ERROR', background='#f00', foreground='#fff',
												   anchor=CENTER,
												   width=10)
			elif not node3_inside:
				self.node3labelstatusres.configure(text='LOC ERROR', background='#f00', foreground='#fff',
												   anchor=CENTER,
												   width=10)
			elif not node3_soil:
				self.node3labelstatusres.configure(text='SOIL ERROR', background='#f00', foreground='#fff',
												   anchor=CENTER,
												   width=10)
			else:
				self.node3labelstatusres.configure(text='ERROR', background='#f00', foreground='#fff', anchor=CENTER,
												   width=10)

			self.nodeStatus_logger.info("Node Status Set")
		except TypeError:
			self.nodeStatus_logger.error("Type Error in setting Node pump_status")
			pass

	def connection_exit(self):  # processes button press to close serial session and exit the program
		self.serial_port.close()
		root.quit()
		self.scheduler.shutdown()
		log_mod.gui_logger.info("Quitting GUI program")
		sys.exit()

	def set_nodeids(self, node):
		print("Setting Node IDs for Node " + str(node))
		self.settings_logger.info("Setting Node IDs for Node " + str(node))

		if node == 0:
			self.node0id = self.node0settingsinp_id.get()
			print("Node ID for Node 0 set to " + self.node0id)
			self.settings_logger.info("Node ID for Node 0 set to " + self.node0id)
		elif node == 1:
			self.node1id = self.node1settingsinp_id.get()
			print("Node ID for Node 1 set to " + self.node1id)
			self.settings_logger.info("Node ID for Node 1 set to " + self.node1id)
		elif node == 2:
			self.node2id = self.node2settingsinp_id.get()
			print("Node ID for Node 2 set to " + self.node2id)
			self.settings_logger.info("Node ID for Node 2 set to " + self.node2id)
		elif node == 3:
			self.node3id = self.node3settingsinp_id.get()
			print("Node ID for Node 3 set to " + self.node3id)
			self.settings_logger.info("Node ID for Node 3 set to " + self.node3id)
		else:
			self.settings_logger.warning("Failed Setting Node ID: Malformed input " + str(node))

	def set_nodesoil(self, node):
		print("Setting Node Soil Moisture Level for Node " + str(node))
		self.settings_logger.info("Setting Soil Moisture Level for Node " + str(node))

		if node == 0:
			self.node0soil = self.node0settingsinp_soil.get()
			print("Node Soil Moisture Level for Node 0 set to " + self.node0soil)
			self.settings_logger.info("Node Soil Moisture Level for Node 0 set to " + self.node0soil)
		elif node == 1:
			self.node1soil = self.node1settingsinp_soil.get()
			print("Node Soil Moisture Level for Node 1 set to " + self.node1soil)
			self.settings_logger.info("Node Soil Moisture Level for Node 1 set to " + self.node1soil)
		elif node == 2:
			self.node2soil = self.node2settingsinp_soil.get()
			print("Node Soil Moisture Level for Node 2 set to " + self.node2soil)
			self.settings_logger.info("Node Soil Moisture Level for Node 2 set to " + self.node2soil)
		elif node == 3:
			self.node3soil = self.node3settingsinp_soil.get()
			print("Node Soil Moisture Level for Node 3 set to " + self.node3soil)
			self.settings_logger.info("Node Soil Moisture Level for Node 3 set to " + self.node3soil)
		else:
			self.settings_logger.warning("Failed Setting Node Soil Moisture Level: Malformed input " + str(node))

	def set_coords(self, node):
		print("Setting Coords for Node " + str(node))
		self.settings_logger.info("Setting Coords for Node " + str(node))

		if node == 0:
			self.latitude_str0 = self.node0settingsinp_lat.get()
			self.longitude_str0 = self.node0settingsinp_lng.get()
			Nodes.node0_center = geofencing.Geofence(float(self.latitude_str0), float(self.longitude_str0))
			self.settings_logger.info(
				"Coords for Node " + str(node) + " set to " + str(self.node0settingsinp_lat.get()) + "," + str(
					self.node0settingsinp_lng.get()))
			self.settings_logger.info(Nodes.node0_center.center_coords)
		elif node == 1:
			self.latitude_str1 = self.node1settingsinp_lat.get()
			self.longitude_str1 = self.node1settingsinp_lng.get()
			Nodes.node1_center = geofencing.Geofence(float(self.latitude_str1), float(self.longitude_str1))
			self.settings_logger.info(
				"Coords for Node " + str(node) + " set to " + str(self.node1settingsinp_lat.get()) + "," + str(
					self.node1settingsinp_lng.get()))
			self.settings_logger.info(Nodes.node1_center.center_coords)
		elif node == 2:
			self.latitude_str2 = self.node2settingsinp_lat.get()
			self.longitude_str2 = self.node2settingsinp_lng.get()
			Nodes.node2_center = geofencing.Geofence(float(self.latitude_str2), float(self.longitude_str2))
			self.settings_logger.info(
				"Coords for Node " + str(node) + " set to " + str(self.node2settingsinp_lat.get()) + "," + str(
					self.node2settingsinp_lng.get()))
			self.settings_logger.info(Nodes.node2_center.center_coords)
		elif node == 3:
			self.latitude_str3 = self.node3settingsinp_lat.get()
			self.longitude_str3 = self.node3settingsinp_lng.get()
			Nodes.node3_center = geofencing.Geofence(float(self.latitude_str3), float(self.longitude_str3))
			self.settings_logger.info(
				"Coords for Node " + str(node) + " set to " + str(self.node3settingsinp_lat.get()) + "," + str(
					self.node3settingsinp_lng.get()))
			self.settings_logger.info(Nodes.node3_center.center_coords)
		else:
			self.settings_logger.warning("Failed Setting Node Coords: Malformed input " + str(node))


# initialize and start instance of gui
try:
	root = Tk()
	Window(root)
	log_mod.gui_logger.info("GUI instance started")
	root.mainloop()
except RuntimeError:
	print("A Fatal Error Occurred")
	log_mod.gui_logger.critical("Fatal Runtime Error")
	sys.exit()
finally:
	sys.exit()
