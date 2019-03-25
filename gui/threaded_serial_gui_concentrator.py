import collections
import logging
import threading
from tkinter import *
from tkinter import ttk

import serial
from apscheduler.schedulers.background import BackgroundScheduler

import geofencing

logging.basicConfig(level=logging.DEBUG, filename='gui.log', filemode='a',
					format='%(asctime)s - %(processName)s:%(levelname)s - %(funcName)s: %(message)s')


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

	logging.debug("Node named tuples initialized")


class Window(Frame):
	def __init__(self, master=None):
		super(Window, self).__init__()
		Frame.__init__(self, master)
		logging.debug("Window instance created")

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
			logging.info("Connection to %s at %d baud Successful", self.port, self.baud)
		except serial.SerialException:
			print("Error connecting")
			logging.critical("Failed to connect to %s at %d baud", self.port, self.baud)
			sys.exit()

		self.latitude = -105.261234
		self.longitude = 40.011234
		self.rssi_min = -103

		# start scheduler for background tasks (i.e. refresh)
		self.scheduler = BackgroundScheduler()
		logging.info("Background Scheduler Started")

		# general status frame
		self.genstatus = LabelFrame(master, width=640, height=240, text="General Status")
		self.genstatus.pack()
		# subsystem status frame
		self.substatus = LabelFrame(master, width=640, height=240, text="Subsystem Status")
		self.substatus.pack()

		# notebook
		self.notebook = ttk.Notebook(self.substatus)
		self.notebook.pack()
		# set frames for notebook
		self.frame1 = ttk.Frame(self.notebook)
		self.notebook.add(self.frame1, text='Sensor Status')
		self.frame2 = ttk.Frame(self.notebook)
		self.notebook.add(self.frame2, text='Serial Output')
		self.frame3 = ttk.Frame(self.notebook)
		self.notebook.add(self.frame3, text='Settings')

		# set frames and labels for 4 sensor nodes
		self.nodeframe0 = ttk.LabelFrame(self.frame1, text='Node 0')
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

		self.nodeframe1 = ttk.LabelFrame(self.frame1, text='Node 1')
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

		self.nodeframe2 = ttk.LabelFrame(self.frame1, text='Node 2')
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

		self.nodeframe3 = ttk.LabelFrame(self.frame1, text='Node 3')
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

		logging.debug("Finished building gui skeleton")

		# node settings frame
		self.node0settings = LabelFrame(self.frame3, width=640, height=240, text="Node 0")
		self.node0settings.grid(column=0, row=0)

		self.node0settingslbl_lat = Label(self.node0settings, text="Latitude")
		self.node0settingslbl_lat.grid(column=1, row=2)
		self.node0settingsinp_lat = Entry(self.node0settings, width=11)
		self.node0settingsinp_lat.grid(column=2, row=2)

		self.node0settingslbl_lng = Label(self.node0settings, text="Longitude")
		self.node0settingslbl_lng.grid(column=1, row=3)
		self.node0settingsinp_lng = Entry(self.node0settings, width=11)
		self.node0settingsinp_lng.grid(column=2, row=3)

		self.node0settingsbtn_lng = Button(self.node0settings, text="Set Coordinates",
										   command=lambda: self.set_coords(0))
		self.node0settingsbtn_lng.grid(column=2, row=4)

		self.node1settings = LabelFrame(self.frame3, width=640, height=240, text="Node 1")
		self.node1settings.grid(column=0, row=1)

		self.node1settingslbl_lat = Label(self.node1settings, text="Latitude")
		self.node1settingslbl_lat.grid(column=1, row=2)
		self.node1settingsinp_lat = Entry(self.node1settings, width=11)
		self.node1settingsinp_lat.grid(column=2, row=2)

		self.node1settingslbl_lng = Label(self.node1settings, text="Longitude")
		self.node1settingslbl_lng.grid(column=1, row=3)
		self.node1settingsinp_lng = Entry(self.node1settings, width=11)
		self.node1settingsinp_lng.grid(column=2, row=3)

		self.node1settingsbtn_lng = Button(self.node1settings, text="Set Coordinates",
										   command=lambda: self.set_coords(1))
		self.node1settingsbtn_lng.grid(column=2, row=4)

		self.node2settings = LabelFrame(self.frame3, width=640, height=240, text="Node 2")
		self.node2settings.grid(column=1, row=0)

		self.node2settingslbl_lat = Label(self.node2settings, text="Latitude")
		self.node2settingslbl_lat.grid(column=1, row=2)
		self.node2settingsinp_lat = Entry(self.node2settings, width=11)
		self.node2settingsinp_lat.grid(column=2, row=2)

		self.node2settingslbl_lng = Label(self.node2settings, text="Longitude")
		self.node2settingslbl_lng.grid(column=1, row=3)
		self.node2settingsinp_lng = Entry(self.node2settings, width=11)
		self.node2settingsinp_lng.grid(column=2, row=3)

		self.node2settingsbtn_lng = Button(self.node2settings, text="Set Coordinates",
										   command=lambda: self.set_coords(2))
		self.node2settingsbtn_lng.grid(column=2, row=4)

		self.node3settings = LabelFrame(self.frame3, width=640, height=240, text="Node 3")
		self.node3settings.grid(column=1, row=1)

		self.node3settingslbl_lat = Label(self.node3settings, text="Latitude")
		self.node3settingslbl_lat.grid(column=1, row=2)
		self.node3settingsinp_lat = Entry(self.node3settings, width=11)
		self.node3settingsinp_lat.grid(column=2, row=2)

		self.node3settingslbl_lng = Label(self.node3settings, text="Longitude")
		self.node3settingslbl_lng.grid(column=1, row=3)
		self.node3settingsinp_lng = Entry(self.node3settings, width=11)
		self.node3settingsinp_lng.grid(column=2, row=3)

		self.node3settingsbtn_lng = Button(self.node3settings, text="Set Coordinates",
										   command=lambda: self.set_coords(3))
		self.node3settingsbtn_lng.grid(column=2, row=4)

		# initialize buttons and other gui stuff
		self.init_window()

		# daemonize and start threading for serial port reading and sensor status refreshing
		self.thread = threading.Thread(target=self.read_from_port, args=())
		self.thread.daemon = True
		self.scheduler.add_job(self.refresh_sensor_status, 'interval', seconds=20)
		self.scheduler.start()
		self.thread.start()

		logging.debug("Thread daemonized and Jobs added")

	def init_window(self):
		self.master.title("Smart Agriculture Control System Interface")
		# button for refreshing sensor status
		self.refreshButton = ttk.Button(self.frame1, text="Refresh", command=self.refresh_sensor_status)
		self.refreshButton.grid(column=2, row=0)

		# label for serial output in serial output frame
		self.serialout = ttk.Label(self.frame2, text='999', background='#000', foreground='#fff', anchor=W, width=70)
		self.serialout.grid(column=0, row=0)

		self.quitConnection = ttk.Button(self.genstatus, text="Exit", command=self.connection_exit)
		self.quitConnection.grid(column=0, row=0)

		logging.debug("GUI fleshed out")

	def read_from_port(self):
		while True:
			# read byte lines from serial port, decode and strip bytestream
			self.reading = self.serial_port.readline().decode('utf-8')
			logging.debug("Incoming Packet String: [%s]", self.reading)
			self.reading = self.reading.lstrip(
				chr(27) + "8" + chr(27) + "7" + chr(27) + "[10r" + chr(27) + "[1;1H" + chr(27) + "[2K" + chr(
					27) + "[2J " + chr(27) + "[0;0H")
			self.reading = self.reading.rstrip('\n')
			self.processed_data = str(self.reading)
			logging.debug("Processed Packet String: [%s]", self.processed_data)

			try:
				# ignore newline lines
				if str(self.processed_data).isspace():
					pass
				else:
					# send serial output packets to serial output frame
					self.serialout.configure(text=self.processed_data)
					# split packet into variables
					self.processed_data = self.processed_data.split('#')

					# send packet data to appropriate named tuples
					if int(self.processed_data[0][7:]) == 10:
						Nodes.node0 = Nodes.node0._replace(nodeid=self.processed_data[0][7:],
														   rssi=self.processed_data[4][5:],
														   lat=self.processed_data[2][9:],
														   lng=self.processed_data[3][10:],
														   soil=self.processed_data[1][13:])
					if int(self.processed_data[0][7:]) == 11:
						Nodes.node1 = Nodes.node1._replace(nodeid=self.processed_data[0][7:],
														   rssi=self.processed_data[4][5:],
														   lat=self.processed_data[2][9:],
														   lng=self.processed_data[3][10:],
														   soil=self.processed_data[1][13:])
					if int(self.processed_data[0][7:]) == 12:
						Nodes.node2 = Nodes.node2._replace(nodeid=self.processed_data[0][7:],
														   rssi=self.processed_data[4][5:],
														   lat=self.processed_data[2][9:],
														   lng=self.processed_data[3][10:],
														   soil=self.processed_data[1][13:])
					if int(self.processed_data[0][7:]) == 13:
						Nodes.node3 = Nodes.node3._replace(nodeid=self.processed_data[0][7:],
														   rssi=self.processed_data[4][5:],
														   lat=self.processed_data[2][9:],
														   lng=self.processed_data[3][10:],
														   soil=self.processed_data[1][13:])
					logging.debug("Packet data sent to appropriate named tuples")
			except IndexError:
				logging.error("Index Error in filling packet named tuples with packet strings")
				pass
			except ValueError:
				logging.error("Value Error in filling packet named tuples with packet strings")
				pass

	def refresh_sensor_status(self):
		print("Sensor Status Refreshed")
		logging.info("Sensor Status Refreshed")
		# set node frames in sensor status frame to fresh values
		self.node0labelnodeidres.configure(text=Nodes.node0.nodeid)
		self.node0labelrssires.configure(text=Nodes.node0.rssi)
		self.node0labellatres.configure(text=Nodes.node0.lat)
		self.node0labellngres.configure(text=Nodes.node0.lng)
		self.node0labelsoilres.configure(text=Nodes.node0.soil)
		logging.debug("Node 0 refreshed")

		self.node1labelnodeidres.configure(text=Nodes.node1.nodeid)
		self.node1labelrssires.configure(text=Nodes.node1.rssi)
		self.node1labellatres.configure(text=Nodes.node1.lat)
		self.node1labellngres.configure(text=Nodes.node1.lng)
		self.node1labelsoilres.configure(text=Nodes.node1.soil)
		logging.debug("Node 1 refreshed")

		self.node2labelnodeidres.configure(text=Nodes.node2.nodeid)
		self.node2labelrssires.configure(text=Nodes.node2.rssi)
		self.node2labellatres.configure(text=Nodes.node2.lat)
		self.node2labellngres.configure(text=Nodes.node2.lng)
		self.node2labelsoilres.configure(text=Nodes.node2.soil)
		logging.debug("Node 2 refreshed")

		self.node3labelnodeidres.configure(text=Nodes.node3.nodeid)
		self.node3labelrssires.configure(text=Nodes.node3.rssi)
		self.node3labellatres.configure(text=Nodes.node3.lat)
		self.node3labellngres.configure(text=Nodes.node3.lng)
		self.node3labelsoilres.configure(text=Nodes.node3.soil)
		logging.debug("Node 3 refreshed")

		# set node status based on rssi, coords
		try:
			if (int(Nodes.node0.rssi) >= int(self.rssi_min)) and (
					float(Nodes.node0.lat) == float(self.node0settingsinp_lat.get())) and (
					float(Nodes.node0.lng) == float(self.node0settingsinp_lng.get())):
				self.node0labelstatusres.configure(text='OK', background='#0f0', foreground='#fff', width=10, anchor=CENTER)
			else:
				self.node0labelstatusres.configure(text='WARNING', background='#f00', foreground='#fff', anchor=CENTER, width=10)
			if (int(Nodes.node1.rssi) >= int(self.rssi_min)) and (
					float(Nodes.node1.lat) == float(self.node1settingsinp_lat.get())) and (
					float(Nodes.node1.lng) == float(self.node1settingsinp_lng.get())):
				self.node1labelstatusres.configure(text='OK', background='#0f0', foreground='#fff', width=10, anchor=CENTER)
			else:
				self.node1labelstatusres.configure(text='WARNING', background='#f00', foreground='#fff', anchor=CENTER, width=10)
			if (int(Nodes.node2.rssi) >= int(self.rssi_min)) and (
					float(Nodes.node2.lat) == float(self.node2settingsinp_lat.get())) and (
					float(Nodes.node2.lng) == float(self.node2settingsinp_lng.get())):
				self.node2labelstatusres.configure(text='OK', background='#0f0', foreground='#fff', width=10, anchor=CENTER)
			else:
				self.node2labelstatusres.configure(text='WARNING', background='#f00', foreground='#fff', anchor=CENTER, width=10)
			if (int(Nodes.node3.rssi) >= int(self.rssi_min)) and (
					float(Nodes.node3.lat) == float(self.node3settingsinp_lat.get())) and (
					float(Nodes.node3.lng) == float(self.node3settingsinp_lng.get())):
				self.node3labelstatusres.configure(text='OK', background='#0f0', foreground='#fff', width=10, anchor=CENTER)
			else:
				self.node3labelstatusres.configure(text='WARNING', background='#f00', foreground='#fff', anchor=CENTER, width=10)

			logging.info("Node Status Set")
		except TypeError:
			logging.error("Type Error in setting Node status")
			pass

	def connection_exit(self):  # processes button press to close serial session and exit the program
		self.serial_port.close()
		root.quit()
		self.scheduler.shutdown()
		logging.info("Quitting GUI program")
		sys.exit()

	def set_coords(self, node):
		print("Setting Coords for Node " + str(node))
		if node == 0:
			Nodes.node0_center.set_geofence(float(self.node0settingsinp_lat.get()), float(self.node0settingsinp_lng.get()))
			print("Coords for Node " + str(node) + " set to " + str(self.node0settingsinp_lat.get()) + "," + str(
				self.node0settingsinp_lng.get()))
			print(Nodes.node0_center.center_coords)
		elif node == 1:
			Nodes.node1_center.set_geofence(float(self.node1settingsinp_lat.get()), float(self.node1settingsinp_lng.get()))
			print("Coords for Node " + str(node) + " set to " + str(self.node1settingsinp_lat.get()) + "," + str(
				self.node1settingsinp_lng.get()))
		elif node == 2:
			Nodes.node2_center.set_geofence(float(self.node2settingsinp_lat.get()), float(self.node2settingsinp_lng.get()))
			print("Coords for Node " + str(node) + " set to " + str(self.node2settingsinp_lat.get()) + "," + str(
				self.node2settingsinp_lng.get()))
		elif node == 3:
			Nodes.node2_center.set_geofence(float(self.node3settingsinp_lat.get()), float(self.node3settingsinp_lng.get()))
			print("Coords for Node " + str(node) + " set to " + str(self.node3settingsinp_lat.get()) + "," + str(
				self.node3settingsinp_lng.get()))
		else:
			pass


# initialize and start instance of gui
try:
	root = Tk()
	Window(root)
	root.mainloop()
	logging.info("GUI instance started")
except RuntimeError:
	print("A Fatal Error Occurred")
	logging.critical("Fatal Runtime Error")
	sys.exit()
finally:
	sys.exit()
