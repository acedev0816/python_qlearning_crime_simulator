# an object of WSGI application 
from flask import Flask, render_template, request
from os import path, walk, remove
import plotly.graph_objects as go
import random
import numpy as np
import pandas as pd
import decimal
import math as Math
import mpu
from random import randint
from random import choice
from flask import send_file
import glob

#insert path
import sys
sys.path.insert(0,'./classes/src')
# user defines
from Simulation import Simulation
from Environment import Environment


app = Flask(__name__)   # Flask constructor 
sim = Simulation()		# create Simulation

# Westminster Co-Ordinates
lat = 51.5101204
lon = -0.1590662

# distance_divide_factor = 100000
distance_divide_factor = 40000

# Some parameters
size_of_the_markers = {
	'offenders': 5,
	'citizens': 5,
	'victims': 5,
	'cameras': 3,
	'campaigns': 12,
	'station':8,
	'park':16
}
colors_of_the_markers = {
	'offenders': 'rgb(255, 0, 0)',
	'citizens': 'rgb(91, 192, 222)',
	'victims': 'rgb(20, 255, 20)',
	'cameras': 'rgb(255, 165, 0)',
	'campaigns': 'rgb(91, 192, 222)',
	'station': 'rgb(55, 47, 225)',
	'park': 'rgb(0, 255, 0)',
}

style = "light"

# in meters
max_effective_distance = {
	'cameras' : 50.0,
	'campaigns' : 200.0
}

night_effectiveness_reduction_factor = 0.6

age_range = (18,50)

gender_type = ('Male', 'Female')

weighted_males_list = [gender_type[0]] * 90 + [gender_type[1]] * 10
weighted_females_list = [gender_type[0]] * 10 + [gender_type[1]] * 90

attackPostion = {
	"lat":[],
	"lon":[]
}

def degrees_to_radians(degrees):
	return degrees * Math.pi

def distance_in_km_between(lat1, lon1, lat2, lon2):
	earth_radius_in_km = 6371

	dLat = degrees_to_radians(lat2-lat1)
	dLon = degrees_to_radians(lon2-lon1)

	lat1 = degrees_to_radians(lat1)
	lat2 = degrees_to_radians(lat2)

	a = Math.sin(dLat/2) * Math.sin(dLat/2) + Math.sin(dLon/2) * Math.sin(dLon/2) * Math.cos(lat1) * Math.cos(lat2)
	c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a))

	distance = earth_radius_in_km * c
	return distance

# A decorator used to tells the application 
# which URL is associated function 
@app.route('/')       
def hello():
    if path.exists('templates/map.html'):
	    remove('templates/map.html')

    clear_previous_simulations()

    return render_template('index.html')

@app.route('/graph')       
def graph():
	days = int(request.args.get('days')) if request.args.get('days') else 0
	attacks = request.args.get('attacks').split(",") if request.args.get('attacks') else []
	x_axis_data = []
	y_axis_data = attacks

	for x in range(1,days):
		x_axis_data.append("Day " + str(x))
	
	fig = go.Figure()
	# Create and style traces
	fig.add_trace(go.Scatter(x=x_axis_data, y=y_axis_data, name='Attacks', line=dict(color='firebrick', width=4)))
	fig.update_layout(title='Effect of Campaigns and Cameras on Attacks', xaxis_title='Days', yaxis_title='Count')
	fig.write_html('templates/graph.html')

	return render_template('graph.html')

@app.route('/clear')
def clear_simulation():
	clear_previous_simulations()
	return {'success':True, 'message' : 'Successfully'}

def clear_previous_simulations():
	attackFiles = glob.glob('templates/attacks-*')
	for file in attackFiles:
			if path.exists(file):
				remove(file)
	sim.clear()
	return True

@app.route('/logo.png')       
def logo():
	return send_file('assets/logo.png', mimetype='image/png')


@app.route('/notify.min.js')       
def notify():
	return send_file('assets/notify.min.js', mimetype='application/javascript')


@app.route('/coordinates')
def coordinates():
	offenders = int(request.args.get('offenders')) if request.args.get('offenders') else 0
	victims = int(request.args.get('victims')) if request.args.get('victims') else 0
	cameras = int(request.args.get('cameras')) if request.args.get('cameras') else 0
	campaigns = int(request.args.get('campaigns')) if request.args.get('campaigns') else 0
	citizens = int(request.args.get('citizens')) if request.args.get('citizens') else 0
	frameDays = int(request.args.get('framedays')) if request.args.get('framedays') else 0
	print("day",frameDays)
	# setting environment
	env = Environment(cameras,campaigns)
	env.setFrameDay(frameDays)
	# setting simulatin
	sim.setEnvironment(env)
	sim.setAttacker(offenders)
	sim.setCitizens(citizens)
	sim.setVictims(victims)



	offenders_co_ordinates = sim.getAttackerPositions()
	victims_co_ordinates = sim.getVictimPositions()
	citizens_co_ordinates = sim.getCitizenPositions()
	cameras_co_ordinates = sim.getCameraPositions()
	campaigns_co_ordinates = sim.getCampaignPositions()
	stations_co_ordinates = sim.getStationPositions()
	parks_co_ordinates = sim.getParkPositions()
	print(parks_co_ordinates)
	data = {
		'offenders' : offenders_co_ordinates,
		'victims' : victims_co_ordinates,
		'cameras' : cameras_co_ordinates,
		'campaigns' : campaigns_co_ordinates,
		'citizens' : citizens_co_ordinates,
		'stations' : stations_co_ordinates,
		'parks' : parks_co_ordinates
	}
	return data
@app.route('/heatmap', methods = ['POST'])
def heatmap():
	json_data = request.get_json(force = True)

	cameras_co_ordinates = json_data['cameras'] if 'cameras' in json_data else {'lats': [], 'lons': []}
	campaigns_co_ordinates = json_data['campaigns'] if 'campaigns' in json_data else {'lats': [], 'lons': []}
	stations_co_ordinates = json_data['stations'] if 'stations' in json_data else {'lats': [], 'lons': []}
	parks_co_ordinates = json_data['parks'] if 'parks' in json_data else {'lats': [], 'lons': []}
	
	whether_night_time = json_data['whether_night_time'] if 'whether_night_time' in json_data else False

	style = 'light'

	if(whether_night_time):
		style = 'dark'

	cameras = len(cameras_co_ordinates['lats'])
	campaigns = len(campaigns_co_ordinates['lats'])
	stations = len(stations_co_ordinates['lats'])
	parks = len(parks_co_ordinates['lats'])


	mapbox_access_token = open(".mapbox_token").read()

	# fig = go.Figure(go.Densitymapbox(
	# 		lat=pd.Series(np.array(stations_co_ordinates['lats'])),
	# 		lon=pd.Series(np.array(stations_co_ordinates['lons'])),
	# 		z= pd.Series(np.array([1]*stations)),
	# 		radius=15))
	# fig.add_trace(
	# 	go.Densitymapbox(
    # 		lat=pd.Series(np.array(parks_co_ordinates['lats'])),
	# 		lon=pd.Series(np.array(parks_co_ordinates['lons'])),
	# 		z= pd.Series(np.array([1]*parks)),
	# 		radius=40))

	print("total attacks: " ,len(attackPostion['lon']))

	print(attackPostion)
	fig = go.Figure()
	fig.add_trace(
		go.Densitymapbox(
    		lat=pd.Series(np.array(attackPostion['lat'])),
			lon=pd.Series(np.array(attackPostion['lon'])),
			z= pd.Series(np.array([1]*(len(attackPostion['lon'])))),
			radius=30))

	# fig.add_trace(
    # 	go.Scattermapbox(
    # 		name="Cameras",
	# 		lat=attackPostion['lat'],
	#         lon=attackPostion['lon'],
	#         mode='markers',
	#         hoverinfo='text',
	#         marker=go.scattermapbox.Marker(
	#             size=size_of_the_markers['offenders'],
	#             color=colors_of_the_markers['offenders'],
	#             opacity=0.7
	#         ),
	#         text=generate_names("Attack", len(attackPostion)),
	#     )
	# )

	# Campaigns to the map
	# fig.add_trace(
    # 	go.Scattermapbox(
    # 		name="Campaigns",
	# 		lat=campaigns_co_ordinates['lats'],
	#         lon=campaigns_co_ordinates['lons'],
	#         mode='markers',
	#         hoverinfo='text',
	#         marker=go.scattermapbox.Marker(
	#             size=size_of_the_markers['campaigns'],
	#             color=colors_of_the_markers['campaigns'],
	#             opacity=0.7
	#         ),
	#         text=generate_names("Campaign", campaigns),
	#     )
	# )

	# Stations to the map
	# fig.add_trace(
    # 	go.Scattermapbox(
    # 		name="Stations",
	# 		lat = stations_co_ordinates['lats'],
	#         lon = stations_co_ordinates['lons'],
	#         mode='markers',
	#         hoverinfo='text',
	#         marker=go.scattermapbox.Marker(
	#             size=size_of_the_markers['station'],
	#             color=colors_of_the_markers['station'],
	#             opacity=0.7
	#         ),
	#         text=generate_names("Station", stations),
	#     )
	# )


	fig.update_layout(
		title="Westminster Crime Simulator",
	    autosize=True,
	    hovermode='closest',
	    showlegend=True,
	    mapbox=go.layout.Mapbox(
	        accesstoken=mapbox_access_token,
	        bearing=0,
	        center=go.layout.mapbox.Center(
	            lat=lat,
	            lon=lon
	        ),
	        pitch=0,
	        zoom=11.5,
		    style=style
	    ),
	)

	fig.write_html('templates/heatmap.html')
	return {
		'status' : True,
		'message' : "Successfully created Map"
	}


@app.route('/generate-map', methods=['POST'])   
def generate_map():
	json_data = request.get_json(force=True)

	offenders_co_ordinates = json_data['offenders'] if 'offenders' in json_data else {'lats': [], 'lons': []}
	citizens_co_ordinates = json_data['citizens'] if 'citizens' in json_data else {'lats': [], 'lons': []}
	victims_co_ordinates = json_data['victims'] if 'victims' in json_data else {'lats': [], 'lons': []}
	cameras_co_ordinates = json_data['cameras'] if 'cameras' in json_data else {'lats': [], 'lons': []}
	campaigns_co_ordinates = json_data['campaigns'] if 'campaigns' in json_data else {'lats': [], 'lons': []}
	stations_co_ordinates = json_data['stations'] if 'stations' in json_data else {'lats': [], 'lons': []}
	parks_co_ordinates = json_data['parks'] if 'parks' in json_data else {'lats': [], 'lons': []}
	
	whether_night_time = json_data['whether_night_time'] if 'whether_night_time' in json_data else False

	style = 'light'

	if(whether_night_time):
		style = 'dark'

	offenders = len(offenders_co_ordinates['lats'])
	citizens = len(citizens_co_ordinates['lats'])
	victims = len(victims_co_ordinates['lats'])
	cameras = len(cameras_co_ordinates['lats'])
	campaigns = len(campaigns_co_ordinates['lats'])
	stations = len(stations_co_ordinates['lats'])
	parks = len(parks_co_ordinates['lats'])

	mapbox_access_token = open(".mapbox_token").read()

	fig = go.Figure()

	fig.add_trace(
		go.Scattermapbox(
			name="Offenders",
			lat=offenders_co_ordinates['lats'],
	        lon=offenders_co_ordinates['lons'],
	        mode='markers',
	        hoverinfo='text',
	        marker=go.scattermapbox.Marker(
	            size=size_of_the_markers['offenders'],
	            color=colors_of_the_markers['offenders'],
	            opacity=0.7
	        ),
	        text=generate_names("Offender", offenders, 'offender'),
	    )
	)

	fig.add_trace(
		go.Scattermapbox(
			name="Citizens",
			lat=citizens_co_ordinates['lats'],
	        lon=citizens_co_ordinates['lons'],
	        mode='markers',
	        hoverinfo='text',
	        marker=go.scattermapbox.Marker(
	            size=size_of_the_markers['citizens'],
	            color=colors_of_the_markers['citizens'],
	            opacity=0.7
	        ),
	        text=generate_names("Citizen", offenders),
	    )
	)

	fig.add_trace(
    	go.Scattermapbox(
    		name="Victims",
			lat=victims_co_ordinates['lats'],
	        lon=victims_co_ordinates['lons'],
	        mode='markers',
	        hoverinfo='text',
	        marker=go.scattermapbox.Marker(
	            size=size_of_the_markers['victims'],
	            color=colors_of_the_markers['victims'],
	            opacity=0.7
	        ),
	        text=generate_names("Victim", victims, 'victim'),
	    )
	)

	# Cameras to the map
	fig.add_trace(
    	go.Scattermapbox(
    		name="Cameras",
			lat=cameras_co_ordinates['lats'],
	        lon=cameras_co_ordinates['lons'],
	        mode='markers',
	        hoverinfo='text',
	        marker=go.scattermapbox.Marker(
	            size=size_of_the_markers['cameras'],
	            color=colors_of_the_markers['cameras'],
	            opacity=0.7
	        ),
	        text=generate_names("Camera", cameras),
	    )
	)

	# Campaigns to the map
	fig.add_trace(
    	go.Scattermapbox(
    		name="Campaigns",
			lat=campaigns_co_ordinates['lats'],
	        lon=campaigns_co_ordinates['lons'],
	        mode='markers',
	        hoverinfo='text',
	        marker=go.scattermapbox.Marker(
	            size=size_of_the_markers['campaigns'],
	            color=colors_of_the_markers['campaigns'],
	            opacity=0.7
	        ),
	        text=generate_names("Campaign", campaigns),
	    )
	)

	# Stations to the map
	fig.add_trace(
    	go.Scattermapbox(
    		name="Stations",
			lat = stations_co_ordinates['lats'],
	        lon = stations_co_ordinates['lons'],
	        mode='markers',
	        hoverinfo='text',
	        marker=go.scattermapbox.Marker(
	            size=size_of_the_markers['station'],
	            color=colors_of_the_markers['station'],
	            opacity=0.7
	        ),
	        text=generate_names("Station", stations),
	    )
	)

	# Parks to the map
	fig.add_trace(
    	go.Scattermapbox(
    		name="Parks",
			lat = parks_co_ordinates['lats'],
	        lon = parks_co_ordinates['lons'],
	        mode='markers',
	        hoverinfo='text',
	        marker=go.scattermapbox.Marker(
	            size=size_of_the_markers['park'],
	            color=colors_of_the_markers['park'],
	            opacity=0.7
	        ),
	        text=generate_names("Park", parks),
	    )
	)

	fig.update_layout(
		title="Westminster Crime Simulator",
	    autosize=True,
	    hovermode='closest',
	    showlegend=True,
	    mapbox=go.layout.Mapbox(
	        accesstoken=mapbox_access_token,
	        bearing=0,
	        center=go.layout.mapbox.Center(
	            lat=lat,
	            lon=lon
	        ),
	        pitch=0,
	        zoom=11.5,
		    style=style
	    ),
	)

	fig.write_html('templates/map.html')
	return {
		'status' : True,
		'message' : "Successfully created Map"
	}


@app.route('/Heat-map')
def heat_map():

	if path.exists('templates/heatmap.html'):
		return render_template('heatmap.html')

	return render_template('westminster.html')

# which URL is associated function 
@app.route('/map')
def map():
	nightmode = request.args.get('night');

	if path.exists('templates/map.html'):
		return render_template('map.html')
	else:
		if nightmode:
			return render_template('westminster-dark.html')

		return render_template('westminster.html')


@app.route('/attacks')
def attacks():
	day = request.args.get('day');
	return render_template('attacks-day-' + day + '.html')

def generate_names(prefix, number, object_type = ''):
	names = []
	for x in range(1,number):
		text = prefix + " " + str(x)
		if object_type == 'victim' or object_type == 'offender':
			text += ", " + get_random_age()
			text += ", " + get_random_gender(object_type)
		
		names.append(text)

	return names

def get_random_age():
	return str(randint(age_range[0], age_range[1]))


def get_random_gender(object_type):
	# Weighted Randomness 
	if(object_type == 'victim'):
		return choice(weighted_females_list)
	
	if(object_type == 'offender'):
		return choice(weighted_males_list)
	



# which URL is associated function 
@app.route('/run', methods=['POST'])
def run_simulation():

	
	json_data = request.get_json(force=True)

	max_effective_distance['campaigns'] = int(json_data['campaigns_effective_distance']) if 'campaigns_effective_distance' in json_data else max_effective_distance['cameras']
	max_effective_distance['cameras'] = int(json_data['cameras_effective_distance']) if 'cameras_effective_distance' in json_data else max_effective_distance['campaigns']
	
	whether_night_time = json_data['whether_night_time'] if 'whether_night_time' in json_data else False
	
	day = json_data['day']

	print("day: ",day)

	style = 'light'

	if(whether_night_time):
		max_effective_distance['campaigns'] = max_effective_distance['campaigns'] * night_effectiveness_reduction_factor
		max_effective_distance['cameras'] = max_effective_distance['cameras'] * night_effectiveness_reduction_factor
		style = 'dark'
	print("type",type(max_effective_distance['cameras']))

	sim.env.setCameraEffective(max_effective_distance['cameras'])
	sim.env.setCampaignEffective(max_effective_distance['campaigns'])

	happened_attacks,attackpositions = sim.runStep()
	mapbox_access_token = open(".mapbox_token").read()

	attackPostion['lat'] = attackPostion['lat'] + happened_attacks['lats']
	attackPostion['lon'] = attackPostion['lon'] + happened_attacks['lons']


	fig = go.Figure()

	fig.add_trace(
		go.Scattermapbox(
			lat=happened_attacks['lats'],
	        lon=happened_attacks['lons'],
	        mode='markers',
	        hoverinfo='text',
	        marker=go.scattermapbox.Marker(
	            size=size_of_the_markers['offenders'],
	            color=colors_of_the_markers['offenders'],
	            opacity=0.7
	        ),
	        text=happened_attacks['texts'],
	    )
	)


	fig.update_layout(
		title="Westminster Crime Simulator",
	    autosize=True,
	    hovermode='closest',
	    showlegend=False,
	    mapbox=go.layout.Mapbox(
	        accesstoken=mapbox_access_token,
	        bearing=0,
	        center=go.layout.mapbox.Center(
	            lat=lat,
	            lon=lon
	        ),
	        pitch=0,
	        zoom=11.5,
	        style=style
	    ),
	)
	print("day: ",day)
	fig.write_html('templates/attacks-day-' + str(day) + '.html')
	return {
		'status' : True,
		'message' : "Successfully created Attack",
		'attacks' : attackpositions,
	}

if __name__=='__main__':
	app.config['TEMPLATES_AUTO_RELOAD'] = True
	app.run(debug=True,use_reloader=True)