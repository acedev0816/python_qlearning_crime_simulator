from Common import *
class Campaign:
	"""Campaign class is ..."""
	def __init__(self, lat, lon,  effective):
		self.lat = lat
		self.lon = lon
		self.effective = effective

	def getPosition(self):
		return self.lat, self.lon

	def getEffective(self):
		return self.effective
	
	def setEffective(self, effective):
		self.effective = effective

	def printPosition(self):
		print("Lat: ", self.lat)
		print("Lon: ", self.lon)

	def printEffective(self):
		print("effective: ", self.effective )

if __name__ == '__main__':
	lat, lon = generateRandomPosition()
	campaign = Campaign(lat, lon,50)
	campaign.printPosition()