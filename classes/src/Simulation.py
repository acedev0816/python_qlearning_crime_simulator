import time
# user define
from Environment import Environment
from Victim import Victim
from Attacker import Attacker
from Citizen import Citizen
from Common import *

class Simulation:
	"""Simulation class is"""
	def __init__(self, env = None, numCitizens = 0, numVictims = 0, numAttackers = 0, days = 0):
		self.env = env
		self.citizens = []
		self.victims = []
		self.attackers = []
		self.days = days

		self.setCitizens (numCitizens)
		self.setVictims (numVictims)
		self.setAttacker (numAttackers)
		self.firtflag = True

	def setEnvironment(self, env):
		self.env = env

	def setCitizens(self, numCitizens):
		for i in range(0,numCitizens):
			lat, lon = generateRandomPosition()
			citizen = Citizen(lat, lon)
			self.citizens.append( citizen )

	def setVictims(self, numVictims):
		for i in range(0,numVictims):
			lat, lon = generateRandomPosition()
			victim = Victim(lat, lon)
			self.victims.append( victim )

	def setAttacker(self, numAttackers):
		for i in range(0,numAttackers):
			lat, lon = generateRandomPosition()
			attacker = Attacker(lat, lon)
			self.attackers.append( attacker )

	def setDays(self, days):
		self.days = days

	def clear(self):
		self.env = None
		self.victims.clear()
		self.attackers.clear()
		self.citizens.clear()
		self.days = 0
		self.firtflag = True

	def initrun(self):
		for i in range(0,4):
			for citizen in self.citizens:
				citizen.move()
			
			for victim in self.victims:
				victim.qLearning(self.env)


			for attacker in self.attackers:
				attacker.qLearning(self.env, self.citizens, self.victims)

	def runStep(self):

		happened_attacks = {
			'lats': [],
			'lons': [],
			'texts' : []
		}
		attack = []

		for i in range(2):

			if self.firtflag:
				self.initrun()
				self.firtflag = False

			for citizen in self.citizens:
				citizen.move()
			
			for victim in self.victims:
				victim.qLearning(self.env)
			for attacker in self.attackers:
				generate_flag = attacker.qLearning(self.env, self.citizens, self.victims)
				if generate_flag:
					lat,lon = attacker.getPosition()
					happened_attacks['lats'].append(lat)
					happened_attacks['lons'].append(lon)
					happened_attacks['texts'].append('Attack')
					attack.append({
						'lats' : lat,
						'lons' : lat,
					})

		return happened_attacks, attack

		
	def run(self):
		self.initrun()
		count = 0
		for i in range(0,self.days * 2):
			print("\ntick",i)
			for citizen in self.citizens:
				citizen.move()
			
			for victim in self.victims:
				victim.qLearning(self.env)
			
			for attacker in self.attackers:
				generate_flag = attacker.qLearning(self.env, self.citizens, self.victims)
				if generate_flag:
					print("tick",i,"generate")
					count += 1

			time.sleep(1)

		print("total: ",count)
		return count
		
	def getAttackerPositions(self):
		lats = []
		lons = []
		
		for attacker in self.attackers:
			lat,lon = attacker.getPosition()
			lats.append(lat)
			lons.append(lon)

		return {
			'lats' : lats,
			'lons' : lons
		}

	def getStationPositions(self):
		lats = []
		lons = []
		
		for station in self.env.stations:
			lat,lon = station.getPosition()
			lats.append(lat)
			lons.append(lon)

		return {
			'lats' : lats,
			'lons' : lons
		}

	

	def getParkPositions(self):
		lats = []
		lons = []
		print(self.env.parks)
		for park in self.env.parks:
			lat,lon = park.getPosition()
			lats.append(lat)
			lons.append(lon)

		return {
			'lats' : lats,
			'lons' : lons
		}
	def getVictimPositions(self):
		lats = []
		lons = []
		
		for victim in self.victims:
			lat,lon = victim.getPosition()
			lats.append(lat)
			lons.append(lon)

		return {
			'lats' : lats,
			'lons' : lons
		}

	def getCitizenPositions(self):
		lats = []
		lons = []
		
		for citizen in self.citizens:
			lat,lon = citizen.getPosition()
			lats.append(lat)
			lons.append(lon)

		return {
			'lats' : lats,
			'lons' : lons
		}
	def getCameraPositions(self):
		lats = []
		lons = []
		
		for camera in self.env.cameras:
			lat,lon = camera.getPosition()
			lats.append(lat)
			lons.append(lon)

		return {
			'lats' : lats,
			'lons' : lons
		}

	def getCampaignPositions(self):
		lats = []
		lons = []
		
		for campaign in self.env.campaigns:
			lat,lon = campaign.getPosition()
			lats.append(lat)
			lons.append(lon)

		return {
			'lats' : lats,
			'lons' : lons
		}

if __name__ == '__main__':

	num_Citizen = 100
	num_Victim = 100
	num_Attacker = 10
	days = 10

	num_camera = 20
	num_Campaign = 10
	camera_effective = 50
	campaign_effective = 200

	simulation = Simulation()

	simulation.setCitizens(num_Citizen)
	simulation.setVictims(num_Victim)	
	simulation.setAttacker(num_Attacker)
	simulation.setDays(days)

	env = Environment(num_camera,num_Campaign,camera_effective,campaign_effective)
	simulation.setEnvironment(env)
	simulation.run()
