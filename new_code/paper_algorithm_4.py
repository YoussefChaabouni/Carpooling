from typing import List
import numpy as np
from new_code.PersonClasses import Rider
from new_code.PersonClasses import Driver
from new_code.graphClasses import Graph , Trajectory
from new_code.meansClasses import Foot
from new_code.paper_algorithm_2 import algorithm_2,walk


def algorithm_4(drivers: List[Driver],rider : Rider,graph : Graph):

	org_r = rider.get_pos_depart
	wd= 0
	wt = 0
	t_prime = rider.get_trajectory().dep_time_list[0] ## departure time from origin

	# --------------- FIRST MILE --------------- #
	t_first = np.Infinity


	for d in drivers:
		'''
		m_dst_d = d.m_dst
		d_trajectory = d.trajectory
		m_dst_r = rider.m_dst
		s_org_r = rider.s_org
		'''
		## rider origin and destination
		r_org = graph.get_node(rider.get_pos_depart)
		r_dst = graph.get_node(rider.get_pos_arrivee)

		## driver origin and destination
		d_org = graph.get_node(d.get_pos_depart)
		d_dst = graph.get_node(d.get_pos_arrivee)

		 
		m_d_org = graph.get_closest_MP(d_org) # closest MP to d's origin
		m_r_org = graph.get_closest_MP(rider.get_pos_depart) # closest MP to r's origin
		s_r_org = graph.get_closest_Station(rider.get_pos_depart) # closest station to r's origin

		if m_d_org == m_r_org and s_r_org in d.get_trajectory.node_list :

			t_chap,w_chap_t,w_chap_d = algorithm_2(rider,d,m_board = m_d_org,m_out = s_r_org) # APPLIQUER L'ALGORITHME 2
			
			

			
			if wd + w_chap_d <= 2500  and  wt + w_chap_t <= 45*60  and  t_chap < t_first: # les longueurs en Mètres et le temps en Secondes

				t_first = t_chap
				wd 	= wd + w_chap_d
				wt		= wt + w_chap_t

				## mis à jour de la trajectoire du rider
				rider.get_trajectory.node_list.append(m_r_org) # ajout du meeting point le plus proche
				rider.get_trajectory.arr_time_list.append(walk(org_r,m_r_org)) ## temps d'arrivée au MP le plus proche
				rider.get_trajectory.dep_time_list.append(w_chap_t)
				rider.get_trajectory.means_list.append(Foot) # il y va à pied





	if t_first == np.Infinity:
		# si ce n'est pas possible d'amener le rider directement à la station, alors cherchons le meeting-point m_prime le plus proche de la station s_org_r qui sera desservit par une voiture 

		for d in drivers:

			m_d_dst = Graph.get_closest_MP(d.get_pos_arrivee) #closest meeting point to driver's destination
			m_prime = Graph.get_closest_MP(s_r_org) ## closest meeting point to the station which is closest to rider origin

			if m_d_dst == m_prime:

				t_chap,w_chap_t,w_chap_d = algorithm_2(rider,d,m_board = m_d_org,m_out = m_prime) # APPLIQUER L'ALGORITHME 2

				if w_chap_d <= 2500  and  w_chap_t <= 45*60  and  t_chap < t_first: # les longueurs en Mètres et le temps en Secondes

					t_first = t_chap
					wd 	= w_chap_d
					wt 	= w_chap_t



	if t_first == np.Infinity:
		# le seul choix du rider est donc de marcher jusqu'à la station la plus proche

		w_chap_d = Graph.get_distance(org_r,s_r_org)

		if w_chap_d < 2500 :

			t_first = t_prime + walk(org_r,s_r_org)
			wd 		= w_chap_d



	if t_first == np.Infinity:
		# le rider ne peut pas atteindre la station s_org_r

		t_prime = np.Infinity

	# --------------- TRAIN --------------- #
	t_prime += 1*60 # admettons qu'une minute est necessaire afin de monter dans le train une fois qu'on a atteint la station

	# increment waiting time by the time the rider waits for the next train after t'
	'''
	On sait qu'on a un train toute les 5 minutes, au lieu de compliquer notre modèle plus on devrait
	simuler un temps d'attente entre 0 et 5 minutes  uniformément
	'''

	# --------------- LAST MILE --------------- #

	t_last = np.Infinity

	for d in drivers:

		m_dst_d = d.m_dst
		d_trajectory = d.trajectory
		m_dst_r = rider.m_dst
		s_dst_r = rider.s_dst

		if m_dst_d == m_dst_r and s_dst_r in d_trajectory :

			t_chap,w_chap_t,w_chap_d = Algo2() # APPLIQUER L'ALGORITHME 2

			if wd + w_chap_d <= 2500  and  wt + w_chap_t <= 45*60  and  t_chap < t_last: # les longueurs en Mètres et le temps en Secondes

				t_last = t_chap
				wd 		= wd + w_chap_d
				wt 		= wt + w_chap_t



	if t_last > np.Infinity:
		# si ce n'est pas possible d'amener le rider directement à la station, alors cherchons le meeting-point m_prime le plus proche de la station s_dst_r qui sera desservit par une voiture 

		for d in drivers:

			m_dst_d = d.m_dst_d
			rider.s_dst_r = s_dst_r

			if m_dst_d == m_prime:

				t_chap,w_chap_t,w_chap_d = Algo2() # APPLIQUER L'ALGORITHME 2

				if w_chap_d <= 2500  and  w_chap_t <= 45*60  and  t_chap < t_last: # les longueurs en Mètres et le temps en Secondes

					t_last = t_chap
					wd 		= w_chap_d
					wt 		= w_chap_t



	if t_last > np.Infinity:
		# le seul choix du rider est donc de marcher jusqu'à la station la plus proche

		w_chap_d = distance(dst_r,s_dst_r)

		if w_chap_d < 2500 :

			t_last = t_prime + walk(dst_r,s_dst_r)
			wd 		= w_chap_d



	if t_last > np.Infinity:
		# le rider ne peut pas atteindre la station s_dst_r

		t_prime = np.Infinity	


	return 0


