class Agent:
	"""Agent class is ..."""
	def __init__(self, lat, lon, age = 0, gender = "male", name = ""):
		self.lat = lat
		self.lon = lon
		self.age = age
		self.gender = gender
		self.name = name
	
	def getPosition(self):
		return self.lat, self.lon
	
	def printPosition(self):
		print("Lat: ", self.lat)
		print("Lon: ", self.lon)
