import collections
import threading
from tkinter import *
from tkinter import ttk

import serial
from apscheduler.schedulers.background import BackgroundScheduler


class Nodes:
	# sets and initializes named tuples to store packet data for each sensor node
	Node = collections.namedtuple('node', ['nodeid', 'rssi', 'lat', 'lng', 'soil'])
	node0 = Node(nodeid=None, rssi=None, lat=None, lng=None, soil=None)
	node1 = Node(nodeid=None, rssi=None, lat=None, lng=None, soil=None)
	node2 = Node(nodeid=None, rssi=None, lat=None, lng=None, soil=None)
	node3 = Node(nodeid=None, rssi=None, lat=None, lng=None, soil=None)


class Window(Frame):
	def __init__(self, master=None):
		super(Window, self).__init__()
		Frame.__init__(self, master)

		# attempt serial connection with receiver
		try:
			self.serial_port = serial.Serial(
				port='COM7',
				baudrate=9600,
				parity="N",
				stopbits=1,
				bytesize=8,
				timeout=8
			)
			print("Connection Successful")
		except serial.SerialException:
			print("Error connecting")
			sys.exit()

		# start scheduler for background tasks (i.e. refresh)
		self.scheduler = BackgroundScheduler()

		# general status frame
		self.genstatus = LabelFrame(master, width=640, height=120, text="General Status")
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

		# initialize buttons and other gui stuff
		self.init_window()

		# daemonize and start threading for serial port reading and sensor status refreshing
		self.thread = threading.Thread(target=self.read_from_port, args=())
		self.thread.daemon = True
		self.scheduler.add_job(self.refresh_sensor_status, 'interval', seconds=20)
		self.scheduler.start()
		self.thread.start()

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

	def read_from_port(self):
		while True:
			# read byte lines from serial port, decode and strip bytestream
			self.reading = self.serial_port.readline().decode('utf-8')
			self.reading = self.reading.rstrip('\n')
			self.global_data = str(self.reading)
			try:
				# ignore newline lines
				if str(self.global_data).isspace():
					pass
				else:
					# send serial output packets to serial output frame
					self.serialout.configure(text=self.global_data)
					# split packet into variables
					self.global_data = self.global_data.split('#')
					# send packet data to appropriate named tuples
					if self.global_data[0][7:] == '0':
						Nodes.node0 = Nodes.node0._replace(nodeid=self.global_data[0][7:], rssi=self.global_data[4][5:],
														   lat=self.global_data[2][9:],
														   lng=self.global_data[3][10:], soil=self.global_data[1][13:])
					if self.global_data[0][7:] == '1':
						Nodes.node1 = Nodes.node1._replace(nodeid=self.global_data[0][7:], rssi=self.global_data[4][5:],
														   lat=self.global_data[2][9:],
														   lng=self.global_data[3][10:], soil=self.global_data[1][13:])
					if self.global_data[0][7:] == '2':
						Nodes.node2 = Nodes.node2._replace(nodeid=self.global_data[0][7:], rssi=self.global_data[4][5:],
														   lat=self.global_data[2][9:],
														   lng=self.global_data[3][10:], soil=self.global_data[1][13:])
					if self.global_data[0][7:] == '3':
						Nodes.node3 = Nodes.node3._replace(nodeid=self.global_data[0][7:], rssi=self.global_data[4][5:],
														   lat=self.global_data[2][9:],
														   lng=self.global_data[3][10:], soil=self.global_data[1][13:])
			except IndexError:
				pass

	def refresh_sensor_status(self):
		print("Sensor Status Refreshed")
		# set node frames in sensor status frame to fresh values
		self.node0labelnodeidres.configure(text=Nodes.node0.nodeid)
		self.node0labelrssires.configure(text=Nodes.node0.rssi)
		self.node0labellatres.configure(text=Nodes.node0.lat)
		self.node0labellngres.configure(text=Nodes.node0.lng)
		self.node0labelsoilres.configure(text=Nodes.node0.soil)

		self.node1labelnodeidres.configure(text=Nodes.node1.nodeid)
		self.node1labelrssires.configure(text=Nodes.node1.rssi)
		self.node1labellatres.configure(text=Nodes.node1.lat)
		self.node1labellngres.configure(text=Nodes.node1.lng)
		self.node1labelsoilres.configure(text=Nodes.node1.soil)

		self.node2labelnodeidres.configure(text=Nodes.node2.nodeid)
		self.node2labelrssires.configure(text=Nodes.node2.rssi)
		self.node2labellatres.configure(text=Nodes.node2.lat)
		self.node2labellngres.configure(text=Nodes.node2.lng)
		self.node2labelsoilres.configure(text=Nodes.node2.soil)

		self.node3labelnodeidres.configure(text=Nodes.node3.nodeid)
		self.node3labelrssires.configure(text=Nodes.node3.rssi)
		self.node3labellatres.configure(text=Nodes.node3.lat)
		self.node3labellngres.configure(text=Nodes.node3.lng)
		self.node3labelsoilres.configure(text=Nodes.node3.soil)

		# set node status based on rssi, coords
		try:
			if (int(Nodes.node0.rssi) >= -103) and (float(Nodes.node0.lat) == -105.26) and (
					float(Nodes.node0.lng) == 40.01):
				self.node0labelstatusres.configure(text='OK', background='#0f0', foreground='#fff', width=10, anchor=CENTER)
			else:
				self.node0labelstatusres.configure(text='WARNING', background='#f00', foreground='#fff', anchor=CENTER, width=10)
			if (int(Nodes.node1.rssi) >= -103) and (float(Nodes.node1.lat) == -105.26) and (
					float(Nodes.node1.lng) == 40.01):
				self.node1labelstatusres.configure(text='OK', background='#0f0', foreground='#fff', width=10, anchor=CENTER)
			else:
				self.node1labelstatusres.configure(text='WARNING', background='#f00', foreground='#fff', anchor=CENTER, width=10)
			if (int(Nodes.node2.rssi) >= -103) and (float(Nodes.node2.lat) == -105.26) and (
					float(Nodes.node2.lng) == 40.01):
				self.node2labelstatusres.configure(text='OK', background='#0f0', foreground='#fff', width=10, anchor=CENTER)
			else:
				self.node2labelstatusres.configure(text='WARNING', background='#f00', foreground='#fff', anchor=CENTER, width=10)
			if (int(Nodes.node3.rssi) >= -103) and (float(Nodes.node3.lat) == -105.26) and (
					float(Nodes.node3.lng) == 40.01):
				self.node3labelstatusres.configure(text='OK', background='#0f0', foreground='#fff', width=10, anchor=CENTER)
			else:
				self.node3labelstatusres.configure(text='WARNING', background='#f00', foreground='#fff', anchor=CENTER, width=10)
		except TypeError:
			pass

	def connection_exit(self):  # processes button press to close serial session and exit the program
		self.serial_port.close()
		root.quit()
		self.scheduler.shutdown()
		sys.exit()


# initialize and start instance of gui
try:
	root = Tk()
	Window(root)
	root.mainloop()
except RuntimeError:
	print("A Fatal Error Occurred")
	sys.exit()
finally:
	sys.exit()
