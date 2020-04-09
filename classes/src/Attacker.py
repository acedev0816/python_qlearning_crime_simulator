import numpy as np
import random

# user define
from Common import *
from Environment import Environment
from Agent import Agent


class Attacker(Agent):
	"""Attacker class is ..."""
	def __init__(self, lat, lon, age = 0, gender = "male"):
		
		super().__init__(lat, lon, age, gender)

		self.action_count = 5 # action space size
		self.state_count = 5  # state space size
		self.epsilon = 0.2 # constant about epsilon greedy policy
		self.state = 0 # init state
		self.alpha = 0.3 #learning rate
		self.gamma  = 0.6 #discout factor
		self.beta = 0.1 #deterioration factor

		self.caught = False # caught flag
		self.caught_day = 0 # caught day
		############################################
		#triger
		self.motivation_trigger = 0.1 # movtivation
		self.phisical_trigger = 0.1 # phiscal
		self.emotional_trigger = 0.1 #emotional
		############################################
		self.Q = np.zeros((self.state_count,self.action_count)) # init q-table
		# Reard matrix
		self.R = np.array([[1, -1, -1, -1, -1],
						   [-1, 1, -1, -1, -1],
						   [-1, -1, 1, -1, -1],
						   [-1, -1, -1, 1, -1],
						   [-1, -1, -1, -1, 100]])


	def Action0move(self, env):
		self.lat ,self.lon = generateRandomPosition()

	def Action1move(self, env):
		pass

	def Action2move(self, env):
		lat, lon = generateRandomPosition()
		self.lat = lat
		self.lon = lon

	def Action3move(self, env):
		lat, lon = generateRandomPosition()
		while env.IsRiskArea(lat,lon):
			lat, lon = generateRandomPosition()

		self.lat = lat
		self.lon = lon

	def Action4move(self, victims):
		self.lat ,self.lon = generateRandomPosition()


	def epsilon_greedy(self, state):
		if np.random.rand() < self.epsilon:
			action = np.random.randint(0, self.action_count)
		else:
			action = state
		return action
	
	def qLearning(self, env, citizens, victims):

		# if caught 
		if self.caught:
			self.caught_day -=1
			if self.caught_day == 0:
				self.caught = False
			return False

		# action select
		action = self.epsilon_greedy(self.state)
		# action implement.
		next_state, done = self.actionImplement(env, citizens, victims, action)

		if done:
			self.state = 0
			return True

		self.state = next_state
		return False



	def actionImplement(self, env, citizens, victims, action):
		next_state = 0
		done = False
		state = self.state
		if action == 0 and self.state == 0:
			next_state = 1
			self.Action0move(env)
			self.Q[state][action] =self.Q[state][action] -  self.beta 

		elif action == 1 and self.state == 1:
			# trigger parameter
			if np.random.rand() > self.motivation_trigger and np.random.rand() > self.phisical_trigger and np.random.rand() > self.emotional_trigger:
				next_state = 2
				self.Q[state][action] = self.Q[state][action] + self.alpha * (self.R[state][action] + self.gamma * np.max(self.Q[next_state,:]) - self.Q[state][action])
			else:
				next_state = 1
				self.Q[state][action] =self.Q[state][action] -  self.beta

			self.Action1move(env)

		elif action == 2 and self.state == 2:
			next_state = 3
			self.Action2move(env)
			self.Q[state][action] =self.Q[state][action] + self.alpha * (self.R[state][action] + self.gamma * np.max(self.Q[next_state,:]) - self.Q[state][action])

		elif action == 3 and self.state == 3:
			next_state = 4
			self.Action3move(env)
			self.Q[state][action] =self.Q[state][action] + self.alpha * (self.R[state][action] + self.gamma * np.max(self.Q[next_state,:]) - self.Q[state][action])


		elif action == 4 and self.state == 4:

			done_flag = False
			# if caught
			if env.IsCameraImpact(self.lat,self.lon):
				self.caught_day = random.randint(0, env.frameDays) 
				self.caught = True
				return next_state, done

			for victim in victims:
				lat, lon = victim.getPosition()
				distance = distance_in_km_between(lat, lon, self.lat, self.lon)
				if distance < 0.1:
					done_flag = True
					break
			if done_flag:
				done = True
				for citizen in citizens:
					lat, lon = citizen.getPosition()
					distance = distance_in_km_between(lat, lon, self.lat, self.lon)
					if distance < 0.05:
						done = False
			if done:		
				next_state == 0
				self.Action4move(victims)

		else:
			next_state = self.state

		return next_state, done


if __name__ == '__main__':

	lat, lon = generateRandomPosition()
	attacker = Attacker(lat, lon)
	attacker.printPosition()