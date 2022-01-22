from typing import List
import numpy as np
from PersonClasses import Rider
from PersonClasses import Driver
from graphClasses import Graph , Trajectory
from meansClasses import Foot
from helperFunctions import next_train_time
from meansClasses import Train
from paper_algorithm_2 import algorithm_2
from helperFunctions import walk, Drive, board_train
import random



def algorithm_4(drivers: List[Driver],rider : Rider,graph : Graph):

	
	
	t_prime = rider.get_trajectory().dep_time_list[0] ## departure time from origin

	##---------------------------NEXT TRAIN----------------------------------------------
	'''
	on veut pouvoir obtenir le prochain train à chaque fois pour calculer la durée d'attente du rider dans le quai
	une solution temporaire serait de mettre une variable aléatoire entre 0 et 5 minutes pour le temps d'attente
	une solution finale serait d'avoir une liste de tous les instants d'arrivée du train dans la station 
	'''
	next_train_waiting_time = random.randint(0,6)

	best_driver = None
		## rider origin and destination
	r_org = graph.get_node(rider.pos_depart)
	r_dst = graph.get_node(rider.pos_arrivee)

		
	s_r_dest = graph.get_closest_MP_or_Station(r_dst,"Stations").get_id()
	m_r_org = graph.get_closest_MP_or_Station(r_org,"MPs").get_id() # closest MP to r's origin
	s_r_org = graph.get_closest_MP_or_Station(r_org,"Stations").get_id() # closest station to r's origin
	# --------------- FIRST MILE --------------- #
	t_first = np.Infinity

	drove_on_first = False

	for d in drivers:
		
		wd= 0
		wt = 0

		## driver origin and destination
		d_org = graph.get_node(d.pos_depart)
		d_dst = graph.get_node(d.pos_arrivee)
		m_d_org = graph.get_closest_MP_or_Station(d_org,"MPs").get_id() # closest MP to d's origin

		if m_d_org == m_r_org and s_r_org in d.get_trajectory().node_id_list :

			t_chap,w_chap_t,w_chap_d = algorithm_2(z = r_org.get_id() ,z_prime = s_r_org,t = t_prime,d=d,m_board =m_d_org,m_out = s_r_org,graph = graph) # APPLIQUER L'ALGORITHME 2
			
			

			
			if wd + w_chap_d <= 2.5  and  wt + w_chap_t <= 45  and  t_chap < t_first: # les longueurs en Mètres et le temps en Secondes

				
				best_driver = d
				t_first = t_chap
				wd 	= wd + w_chap_d
				wt	= wt + w_chap_t

				
				## mise à jour de la trajectoire du rider
				## new_mean : Mean_of_transportation,new_arr_time,new_dep_time,new_node_id : int
				## on ajoute les temps d'arrivée et de départ de chaque node parcourue
			
				#le rider va :
				#- marcher jusqu'à m_d_org
				#- prendre la voiture jusqu'à s_r_org
				
				arrival_time_mp = t_prime + walk(r_org,graph.get_node(m_d_org),graph,4.5/60) # arrivée à m_r_org
				departure_time_mp = arrival_time_mp + w_chap_t #départ de m_r_org
				arrival_time_station = t_chap + 1 #arrivée à la plateforme de s_r_org
				departure_time_station =  next_train_time(graph.get_node(s_r_org),graph.get_node(s_r_dest),arrival_time_station)	


				rider.get_trajectory().update_trajectory(Foot(ID=m_d_org,Speed=4.5/60),arrival_time_mp,departure_time_mp,m_d_org) # ajouter m_d_org node à trajectory
				rider.get_trajectory().update_trajectory(d,arrival_time_station,departure_time_station,s_r_org) # ajouter s_r_org à trajectory
				
				# mise à jour des informations du rider
				
	#rider.update_waiting_time(wt)
	rider.update_walking_distance(wd)

				# update driver's capacity
	if best_driver != None:
		drove_on_first = True
		#print("le rider monte dans la voiture avec le driver pour le first mile ",best_driver.get_id())
				
		best_d_org = graph.get_node(best_driver.pos_depart)
		best_m_d_org = graph.get_closest_MP_or_Station(best_d_org,"MPs").get_id() # closest MP to d's origin

		idx_board = best_driver.get_trajectory().node_id_list.index(best_m_d_org)
		idx_out = best_driver.get_trajectory().node_id_list.index(s_r_org)
		for i in range(idx_board,idx_out+1):
			best_driver.get_current_capacity()[i] +=(-1)
		#print("driver ID = ",best_driver.get_id())
		#print("current capacity of driver = ",best_driver.get_current_capacity())

		##__________UPDATE DRIVER INFORMATION___________________
		best_driver.first_detour = True
		best_driver.first_riders += 1

	best_driver = None





	if t_first == np.Infinity:
		# si ce n'est pas possible d'amener le rider directement à la station, alors cherchons le meeting-point m_prime le plus proche de la station s_r_org qui sera desservit par une voiture 

		for d in drivers:
			wd = 0
			wt = 0
			'''
			m_d_dst = Graph.get_closest_MP(d.get_pos_arrivee) #closest meeting point to driver's destination
			m_prime = Graph.get_closest_MP(s_r_org) ## closest meeting point to the station which is closest to rider origin
			'''
			#print("destination = ",d_dst.get_id())
			#print("station origine rider = ",s_r_org)
			d_org = graph.get_node(d.pos_depart)
			d_dst = graph.get_node(d.pos_arrivee)
			m_d_dst = graph.get_closest_MP_or_Station(d_dst,"MPs").get_id() # closest MP to d's destination
			m_prime = graph.get_closest_MP_or_Station(graph.get_node(s_r_org),"MPs").get_id() # closest MP to r's closest station to origin
			m_d_org = graph.get_closest_MP_or_Station(d_org,"MPs").get_id() # closest MP to d's origin

			if m_d_dst == m_prime and m_prime in d.get_trajectory().node_id_list and m_d_org in d.get_trajectory().node_id_list:

				t_chap,w_chap_t,w_chap_d = algorithm_2(z = r_org.get_id(),z_prime = s_r_org,t = t_prime,d=d,m_board = m_d_org,m_out = m_prime,graph=graph) # APPLIQUER L'ALGORITHME 2

				if w_chap_d <= 2.5  and  w_chap_t <= 45  and  t_chap < t_first: # les longueurs en Mètres et le temps en Secondes
					
					best_driver = d

					t_first = t_chap
					wd 	= w_chap_d
					wt 	= w_chap_t

					## mise à jour de la trajectoire du rider
					## new_mean : Mean_of_transportation,new_arr_time,new_dep_time,new_node_id : int
					## on ajoute les temps d'arrivée et de départ de chaque node parcourue
					
					#le rider va :
					#- marcher jusqu'à m_d_org
					#- prendre la voiture jusqu'à m_prime
					#- marcher jusqu'à s_r_org
					
					arrival_time_mp = t_prime + w_chap_t + walk(r_org,graph.get_node(m_d_org),graph,4.5/60) # arrivée à m_d_org
					departure_time_mp = arrival_time_mp  #départ de m_r_org
					arrival_time_m_prime = t_chap # arrivée à m_prime
					departure_time_m_prime = t_chap # départ de m_prime
					arrival_time_station = t_chap + walk(graph.get_node(m_prime),graph.get_node(s_r_org),graph,4.5/60) + 1 #arrivée à la plateforme de s_r_org
					departure_time_station = next_train_time(graph.get_node(s_r_org),graph.get_node(s_r_dest),arrival_time_station)	# départ de s_r_org


					rider.get_trajectory().update_trajectory(Foot(ID=m_d_org,Speed=4.5/60),arrival_time_mp,departure_time_mp,m_d_org) # ajouter m_d_org node à trajectory de r
					rider.get_trajectory().update_trajectory(d,arrival_time_m_prime,departure_time_m_prime,m_prime) # ajouter m_prime à trajectory de r
					rider.get_trajectory().update_trajectory(Foot(ID=s_r_org,Speed=4.5/60),arrival_time_station,departure_time_station,s_r_org) # ajouter s_r_org à trajectory de r

					# mise à jour des informations du rider
				
	#rider.update_waiting_time(wt)
	rider.update_walking_distance(wd)

			# update driver's capacity
				# update driver's capacity
	if best_driver != None:
		drove_on_first = True
		#print("le rider monte dans la voiture avec le driver pour le first mile ",best_driver.get_id())
				
		best_d_org = graph.get_node(best_driver.pos_depart)
		best_m_d_org = graph.get_closest_MP_or_Station(best_d_org,"MPs").get_id() # closest MP to d's origin

		idx_board = best_driver.get_trajectory().node_id_list.index(best_m_d_org)
		idx_out = best_driver.get_trajectory().node_id_list.index(m_prime)
		for i in range(idx_board,idx_out+1):
			best_driver.get_current_capacity()[i] +=(-1)
		#print("driver ID = ",best_driver.get_id())
		#print("current capacity of driver = ",best_driver.get_current_capacity())


		##__________UPDATE DRIVER INFORMATION___________________
		best_driver.first_detour = True
		best_driver.first_riders += 1

	best_driver = None		


	if t_first == np.Infinity:
		# le seul choix du rider est donc de marcher jusqu'à la station la plus proche
		
		w_chap_d = graph.get_distance(r_org,graph.get_node(s_r_org))

		if w_chap_d < 2.5 :
		#	print("le rider marche jusqu'à la station de départ")
			t_first = t_prime + walk(r_org,graph.get_node(s_r_org),graph,4.5/60)
			wd 		= w_chap_d

			## mise à jour de la trajectoire du rider
			## new_mean : Mean_of_transportation,new_arr_time,new_dep_time,new_node_id : int
			## on ajoute les temps d'arrivée et de départ de chaque node parcourue
			'''
			le rider va :
			- marcher jusqu'à s_r_org
			'''
			
			arrival_time_station = t_prime + walk(r_org,graph.get_node(s_r_org),graph,4.5/60) + 1 #arrivée à la plateforme de s_r_org
			#departure_time_station = arrival_time_station + next_train_waiting_time	# départ de s_r_org
			departure_time_station = next_train_time(graph.get_node(s_r_org),graph.get_node(s_r_dest),arrival_time_station)
			
			rider.get_trajectory().update_trajectory(Foot(ID=s_r_org,Speed=4.5/60),arrival_time_station,departure_time_station,s_r_org) # ajouter s_r_org à trajectory de r

			# mise à jour des informations du rider
				
			
			rider.update_walking_distance(wd)
				


	#print("the walking distance from first mile = ",wd)
	#print("the waiting time from first mile = ",wt)

	if t_first == np.Infinity:
		# le rider ne peut pas atteindre la station s_get_trajectory()

		t_prime = np.Infinity
		return t_prime

	# --------------- TRAIN --------------- #
	t_prime = t_first # mettre la durée du first mile dans t_prime
	t_prime += 1 # admettons qu'une minute est necessaire afin d'atteindre la plateforme

	# --------------------------- ajouter le train à trajectory de r -----------------------
	

	

	arrival_time_dest_station = board_train(graph.get_node(s_r_org),graph.get_node(s_r_dest),temps_darrivee = departure_time_station ) # temps d'arrivée à s_r_dest
	departure_time_dest_station = arrival_time_dest_station + 1 # temps de départ de s_r_dest
	rider.get_trajectory().update_trajectory(Train(ID=s_r_org + s_r_dest),arrival_time_dest_station,departure_time_dest_station,new_node_id = s_r_dest)


	# ------------------------incrémenter le temps d'attente et t_prime---------------------------
	if drove_on_first :
		wt += departure_time_station - arrival_time_station
	t_prime = departure_time_dest_station


	# ------------------------ LAST MILE ------------------------------- #

	t_last = np.Infinity


	m_r_dest = graph.get_closest_MP_or_Station(r_dst,"MPs").get_id() # closest meeting point to r_dest
	

	##----------------- RIDER GETS PICKED UP DIRECTLY FROM THE STATION -------------------------------------------
	for d in drivers:

		d_dst = graph.get_node(d.pos_arrivee)
		m_d_dest = graph.get_closest_MP_or_Station(d_dst,"MPs").get_id() # closest meeting point to d_dest

		if m_d_dest == m_r_dest and s_r_dest in d.get_trajectory().node_id_list :

			t_chap,w_chap_t,w_chap_d = algorithm_2(z = s_r_dest,z_prime =  r_dst.get_id(),t = t_prime,d=d,m_board = s_r_dest,m_out = m_d_dest,graph=graph)
			if wd + w_chap_d < 2.5 and wt+ w_chap_t <45 and t_chap<t_last:
				#print("le rider monte dans la voiture avec le driver pour le last mile",d.get_id())
				best_driver = d
				# mettre à jour t_last wd et wt
				t_last = t_chap
				wd += w_chap_d
				wt += w_chap_t

				## mise à jour de la trajectoire du rider
				## new_mean : Mean_of_transportation,new_arr_time,new_dep_time,new_node_id : int
				## on ajoute les temps d'arrivée et de départ de chaque node parcourue
				
				#le rider va :
				#- prendre une voiture depuis s_r_org jusqu'à m_r_dest
				#- marcher jusqu'à r_dst
				
				
				arrival_time_m_r_dest = t_chap
				departure_time_m_r_dest = t_chap
				arrival_time_dst = departure_time_m_r_dest + walk(graph.get_node(m_d_dest),r_dst,graph,4.5/60)
				departure_time_dst = arrival_time_dst

				rider.get_trajectory().update_trajectory(d,arrival_time_m_r_dest,departure_time_m_r_dest,m_d_dest) # ajouter m_r_dest à trajectory
				rider.get_trajectory().update_trajectory(Foot(ID=r_dst.get_id(),Speed=4.5),arrival_time_dst,departure_time_dst,r_dst.get_id()) # ajouter r_dst à trajectory de r

				# mise à jour des informations du rider
				
	rider.update_waiting_time(wt)
	rider.update_walking_distance(wd)
				# update driver's capacity
	if best_driver != None:
		#print("le rider monte dans la voiture avec le driver pour le last mile ",best_driver.get_id())
				
		best_d_dest = graph.get_node(best_driver.pos_arrivee)
		best_m_d_dest = graph.get_closest_MP_or_Station(best_d_dest,"MPs").get_id()# closest MP to d's dest

		idx_board = best_driver.get_trajectory().node_id_list.index(s_r_dest)
		idx_out = best_driver.get_trajectory().node_id_list.index(best_m_d_dest)
		for i in range(idx_board,idx_out+1):
			best_driver.get_current_capacity()[i] +=(-1)
		#print("driver ID = ",best_driver.get_id())
		#print("current capacity of driver = ",best_driver.get_current_capacity())

		##__________UPDATE DRIVER INFORMATION___________________
		best_driver.last_detour = True
		best_driver.last_riders += 1

	best_driver = None


##--------------- RIDER HAS TO WALK TO A MEETING POINT IN LAST MILE-----------------------------------------
	if t_last == np.Infinity:

		m_seconde = graph.get_closest_MP_or_Station(graph.get_node(s_r_dest),"Stations").get_id() # meeting point le plus proche de s_r_dest
		for d in drivers:
			'''
			m_dst_d = d.m_dst
			d_trajectory = d.trajectory
			m_dst_r = rider.m_dst
			s_dst_r = rider.s_dst
			'''
			
			d_dst = graph.get_node(d.pos_arrivee)
			m_d_dest = graph.get_closest_MP_or_Station(d_dst,"MPs").get_id() # closest meeting point to d_dest

			if m_d_dest == m_r_dest and s_r_dest in d.get_trajectory().node_id_list :
				if m_d_org == m_seconde :	
					t_chap,w_chap_t,w_chap_d = algorithm_2(z = s_r_dest,z_prime = m_r_dest,t = t_prime,d=d,m_board = m_seconde,m_out = m_d_dest,graph = graph) # APPLIQUER L'ALGORITHME 2

					if wd + w_chap_d <= 2.5  and  wt + w_chap_t <= 45  and  t_chap < t_last: # les longueurs en Mètres et le temps en Secondes
						print("le rider monte dans la voiture avec le driver pour le last mile",d.get_id())
						best_driver = d

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
						
						arrival_time_m_seconde = t_prime + walk(graph.get_node(s_r_dest),graph.get_node(m_seconde),graph,4.5/60) # arrivée en m_seconde
						departure_time_m_seconde = arrival_time_m_seconde + wt	# départ de m_seconde
						arrival_time_m_r_dest = departure_time_m_seconde + Drive(graph.get_node(m_r_dest),graph.get_node(m_seconde),graph,38/60) # arrivée en m_r_dest
						departure_time_m_r_dest = departure_time_m_r_dest # départ de m_r_dest
						arrival_time_r_dst = departure_time_m_r_dest + walk(graph.get_node(m_r_dest),r_dst,graph,4.5/60) # arrivée en r_dest
						departure_time_r_dst = arrival_time_r_dst # départ de r_dest

						rider.get_trajectory().update_trajectory(Foot(ID=m_seconde,Speed=4.5/60),arrival_time_m_seconde,departure_time_m_seconde,m_seconde) # ajouter m_seconde à trajectory de r
						rider.get_trajectory().update_trajectory(d,arrival_time_m_r_dest,departure_time_m_r_dest,m_r_dest) # ajouter m_r_dst à trajectory de r
						rider.get_trajectory().update_trajectory(Foot(ID=r_dst.get_id(),Speed=4.5/60),arrival_time_r_dst,departure_time_r_dst,r_dst.get_id())  # ajouter m_dst à trajectory de r

					# mise à jour des informations du rider
				
	rider.update_waiting_time(wt)
	rider.update_walking_distance(wd)

	if best_driver != None:
		#print("le rider monte dans la voiture avec le driver pour le last mile ",best_driver.get_id())
				
		best_d_dest = graph.get_node(best_driver.pos_arrivee)
		best_m_d_dest = graph.get_closest_MP_or_Station(best_d_dest,"MPs").get_id()# closest MP to d's dest

		idx_board = best_driver.get_trajectory().node_id_list.index(m_seconde)
		idx_out = best_driver.get_trajectory().node_id_list.index(best_m_d_dest)
		for i in range(idx_board,idx_out+1):
			best_driver.get_current_capacity()[i] +=(-1)
		#print("driver ID = ",best_driver.get_id())
		#print("current capacity of driver = ",best_driver.get_current_capacity())

		##__________UPDATE DRIVER INFORMATION___________________
		best_driver.last_detour = True
		best_driver.last_riders += 1

	best_driver = None

	if t_last == np.Infinity:
		# le seul choix du rider est donc de marcher jusqu'à la station la plus proche

		w_chap_d = graph.get_distance(graph.get_node(s_r_dest),r_dst)

		if w_chap_d < 2.5 :
			#print("le rider va marcher pour le last mile")

			t_last = t_prime + walk(graph.get_node(s_r_dest),r_dst,graph,4.5/60)
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

			rider.get_trajectory().update_trajectory(Foot(ID=r_dst.get_id(),Speed=4.5/60),arrival_time_r_dst,departure_time_r_dst,r_dst.get_id()) # ajouter r_dst à trajectory
			# mise à jour des informations du rider
			rider.update_walking_distance(wd)
				
	if t_first == np.Infinity and t_last == np.Infinity:
		# le rider ne peut pas atteindre la station s_dst_r

		t_prime = np.Infinity

	#print("the walking distance from first mile = ",wd)
	#print("the waiting time from first mile = ",wt)

	return t_prime


