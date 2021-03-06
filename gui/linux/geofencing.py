import numpy
from osgeo import ogr


class Geofence:
	"""GeoFence class that accepts, latitude and longitude to create the center coordinates and a 25.16m octagonal fence"""
	def __init__(self, latitude, longitude):
		self.center = (latitude, longitude)
		self.center_coords = ogr.Geometry(ogr.wkbPoint)
		self.center_coords.AddPoint(*self.center)

		# ~25.16m radius octagon
		self.north = (0.00023, 0)
		self.north_coords = tuple()
		self.northeast = (0.00016, 0.00016)
		self.northeast_coords = tuple()
		self.east = (0, 0.00023)
		self.east_coords = tuple()
		self.southeast = (-0.00016, 0.00016)
		self.southeast_coords = tuple()
		self.south = (-0.00023, 0)
		self.south_coords = tuple()
		self.southwest = (-0.00016, -0.00016)
		self.southwest_coords = tuple()
		self.west = (0, -0.00023)
		self.west_coords = tuple()
		self.northwest = (0.00016, -0.00016)
		self.northwest_coords = tuple()

		# initialize polygon
		self.polygon = ogr.Geometry(ogr.wkbPolygon)

		# create geofence
		self.init_geofence()

	def create_ring(self):
		"""Internal function to create perimeter points for instance init"""
		self.north_coords = numpy.add(self.center, self.north)
		self.northeast_coords = numpy.add(self.center, self.northeast)
		self.east_coords = numpy.add(self.center, self.east)
		self.southeast_coords = numpy.add(self.center, self.southeast)
		self.south_coords = numpy.add(self.center, self.south)
		self.southwest_coords = numpy.add(self.center, self.southwest)
		self.west_coords = numpy.add(self.center, self.west)
		self.northwest_coords = numpy.add(self.center, self.northwest)

	def create_geofence(self):
		"""Internal function to create GDAL perimeter from perimeter points for instance init"""
		ring = ogr.Geometry(ogr.wkbLinearRing)
		ring.AddPoint(*self.north_coords)
		ring.AddPoint(*self.northeast_coords)
		ring.AddPoint(*self.east_coords)
		ring.AddPoint(*self.southeast_coords)
		ring.AddPoint(*self.south_coords)
		ring.AddPoint(*self.southwest_coords)
		ring.AddPoint(*self.west_coords)
		ring.AddPoint(*self.northwest_coords)
		ring.AddPoint(*self.north_coords)
		self.polygon.AddGeometry(ring)

	def set_geofence(self, latitude, longitude):
		"""External function to set geofence to new coordinates"""
		self.center = (latitude, longitude)
		self.center_coords = ogr.Geometry(ogr.wkbPoint)
		self.center_coords.AddPoint(*self.center)
		self.init_geofence()

	def init_geofence(self):
		"""Internal function to wrap perimeter geometry creation functions"""
		self.create_ring()
		self.create_geofence()

	def in_geofence(self, coordinates):
		"""External function that returns boolean if input coordinates are inside the geofence"""
		coords_transformed = ogr.Geometry(ogr.wkbPoint)
		coords_transformed.AddPoint(*coordinates)
		return self.polygon.Contains(coords_transformed)


# if __name__ == "__main__":
# 	node1 = Geofence(40.011234, -105.261234)
# 	print(node1.center_coords)
# 	coords1 = (40.011234, -105.261234)
# 	print(node1.in_geofence(coords1))
#
# 	center_coords2 = (40.010000, -105.260000)
# 	node1 = Geofence(*center_coords2)
# 	print(node1.center_coords)
# 	coords2 = (40.010000, -105.260000)
# 	print(node1.in_geofence(coords2))
