import random
import decimal
import math as Math

# Westminster Co-Ordinates
lat = 51.5101204
lon = -0.1590662

# distance_divide_factor = 100000
distance_divide_factor = 40000

def degrees_to_radians(degrees):
	return degrees * Math.pi

def distance_in_km_between(lat1, lon1, lat2, lon2):
	# earth_radius_in_km = 6371

	# dLat = degrees_to_radians(lat2-lat1)
	# dLon = degrees_to_radians(lon2-lon1)

	# lat1 = degrees_to_radians(lat1)
	# lat2 = degrees_to_radians(lat2)

	# a = Math.sin(dLat/2) * Math.sin(dLat/2) + Math.sin(dLon/2) * Math.sin(dLon/2) * Math.cos(lat1) * Math.cos(lat2)
	# c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a))

	# distance = earth_radius_in_km * c
	# return distance

	distancePerDegree = 111.14 # l = pi * r /180
	dLat = abs(lat2-lat1) * distancePerDegree
	dLon = abs(lon2-lon1) * distancePerDegree

	distance = Math.sqrt(dLat * dLat + dLon * dLon )
	return distance

def generateRandomPosition():
	if(decimal.Decimal(random.randrange(0,1000))%2 == 0):
		genLate = lat + float(decimal.Decimal(random.randrange(0,1000))/distance_divide_factor)
	else:
		genLate = lat - float(decimal.Decimal(random.randrange(0,1000))/distance_divide_factor)

	if(decimal.Decimal(random.randrange(0,1000))%2 == 0):
		genLon = lon + float(decimal.Decimal(random.randrange(0,1000))/distance_divide_factor)
	else:
		genLon = lon - float(decimal.Decimal(random.randrange(0,1000))/distance_divide_factor)

	return genLate,genLon