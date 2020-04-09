from Common import *
from Agent import Agent
import numpy as np

class Victim(Agent):
	"""Victim class is ..."""
	def __init__(self, lat, lon, age = 0, gender = "female"):

		super().__init__(lat, lon, age, gender)

		self.action_count = 5 # action space size
		self.state_count = 3 # state space size
		self.state = 0 # init state
		self.Q = np.zeros((self.state_count,self.action_count)) # init q-table
		self.R = np.array([[0,0,0,-1,-1],
						   [-1,-1,-1,1,-1],
						   [-1,-1,-1,-1,100]])

	def move(self):
		self.lat ,self.lon = generateRandomPosition()

	def qLearning(self,env):
		# action select
		action = self.predectAction( env,self.state)
		# action implement
		next_state = self.actionImplement(env,action)
		self.state = next_state

	def predectAction(self, env, state):
		action = 0
		if state == 0:
			if env.IsCampaignArea(self.lat,self.lon):
				action = 2
			else:
				action = np.random.randint(2)
		if state == 1:
			action = 3
		if state == 2:
			action = 3
		return action

	def actionImplement(self,env,action):
		next_state = 0
		if action == 0:
			lat, lon = generateRandomPosition()
			while env.IsRiskArea(lat,lon):
				lat, lon = generateRandomPosition()

			self.lat = lat
			self.lon = lon
			next_state = 0
		if action == 1 or action == 2 :
			lat, lon = generateRandomPosition()
			while not env.IsRiskArea(lat,lon):
				lat, lon = generateRandomPosition()

			self.lat = lat
			self.lon = lon
			next_state = 1
		if action == 3:
			lat, lon = generateRandomPosition()
			if env.IsRiskArea(lat,lon):
				next_state = 0
			else:
				next_state = 1
			self.lat = lat
			self.lon = lon
		return next_state


if __name__ == '__main__':
	lat, lon = generateRandomPosition()

	victim = Victim(lat, lon)
	print("init:")
	victim.printPosition()
	victim.move()

	print("Next")
	victim.printPosition()