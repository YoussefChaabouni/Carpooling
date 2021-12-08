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
	#print(" class of d_org in alg1 = ",type(org_d))
	dst_d = graph.get_node(d.pos_arrivee)

	# prendre les meeting points les plus proches
	m_org_d = graph.get_closest_MP_or_Station(org_d,"MPs")
	m_dst_d = graph.get_closest_MP_or_Station(dst_d,"MPs")
	# prendre les stations les plus proches
	s_org_d = graph.get_closest_MP_or_Station(org_d,"Stations")
	s_dst_d = graph.get_closest_MP_or_Station(dst_d,"Stations")

	J_d = [org_d, m_org_d, m_dst_d, dst_d]

	arrival_time =0
	departure_time =0
	# mettre à jour la trajectoire du driver
	# on assume que le driver ne perd pas de temps entre les nodes ?? on peut ajouter un délai
	delai = 1 # on suppose un délai d'une minute
	arrival_time = t + Drive(org_d,m_org_d,graph,d.speed) ## arrivée à m_org_d
	departure_time = arrival_time+ delai # départ de m_org_d	
	d.get_trajectory().update_trajectory(d,arrival_time,departure_time,m_org_d.get_id())
	
	r = np.random.randint(2)

	# vérifier si la destination n'est pas le mp_org le plus proche
	if m_org_d == dst_d :
		J_d = [org_d,dst_d]
		
	else:
		if r == 1:
			# Try to add a detour close to the origin
			if  graph.get_distance(m_org_d,s_org_d) + graph.get_distance(s_org_d,m_dst_d) <= MAX_DETOUR_PERCENTAGE * graph.get_distance(m_org_d,m_dst_d):
				print("detour to s_org_d")
				# Add a detour through station s_org_d
				J_d = [org_d, m_org_d, s_org_d, m_dst_d, dst_d]
				
				#__________________________
				print("driver went from m_org_d to s_org_d in : ",Drive(m_org_d,s_org_d,graph,d.speed))


				# ajouter s_org_d à trajectory
				arrival_time = departure_time + Drive(m_org_d,s_org_d,graph,d.speed) ## arrivée à s_org_d
				departure_time = arrival_time + delai # départ de s_org_d	
				d.get_trajectory().update_trajectory(d,arrival_time,departure_time,s_org_d.get_id())	


				if graph.get_distance(m_org_d,s_org_d) + graph.get_distance(s_org_d,s_dst_d) + graph.get_distance(s_org_d,m_dst_d) <= MAX_DETOUR_PERCENTAGE * graph.get_distance(m_org_d,m_dst_d) and s_org_d.get_id() != s_dst_d.get_id():
					# Also add a detour through the station close to the driver destination
					J_d = [org_d, m_org_d, s_org_d, s_dst_d, m_dst_d, dst_d]

					# ajouter s_dst_d à trajectory
					arrival_time = departure_time + Drive(s_org_d,s_dst_d,graph,d.speed) ## arrivée à s_dst_d
					departure_time = arrival_time + delai # départ de s_dst_d	
					d.get_trajectory().update_trajectory(d,arrival_time,departure_time,s_dst_d.get_id())
		
		else:
			# Try to add a detour close to the destination
			if  graph.get_distance(m_org_d,s_dst_d) + graph.get_distance(s_dst_d,m_dst_d) <= MAX_DETOUR_PERCENTAGE * graph.get_distance(m_org_d,m_dst_d):
				# Add a detour through station s_dst_d
				J_d = [org_d, m_org_d, s_dst_d, m_dst_d, dst_d]

				# ajouter s_dst_d à trajectory
				arrival_time= departure_time + Drive(m_org_d,s_dst_d,graph,d.speed) ## arrivée à s_dst_d
				departure_time = arrival_time + delai # départ de s_dst_d	
				d.get_trajectory().update_trajectory(d,arrival_time,departure_time,s_dst_d.get_id())


				if graph.get_distance(m_org_d,s_org_d) + graph.get_distance(s_org_d,s_dst_d) + graph.get_distance(s_org_d,m_dst_d) <= MAX_DETOUR_PERCENTAGE * graph.get_distance(m_org_d,m_dst_d) and s_org_d.get_id() != s_dst_d.get_id():
					# Also add a detour through the station close to the driver origin
					J_d = [org_d, m_org_d, s_org_d, s_dst_d, m_dst_d, dst_d]

					# ajouter m_dst_d à trajectory
					arrival_time= departure_time + Drive(s_dst_d,s_org_d,graph,d.speed) ## arrivée à m_dst_d
					departure_time = arrival_time + delai # départ de m_dst_d	
					d.get_trajectory().update_trajectory(d,arrival_time,departure_time,s_org_d.get_id())

		#------------------------
		if m_dst_d != m_org_d :
			# ajout du meeting point le plus proche de la destination
			arrival_time = departure_time + Drive(J_d[len(J_d)-3],m_dst_d,graph,d.speed)
			departure_time = arrival_time
			d.get_trajectory().update_trajectory(d,arrival_time,departure_time,m_dst_d.get_id())

		# ajout de la destination
		arrival_time = departure_time + Drive(J_d[len(J_d)-2],dst_d,graph,d.speed)
		departure_time = arrival_time 
		d.get_trajectory().update_trajectory(d,arrival_time,departure_time,dst_d.get_id())

		d.set_current_capacity([4]*len(J_d))
	return J_d

