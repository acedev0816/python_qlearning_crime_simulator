from Common import *
from Camera import Camera
from Campaign import Campaign
from Station import Station
from Park import Park
stations = [{"name": "Baker Street", "lat": 51.52313, "lon": -0.156904},
			{"name": "Bayswater", "lat" : 51.512111, "lon": -0.187902},
			{"name": "Bond Street","lat": 51.513798, "lon":	-0.149614},
			{"name": "Charing Cross","lat": 51.508359, "lon":-0.124803},		
			{"name": "Covent Garden","lat": 51.51276, "lon":-0.124507},	
			{"name": "Edgware Road (bakerloo line)","lat": 51.520645, "lon":-0.17054},
			{"name": "Edgware Road (Cicle, district, h&c line)","lat": 51.519998, "lon":-0.167668},	
			{"name": "Embankment","lat": 51.507312, "lon":	-0.122367}, 		
			{"name": "Great Portland Street","lat": 51.523789, "lon":	-0.143961},
			{"name": "Green Park","lat": 51.50676, "lon":	-0.142478},
			{"name": "Hyde Park Corner","lat": 51.502584, "lon":	-0.152474},	
			{"name": "Lancaster Gate","lat": 51.511891, "lon":	-0.17543},
			{"name": "Leicester Square","lat": 51.511291, "lon":	-0.128242},
			{"name": "London Victoria","lat": 51.496424, "lon":	-0.143921},
			{"name": "Maida Vale","lat": 51.529995, "lon":	-0.185433},
			{"name": "Marble Arch","lat": 51.513965, "lon":	-0.158571},
			{"name": "Marylebone","lat": 51.522397, "lon":	-0.163493},	
			{"name": "Oxford Circus","lat": 51.515223, "lon":	-0.140836},	
			{"name": "Paddington underground","lat": 51.515394, "lon":	-0.175737},
			{"name": "Paddington station","lat": 51.517128, "lon":	-0.176933},
			{"name": "Piccadilly Circus","lat": 51.509697, "lon":	-0.133712},
			{"name": "Pimlico","lat": 51.489553, "lon":	-0.133108},
			{"name": "Queensway","lat": 51.510449, "lon":	-0.18742},
			{"name": "Regent’s Park","lat": 51.523811, "lon":	-0.145344},
			{"name": "Royal Oak","lat": 51.518294, "lon":	-0.188824},	
			{"name": "St. James’s Park","lat": 51.49961, "lon":	-0.133879}, 
			{"name": "St. John’s Wood","lat": 51.534854, "lon":	-0.174065},	
			{"name": "Tottenham Court Road","lat": 51.516211, "lon":-0.13111},
			{"name": "Warwick Avenue","lat": 51.523104, "lon":-0.182953},
			{"name": "Westbourne Park","lat": 51.520989, "lon":	-0.200883},
			{"name": "Westminster","lat": 51.501402, "lon":	-0.125002}]

parks = [{"name":"Kensington gardens","lat":51.507110,"lon":-0.178906,"radius":1},
	{"name":"Hyde park","lat":51.507362,"lon":-0.165838,"radius":1.2},
	{"name":"Green Park","lat":51.504084,"lon":-0.143943,"radius":0.4},
	{"name":"St. James Park","lat":51.502640,"lon":-0.134854,"radius":0.45}]


class Environment:
	"""Environment class is ..."""
	def __init__(self, num_camera = 0, num_campaign = 0, camera_effective = 50, campaign_effective = 200):

		self.num_camera = num_camera
		self.num_campaign = num_campaign
		self.camera_effective = camera_effective
		self.campaign_effective = campaign_effective
		self.frameDays = 1
		self.cameras = []
		self.campaigns = []
		self.stations = []
		self.parks = []

		for station_data in stations: 
			name = station_data['name']
			lat = station_data['lat']
			lon = station_data['lon']

			station = Station(lat,lon,500,name)
			self.stations.append(station)
		for park_data in parks: 
			name = park_data['name']
			lat = park_data['lat']
			lon = park_data['lon']
			radius = park_data['radius']

			park = Park(lat,lon,radius,name)
			self.parks.append(park)

		self.setCameras(num_camera, camera_effective)
		self.setCampaigns(num_campaign, campaign_effective)

	def IsCampaignArea(self, lat, lon):
		for campaign in self.campaigns:
			campaign_lat, campaign_lon = campaign.getPosition()
			distance = distance_in_km_between(lat,lon,campaign_lat,campaign_lon)
			if distance*1000 < float(self.campaign_effective):
				return True
		return False

	def IsRiskArea(self, lat, lon):



		for camera in self.cameras:
			camera_lat, camera_lon = camera.getPosition()
			distance = distance_in_km_between(lat,lon,camera_lat,camera_lon)
			if distance*1000 < float(self.camera_effective):
				return False
		if self.IsStationArea(lat,lon) or self.IsParkArea(lat,lon):
			return True
		return True

	def IsCameraImpact(self, lat, lon):

		for camera in self.cameras:
			camera_lat, camera_lon = camera.getPosition()
			distance = distance_in_km_between(lat,lon,camera_lat,camera_lon)
			if distance*1000 < 0.05:
				return True
		return False
	def IsStationArea(self,lat,lon):
		for staton in self.stations:
			station_lat,staton_lon = staton.getPosition()
			distance = distance_in_km_between(lat,lon,station_lat,staton_lon)
			if distance < 0.5:
				return True
		return False
	def IsParkArea(self,lat,lon):
		for park in self.parks:
			park_lat,park_lon = park.getPosition()
			distance = distance_in_km_between(lat,lon,park_lat,park_lon)
			if distance < park.getRadius():
				return True
		return False

	def setCameras(self, numCamera, camera_effective):

		self.camera_effective = float(camera_effective)
		for x in range(0,int(numCamera)):
			lat, lon = generateRandomPosition()
			while not (self.IsStationArea(lat,lon) or self.IsStationArea(lat,lon)) :
				lat, lon = generateRandomPosition()

			camera = Camera(lat,lon,camera_effective)
			self.cameras.append(camera)

	def setCampaigns(self, numCampaign, campaign_effective):

		self.campaign_effective =  float(campaign_effective)
		for x in range(0,int(numCampaign)):
			lat, lon = generateRandomPosition()
			campaign = Campaign(lat,lon,campaign_effective)
			self.campaigns.append(campaign)
	def setFrameDay(self,days):
		self.frameDays = days

	def clear(self):
		self.camera_effective = 50
		self.campaign_effective = 200
		self.cameras.clear()
		self.campaigns.clear()
	
	def setCameraEffective(self,cameraEffective):
		self.camera_effective = cameraEffective
		for camera in self.cameras:
			camera.setEffective(cameraEffective)
		
	def setCampaignEffective(self,campaignEffective):
		self.campaign_effective = float(campaignEffective)
		for campaign in self.campaigns:
			campaign.setEffective(campaignEffective)
