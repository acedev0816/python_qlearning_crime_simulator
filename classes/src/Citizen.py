# user define
from Common import *
from Agent import Agent

class Citizen(Agent):
	"""Citizen class is ..."""
	def __init__(self, lat, lon):

		super().__init__(lat, lon)

	def move(self):
		self.lat ,self.lon = generateRandomPosition()

if __name__ == '__main__':
	lat, lon = generateRandomPosition()
	citizen = Citizen(lat, lon)
	citizen.printPosition()
