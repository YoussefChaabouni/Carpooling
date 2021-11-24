from typing import List
import numpy as np
from new_code.PersonClasses import Rider
from new_code.PersonClasses import Driver
from new_code.graphClasses import Graph , Trajectory
from new_code.meansClasses import Foot
from new_code.paper_algorithm_2 import algorithm_2
from helperFunctions import walk, Drive, board_train
import random



def algorithm_4(drivers: List[Driver],rider : Rider,graph : Graph):

	org_r = rider.get_pos_depart
	wd= 0
	wt = 0
	t_prime = rider.get_trajectory().dep_time_list[0] ## departure time from origin

	##---------------------------NEXT TRAIN----------------------------------------------
	'''
	on veut pouvoir obtenir le prochain train à chaque fois pour calculer la durée d'attente du rider dans le quai
	une solution temporaire serait de mettre une variable aléatoire entre 0 et 5 minutes pour le temps d'attente
	une solution finale serait d'avoir une liste de tous les instants d'arrivée du train dans la station 
	'''
	next_train_waiting_time = random.randint(6)


		## rider origin and destination
	r_org = graph.get_node(rider.get_pos_depart)
	r_dst = graph.get_node(rider.get_pos_arrivee)

		
	
	m_r_org = graph.get_closest_MP_or_Station(r_org,"MPs") # closest MP to r's origin
	s_r_org = graph.get_closest_MP_or_Station(r_org,"Stations") # closest station to r's origin
	# --------------- FIRST MILE --------------- #
	t_first = np.Infinity


	for d in drivers:
		
		## driver origin and destination
		d_org = graph.get_node(d.get_pos_depart)
		d_dst = graph.get_node(d.get_pos_arrivee)
		m_d_org = graph.get_closest_MP_or_Station(d_org,"MPs") # closest MP to d's origin

		if m_d_org == m_r_org and s_r_org.get_id in d.get_trajectory.node_id_list :

			t_chap,w_chap_t,w_chap_d = algorithm_2(z = r_org,z_prime = s_r_org,t = t_prime,d=d,m = m_d_org,m_prime = s_r_org) # APPLIQUER L'ALGORITHME 2
			
			

			
			if wd + w_chap_d <= 2500  and  wt + w_chap_t <= 45*60  and  t_chap < t_first: # les longueurs en Mètres et le temps en Secondes

				t_first = t_chap
				wd 	= wd + w_chap_d
				wt		= wt + w_chap_t

				## mise à jour de la trajectoire du rider
				## new_mean : Mean_of_transportation,new_arr_time,new_dep_time,new_node_id : int
				## on ajoute les temps d'arrivée et de départ de chaque node parcourue
				'''
					le rider va :
					- marcher jusqu'à m_d_org
					- prendre la voiture jusqu'à s_r_org
				'''
				arrival_time_mp = t_prime + walk(r_org,m_d_org) # arrivée à m_r_org
				departure_time_mp = arrival_time_mp + w_chap_t #départ de m_r_org
				arrival_time_station = t_chap + 1 #arrivée à la plateforme de s_r_org
				departure_time_station = arrival_time_station + next_train_waiting_time	


				rider.get_trajectory.update_trajectory(Foot(),arrival_time_mp,departure_time_mp,m_d_org.get_id) # ajouter m_d_org node à trajectory
				rider.get_trajectory.update_trajectory(d,arrival_time_station,departure_time_station,s_r_org.get_id) # ajouter s_r_org à trajectory
				






	if t_first == np.Infinity:
		# si ce n'est pas possible d'amener le rider directement à la station, alors cherchons le meeting-point m_prime le plus proche de la station s_org_r qui sera desservit par une voiture 

		for d in drivers:
			'''
			m_d_dst = Graph.get_closest_MP(d.get_pos_arrivee) #closest meeting point to driver's destination
			m_prime = Graph.get_closest_MP(s_r_org) ## closest meeting point to the station which is closest to rider origin
			'''
			m_d_dst = graph.get_closest_MP_or_Station(d_dst,"MPs") # closest MP to d's destination
			m_prime = graph.get_closest_MP_or_Station(s_r_org,"MPs") # closest MP to r's closest station to origin

			if m_d_dst == m_prime:

				t_chap,w_chap_t,w_chap_d = algorithm_2(z = r_org,z_prime = s_r_org,t = t_prime,d=d,m = m_d_org,m_prime = m_prime) # APPLIQUER L'ALGORITHME 2

				if w_chap_d <= 2500  and  w_chap_t <= 45*60  and  t_chap < t_first: # les longueurs en Mètres et le temps en Secondes

					t_first = t_chap
					wd 	= w_chap_d
					wt 	= w_chap_t

					## mise à jour de la trajectoire du rider
					## new_mean : Mean_of_transportation,new_arr_time,new_dep_time,new_node_id : int
					## on ajoute les temps d'arrivée et de départ de chaque node parcourue
					'''
					le rider va :
					- marcher jusqu'à m_d_org
					- prendre la voiture jusqu'à m_prime
					- marcher jusqu'à s_r_org
					'''
					arrival_time_mp = t_prime + walk(r_org,m_d_org) # arrivée à m_d_org
					departure_time_mp = arrival_time_mp + w_chap_t #départ de m_r_org
					arrival_time_m_prime = t_chap # arrivée à m_prime
					departure_time_m_prime = t_chap # départ de m_prime
					arrival_time_station = t_chap + walk(m_prime,s_r_org) + 1 #arrivée à la plateforme de s_r_org
					departure_time_station = arrival_time_station + next_train_waiting_time	# départ de s_r_org


					rider.get_trajectory.update_trajectory(Foot(),arrival_time_mp,departure_time_mp,m_d_org.get_id) # ajouter m_d_org node à trajectory de r
					rider.get_trajectory.update_trajectory(d,arrival_time_m_prime,departure_time_m_prime,m_prime.get_id) # ajouter m_prime à trajectory de r
					rider.get_trajectory.update_trajectory(Foot(),arrival_time_station,departure_time_station,s_r_org.get_id) # ajouter s_r_org à trajectory de r
				


	if t_first == np.Infinity:
		# le seul choix du rider est donc de marcher jusqu'à la station la plus proche

		w_chap_d = Graph.get_distance(org_r,s_r_org)

		if w_chap_d < 2500 :

			t_first = t_prime + walk(org_r,s_r_org)
			wd 		= w_chap_d

			## mise à jour de la trajectoire du rider
			## new_mean : Mean_of_transportation,new_arr_time,new_dep_time,new_node_id : int
			## on ajoute les temps d'arrivée et de départ de chaque node parcourue
			'''
			le rider va :
			- marcher jusqu'à s_r_org
			'''
			
			arrival_time_station = t_prime + walk(r_org,s_r_org) + 1 #arrivée à la plateforme de s_r_org
			departure_time_station = arrival_time_station + next_train_waiting_time	# départ de s_r_org


			rider.get_trajectory.update_trajectory(Foot(),arrival_time_station,departure_time_station,s_r_org.get_id) # ajouter s_r_org à trajectory de r
				




	if t_first == np.Infinity:
		# le rider ne peut pas atteindre la station s_org_r

		t_prime = np.Infinity

	# --------------- TRAIN --------------- #
	t_prime = t_first # mettre la durée du first mile dans t_prime
	t_prime += 1*60 # admettons qu'une minute est necessaire afin d'atteindre la plateforme

	# --------------------------- ajouter le train à trajectory de r -----------------------
	s_r_dest = graph.get_closest_MP_or_Station(r_org,"Stations")


	arrival_time_dest_station = departure_time_station + board_train(s_r_org,s_r_dest) # temps d'arrivée à s_r_dest
	departure_time_dest_station = arrival_time_dest_station + 1 # temps de départ de s_r_dest
	rider.get_trajectory.update_trajectory(d,arrival_time_dest_station,departure_time_dest_station,new_node_id = s_r_dest.get_id)


	# ------------------------incrémenter le temps d'attente et t_prime---------------------------
	wt += next_train_waiting_time
	t_prime = departure_time_dest_station


	# ------------------------ LAST MILE ------------------------------- #

	t_last = np.Infinity


	m_r_dest = graph.get_closest_MP_or_Station(r_dst,"MPs") # closest meeting point to r_dest
	m_d_dest = graph.get_closest_MP_or_Station(d_dst,"MPs") # closest meeting point to d_dest


	##----------------- RIDER GETS PICKED UP DIRECTLY FROM THE STATION -------------------------------------------
	for d in drivers:
		if m_d_dest == m_r_dest and s_r_dest.get_id in d.get_trajectory.node_id_list :

			t_chap,w_chap_t,w_chap_d = algorithm_2(s_r_dest, r_dst,t_prime,d,m = s_r_dest,m_prime = m_d_dest)
			if wd + w_chap_d < 2500 and wt+ w_chap_t <45*60 and t_chap<t_last:
			
				# mettre à jour t_last wd et wt
				t_last = t_chap
				wd += w_chap_d
				wt += w_chap_t

				## mise à jour de la trajectoire du rider
				## new_mean : Mean_of_transportation,new_arr_time,new_dep_time,new_node_id : int
				## on ajoute les temps d'arrivée et de départ de chaque node parcourue
				'''
				le rider va :
				- prendre une voiture depuis s_r_org jusqu'à m_r_dest
				- marcher jusqu'à r_dst
				'''
				
				arrival_time_m_r_dest = t_chap
				departure_time_m_r_dest = t_chap
				arrival_time_dst = departure_time_m_r_dest + walk(m_d_dest,r_dst)
				departure_time_dst = arrival_time_dst

				rider.get_trajectory.update_trajectory(d,arrival_time_m_r_dest,departure_time_m_r_dest,m_d_dest.get_id) # ajouter m_r_dest à trajectory
				rider.get_trajectory.update_trajectory(Foot(),arrival_time_dst,departure_time_dst,r_dst.get_id) # ajouter r_dst à trajectory de r
							
##--------------- RIDER HAS TO WALK TO A MEETING POINT IN LAST MILE-----------------------------------------
	if t_last == np.Infinity:

		m_seconde = graph.get_closest_MP_or_Station(s_r_dest,"Stations") # meeting point le plus proche de s_r_dest
		for d in drivers:
			'''
			m_dst_d = d.m_dst
			d_trajectory = d.trajectory
			m_dst_r = rider.m_dst
			s_dst_r = rider.s_dst
			'''
			

			if m_d_dest == m_r_dest and s_r_dest.get_id in d.get_trajectory.node_id_list :

				t_chap,w_chap_t,w_chap_d = algorithm_2(z = s_r_dest,z_prime = m_r_dest,t = t_prime,d=d,m = m_seconde,m_prime = m_d_dst) # APPLIQUER L'ALGORITHME 2

				if wd + w_chap_d <= 2500  and  wt + w_chap_t <= 45*60  and  t_chap < t_last: # les longueurs en Mètres et le temps en Secondes

					t_last = t_chap
					wd 		= wd + w_chap_d
					wt 		= wt + w_chap_t

					
					## mise à jour de la trajectoire du rider
					## new_mean : Mean_of_transportation,new_arr_time,new_dep_time,new_node_id : int
					## on ajoute les temps d'arrivée et de départ de chaque node parcourue
					'''
					le rider va :
					- marcher de s_r_dest jusqu'à m_seconde
					- prendre une voiture de m_seconde à m_r_dest
					- marcher jusqu'à r_dst
					
					'''
					
					arrival_time_m_seconde = t_prime + walk(r_org,s_r_org) # arrivée en m_seconde
					departure_time_m_seconde = arrival_time_m_seconde + wt	# départ de m_seconde
					arrival_time_m_r_dest = departure_time_m_seconde + Drive(m_seconde,s_r_dest) # arrivée en m_r_dest
					departure_time_m_r_dest = departure_time_m_r_dest # départ de m_r_dest
					arrival_time_r_dst = departure_time_m_r_dest + walk(m_r_dest,r_dst) # arrivée en r_dest
					departure_time_r_dst = arrival_time_r_dst # départ de r_dest

					rider.get_trajectory.update_trajectory(Foot(),arrival_time_m_seconde,departure_time_m_seconde,m_seconde.get_id) # ajouter m_seconde à trajectory de r
					rider.get_trajectory.update_trajectory(d,arrival_time_m_r_dest,departure_time_m_r_dest,m_r_dest.get_id) # ajouter m_r_dst à trajectory de r
					rider.get_trajectory.update_trajectory(Foot(),arrival_time_r_dst,departure_time_r_dst,r_dst.get_id)  # ajouter m_dst à trajectory de r

	if t_last > np.Infinity:
		# le seul choix du rider est donc de marcher jusqu'à la station la plus proche

		w_chap_d = walk(s_r_dest,r_dst)

		if w_chap_d < 2500 :

			t_last = t_prime + walk(s_r_dest,r_dst)
			wd 		+= w_chap_d

			## mise à jour de la trajectoire du rider
			## new_mean : Mean_of_transportation,new_arr_time,new_dep_time,new_node_id : int
			## on ajoute les temps d'arrivée et de départ de chaque node parcourue
			'''
			le rider va :
			- marcher de s_r_dest à r_dst
			'''
			
			arrival_time_r_dst = t_last # arrivée à la destination
			departure_time_r_dst = arrival_time_r_dst	# départ de la destination

			rider.get_trajectory.update_trajectory(Foot(),arrival_time_r_dst,departure_time_r_dst,r_dst.get_id) # ajouter r_dst à trajectory
				
	if t_last > np.Infinity:
		# le rider ne peut pas atteindre la station s_dst_r

		t_prime = np.Infinity	


	return t_prime


