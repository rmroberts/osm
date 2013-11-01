"""
Rebecca Roberts
Description:
	This program reads an OSM file and creates 
	three routable data files.
"""

import time
from math import radians, cos, sin, asin, sqrt
t = time.clock()
fin = open('/usr/share/grenada.osm')
nodesoutput = open('Nodes.txt', 'w')
edgesoutput = open('Edges.txt', 'w')
edgegeomoutput = open('EdgeGeometry.txt', 'w')
Nodes = {}
way_flag = 0
tag_flag = 0
length = 0
maxspeed = 30
count=0

#takes two points and determines the great circle distance between
#them using the haversine formula, returns distance in meters
def haversine(lon1,lat1,lon2,lat2):
	radius = 6378100	#radius of earth in meters
	#convert decimal degrees to radians 
	lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
	dlat = lat2-lat1
	dlon = lon2-lon1
	a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
	c = 2 * asin(sqrt(a))
	d = radius * c
	return d

for line in fin:
	line = line.strip()
	if line.startswith('<relation'):		#only read relevant part of file
		break
	ind1 = line.find('<node id="')
	if ind1 != -1:							#if line contains a node id ...
		nodeid = line[ind1+10:line.find('"',ind1+11)]
		ind2 = line.find('lat="')				#find node id, lat, and lon
		lat = line[ind2+5:line.find('"',ind2+6)]
		ind3 = line.find('lon="')
		lon = line[ind3+5:line.find('"',ind3+6)]
		Nodes[nodeid] = lat,lon				#dictionary of nodes, used later to look up lat/lon for nodes in way
	if line.startswith('<way'):				#the beginning of a way
		E = {}							#dictionary will contain EdgeID, Nodes in the way,
		i1 = line.find('<way id="')		#Name, and Type for one way, then is reset for each 
		edgeid = line[i1+9:line.find('"',i1+10)]	#way after results are printed.  So E only contains info
		E['EdgeID'] = edgeid						#for a single way, is reset for each one
		E['Nodes'] = []
		way_flag = 1
		length = 0
		maxspeed = 30	#default value
	elif line.startswith('</way'):			#the end of a way
		if not 'Name' in E:		#Name and Type will be empty strings if 
			E['Name'] = ''		#there are no values in the file
		if not 'Type' in E:
			E['Type'] = ''
		edgegeomoutput.write(E['EdgeID']+'^'+E['Name']+'^'+E['Type'])
		index = E['Nodes'][0]
		if index in Nodes:			#if the nd ref from a way does not correspond to a node id
			prevlat,prevlon = Nodes[index]		#then it is ignored.
			count = 1
		else:
			for i in E['Nodes'][1:]:
				count += 1
				if i in Nodes:
					prevlat,prevlon = Nodes[i]
		for j in E['Nodes'][count:]:
			if j in Nodes:						#accumulates length between every two lon/lat pairs
				latitude,longitude = Nodes[j]
				length += haversine(float(prevlon),float(prevlat),float(longitude),float(latitude))
				prevlat,prevlon = latitude,longitude
		length = round(length,2)
		edgegeomoutput.write('^'+str(length))
		for j in E['Nodes']:
			if j in Nodes:						#prints lat/lon for nodes in way
				latitude,longitude = Nodes[j]
				nodesoutput.write(j+' '+latitude+' '+longitude+'\n')
				edgegeomoutput.write('^'+latitude+'^'+longitude)	
		edgegeomoutput.write('\n')
		maxspeed = maxspeed * (1609.34/3600)	#convert from miles/hr to m/s
		cost = length / maxspeed				#seconds to traverse length
		cost = round(cost,2)
		edgesoutput.write(E['EdgeID']+' '+E['Nodes'][0]+' '+E['Nodes'][-1]+' '+str(cost)+'\n')
		way_flag = 0
		tag_flag = 0
	if way_flag == 1 and line.startswith('<nd ref'):
		i2 = line.find('<nd ref="')
		noderef = line[i2+9:line.find('"',i2+10)]
		E['Nodes'].append(noderef)					#list of ids of nodes in way
	elif way_flag == 1 and line.startswith('<tag k="name"'):
		i3 = line.find('<tag k="name" v="')
		name = line[i3+17:line.find('"',i3+18)]
		E['Name'] = name
	elif way_flag == 1 and tag_flag == 0 and line.startswith('<tag k="'):
		i4 = line.find('v="')
		type = line[i4+3:line.find('"',i4+4)]
		if type != 'no' and type != 'yes':
			E['Type'] = type
			tag_flag = 1
		elif type == 'yes':
			i5 = line.find('<tag k="')
			type = line[i5+8:line.find('"',i5+9)]
			E['Type'] = type
			tag_flag = 1
		i6 = line.find('<tag k="maxspeed" v="')
		if i6 != -1:
			maxspeed = line[i6+21,line.find('"',i6+22)]
		elif type == 'motorway':
			maxspeed = 65
		elif type == 'trunk' or type == 'primary' or type == 'secondary':
			maxspeed = 55
		elif type == 'tertiary' or type == 'unclassified':
			maxspeed = 45
		elif type == 'service':
			maxspeed = 15
		else:
			maxspeed = 30
Nodes.clear()
fin.close()
nodesoutput.close()
edgesoutput.close()
edgegeomoutput.close()
t = time.clock()
print t