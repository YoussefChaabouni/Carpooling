import numpy as np

from PersonClasses import Driver
from graphClasses import Graph
from helperFunctions import Drive

def algorithm_1(d : Driver, graph : Graph):

	"""
	Inputs :
		d : Driver that accomplishes the journey
		graph : the graph of the simulation
	Outputs :
		J_d : trajectory
	"""

	MAX_DETOUR_PERCENTAGE = 1.15
	
	t = d.get_born_time()
	# prendre les nodes d'arrivée et de départ
	org_d = graph.get_node(d.pos_depart)
	dst_d = graph.get_node(d.pos_arrivee)

	# prendre les meeting points les plus proches
	m_org_d = graph.get_closest_MP_or_Station(org_d,"MPs")
	m_dst_d = graph.get_closest_MP_or_Station(dst_d,"MPs")
	# prendre les stations les plus proches
	s_org_d = graph.get_closest_MP_or_Station(org_d,"Stations")
	s_dst_d = graph.get_closest_MP_or_Station(dst_d,"Stations")

	J_d = [org_d, m_org_d, m_dst_d, dst_d]

	# mettre à jour la trajectoire du driver
	# on assume que le driver ne perd pas de temps entre les nodes ?? on peut ajouter un délai
	delai = 1 # on suppose un délai d'une minute
	arrival_time_m_org_d = t + Drive(org_d,m_org_d,graph,d.speed) ## arrivée à m_org_d
	departure_time_m_org_d = arrival_time_m_org_d + delai # départ de m_org_d	
	d.get_trajectory().update_trajectory(d,arrival_time_m_org_d,departure_time_m_org_d,m_org_d.get_id())
	
	r = np.random.randint(2)

	if r:
		# Try to add a detour close to the origin
		if  graph.get_distance(m_org_d,s_org_d) + graph.get_distance(s_org_d,m_dst_d) <= MAX_DETOUR_PERCENTAGE * graph.get_distance(m_org_d,m_dst_d):
			# Add a detour through station s_org_d
			J_d = [org_d, m_org_d, s_org_d, m_dst_d, dst_d]
			

			# ajouter s_org_d à trajectory
			arrival_time_s_org_d = departure_time_m_org_d + Drive(m_org_d,s_org_d,graph,d.speed) ## arrivée à s_org_d
			departure_time_s_org_d = arrival_time_m_org_d + delai # départ de s_org_d	
			d.get_trajectory().update_trajectory(d,arrival_time_s_org_d,departure_time_s_org_d,s_org_d.get_id())	


			if graph.get_distance(m_org_d,s_org_d) + graph.get_distance(s_org_d,s_dst_d) + graph.get_distance(s_org_d,m_dst_d) <= MAX_DETOUR_PERCENTAGE * graph.get_distance(m_org_d,m_dst_d):
				# Also add a detour through the station close to the driver destination
				J_d = [org_d, m_org_d, s_org_d, s_dst_d, m_dst_d, dst_d]

				# ajouter s_dst_d à trajectory
				arrival_time_s_dst_d = departure_time_s_org_d + Drive(s_org_d,s_dst_d,graph,d.speed) ## arrivée à s_dst_d
				departure_time_s_dst_d = arrival_time_m_org_d + delai # départ de s_dst_d	
				d.get_trajectory().update_trajectory(d,arrival_time_s_dst_d,departure_time_s_dst_d,s_dst_d.get_id())
	
	else:
		# Try to add a detour close to the destination
		if  graph.get_distance(m_org_d,s_dst_d) + graph.get_distance(s_dst_d,m_dst_d) <= MAX_DETOUR_PERCENTAGE * graph.get_distance(m_org_d,m_dst_d):
			# Add a detour through station s_dst_d
			J_d = [org_d, m_org_d, s_dst_d, m_dst_d, dst_d]

			# ajouter s_dst_d à trajectory
			arrival_time_s_dst_d = departure_time_m_org_d + Drive(m_org_d,s_dst_d,graph,d.speed) ## arrivée à s_dst_d
			departure_time_s_dst_d = arrival_time_m_org_d + delai # départ de s_dst_d	
			d.get_trajectory().update_trajectory(d,arrival_time_s_dst_d,departure_time_s_dst_d,s_dst_d.get_id())


			if graph.get_distance(m_org_d,s_org_d) + graph.get_distance(s_org_d,s_dst_d) + graph.get_distance(s_org_d,m_dst_d) <= MAX_DETOUR_PERCENTAGE * graph.get_distance(m_org_d,m_dst_d):
				# Also add a detour through the station close to the driver origin
				J_d = [org_d, m_org_d, s_org_d, s_dst_d, m_dst_d, dst_d]

				# ajouter m_dst_d à trajectory
				arrival_time_m_dst_d = departure_time_s_dst_d + Drive(s_dst_d,m_dst_d,graph,d.speed) ## arrivée à m_dst_d
				departure_time_m_dst_d = arrival_time_m_dst_d + delai # départ de m_dst_d	
				d.get_trajectory().update_trajectory(d,arrival_time_m_dst_d,departure_time_m_dst_d,m_dst_d.get_id())


	d.set_current_capacity([4]*len(J_d))
	return J_d

