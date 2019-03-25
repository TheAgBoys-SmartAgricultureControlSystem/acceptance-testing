import threading
import serial
import time
import datetime
import collections
import io


def init_conn():
	port = 'COM7'
	baud = 9600
	global serial_port
	serial_port = serial.Serial(port, baud)


def set_modules():
	while True:
		if (Nodes.node0.nodeid or Nodes.node1.nodeid or Nodes.node2.nodeid or Nodes.node3.nodeid) is None:
			print("Acquiring")
			time.sleep(10)
		else:
			print(Nodes.node0)
			time.sleep(0.1)
			print(Nodes.node1)
			time.sleep(0.1)
			print(Nodes.node2)
			time.sleep(0.1)
			print(Nodes.node3)
			time.sleep(0.1)


class Nodes:
	numModules = 5
	Node = collections.namedtuple('node', ['nodeid', 'rssi', 'lat', 'lng', 'soil'])
	node0 = Node(nodeid=None, rssi=None, lat=None, lng=None, soil=None)
	node1 = Node(nodeid=None, rssi=None, lat=None, lng=None, soil=None)
	node2 = Node(nodeid=None, rssi=None, lat=None, lng=None, soil=None)
	node3 = Node(nodeid=None, rssi=None, lat=None, lng=None, soil=None)


def handle_data(data):
	data = data.rstrip('\n')
	global_data = str(data)
	try:
		if str(global_data).isspace():
			pass
		else:
			print(global_data)
			global_data = global_data.split('#')
			if global_data[0][7:] == '0':
				Nodes.node0 = Nodes.node0._replace(nodeid=global_data[0][7:], rssi=global_data[4][5:], lat=global_data[2][9:],
												   lng=global_data[3][10:], soil=global_data[1][13:])
			if global_data[0][7:] == '1':
				Nodes.node1 = Nodes.node1._replace(nodeid=global_data[0][7:], rssi=global_data[4][5:], lat=global_data[2][9:],
												   lng=global_data[3][10:], soil=global_data[1][13:])
			if global_data[0][7:] == '2':
				Nodes.node2 = Nodes.node2._replace(nodeid=global_data[0][7:], rssi=global_data[4][5:], lat=global_data[2][9:],
												   lng=global_data[3][10:], soil=global_data[1][13:])
			if global_data[0][7:] == '3':
				Nodes.node3 = Nodes.node3._replace(nodeid=global_data[0][7:], rssi=global_data[4][5:], lat=global_data[2][9:],
												   lng=global_data[3][10:], soil=global_data[1][13:])
	except IndexError:
		pass


def read_from_port(ser):
	while True:
		reading = ser.readline().decode('utf-8')
		handle_data(reading)


def main():
	thread = threading.Thread(target=read_from_port, args=(serial_port,))
	thread.start()
	print("Connection Made")
	set_modules()


if __name__ == "__main__":
	init_conn()
	main()
