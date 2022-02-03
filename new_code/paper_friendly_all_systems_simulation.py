import copy
import pandas as pd
import numpy as np
from meansClasses import Foot
from helperFunctions import get_timetable
from current_system import current_system
from CSV_creation import DUREE_DE_SIM
from CSV_creation import NUMBER_OF_RIDERS
from statistics import vehicle_maximum_occupancy
from statistics import average_walking_and_waiting_time , camembert_function
from detour_plot import detour_plot
from mapGeneration import data_generation
from figure5_but_better import frequency2, travel_time_integrated_current2
from statistics import better_camembert
from statistics import better_waiting_walking_times
from no_carpooling_system import no_carpooling_system
from paper_algorithm_4 import algorithm_4
from paper_algorithm_3 import algorithm_3
from tqdm import tqdm
import os
from paper_algorithm_1 import algorithm_1
from paper_algorithm_2 import algorithm_2
from graphClasses import MeetingPoint, Station, Graph, Trajectory
from PersonClasses import Driver, Rider
from helperFunctions import Drive
from Integrated_system import integrated_system
import time
from figure_4 import figure_4

start = time.time()

NUMBER_OF_MPS = 50
NUMBER_OF_STATIONS = 10
TAILLE_DE_MAP = 10 # en km

# CREATION DES NODES
NODES = []
x,y = np.random.random((2,NUMBER_OF_MPS)) * TAILLE_DE_MAP
#print(x,y)
for i in range(NUMBER_OF_MPS):
	NODES.append(MeetingPoint(ID="MP"+str(i),x_coord=x[i], y_coord=y[i]))

x,y = np.random.random((2,NUMBER_OF_STATIONS)) * TAILLE_DE_MAP
#print(x,y)

#liste_droite = [0,1,11]
#liste_gauche = [11 - x for x in liste_droite]

# if s_org < s_dest : 
# 	s_org.get_liste_droite()
# else:
# 	graph.get_node(s_org).get_liste_gauche()   
duration_of_simulation = 300
train_frequency = 5
number_of_trains_per_sim = int(duration_of_simulation/train_frequency)

#list_ids_stations = ["S0","S1","S2","S3"] -> [0,1,1.5,0.5] -> [0,2,3,1] -> [0,2,5,6]


list_id_stations = []

for i in range(NUMBER_OF_STATIONS):
	list_id_stations.append("S"+str(i))
	NODES.append(Station(ID="S"+str(i),x_coord=x[i], y_coord=y[i]))

# INITIALISATION DU GRAPH
G = Graph(node_list = NODES)

timetable_gauche , timetable_droite = get_timetable(G,80,list_id_stations,number_of_trains_per_sim)

# add timetables to stations
for i in range(len(list_id_stations)):
	G.get_node(list_id_stations[i]).liste_gauche = timetable_gauche[:,i].tolist()
	G.get_node(list_id_stations[i]).liste_droite = timetable_droite[:,i].tolist()

#print("liste gauche de S0 = ",G.get_node(list_id_stations[0]).liste_gauche)

print("graph of this many nodes = ",len(G.node_list))

# try out many drivers
drivers = []
for i in range(300):

    # generate random origin, destination and born time
    random_born_time = np.random.randint(0,120)
    n_org = np.random.randint(0,NUMBER_OF_MPS-1)
    n_dest = n_org
    while n_dest == n_org :
        n_dest = np.random.randint(0,NUMBER_OF_MPS-1)

    # initialise drivers
    d = Driver(pos_depart="MP"+str(n_org),
	pos_arrivee="MP"+str(n_dest),
	ID_user = "D"+str(i),
	born_time = random_born_time,
	ID_car="C"+str(i),
	Speed=40/60,
	max_capacity=4,
	current_capacity=[],
	riders_list=[],
	trajectory=Trajectory())

    d.trajectory = Trajectory(means_list=[d],arr_time_list=[d.born_time],dep_time_list=[d.born_time],node_list=[d.pos_depart])

    drivers.append(d)


riders_list = []
NUMBER_OF_RIDERS = 100
for j in range(NUMBER_OF_RIDERS):

	random_born_time = np.random.randint(0,120)
	n_org = np.random.randint(0,NUMBER_OF_MPS-1)
	n_dest = n_org
	while n_dest == n_org :
		n_dest = np.random.randint(0,NUMBER_OF_MPS-1)

	r = Rider(pos_depart = "MP"+str(n_org),pos_arrivee = "MP"+str(n_dest),ID = "R"+str(j),born_time=random_born_time,trajectory=Trajectory())
	r.trajectory = Trajectory(means_list=[Foot(Speed=5/60,ID="init "+r.get_id())],arr_time_list=[r.born_time],dep_time_list=[r.born_time],node_list=[r.pos_depart])
	riders_list.append(r)

# GENERATE THE DATA WITH RESPECT TO THE PAPER
#riders_list, drivers, G = data_generation()
NUMBER_OF_RIDERS = len(riders_list)

DRIVERS = drivers
RIDERS = riders_list

# empty the folder
save_path = "graphs"
#os.remove(save_path)
#os.makedirs(save_path)

def simulation(DRIVERS,RIDERS,G,save_path):
	# APPLICATION DE L'ALGORITHME 1
	print("___________________ALGORITHM 1_________________________________")
	for d in DRIVERS:
		journey = algorithm_1(d,G)
		#print(journey)
		d.set_journey(journey)




	# TOUTES LES LISTES DES DIFFERENTES SIMULATIONS
	drivers_1 = copy.deepcopy(DRIVERS)
	drivers2 = copy.deepcopy(DRIVERS)
	drivers3 = copy.deepcopy(DRIVERS)
	ALL_DRIVERS   = [drivers_1,drivers2,drivers3]
	ALL_RIDERS    = [copy.deepcopy(RIDERS),copy.deepcopy(RIDERS),copy.deepcopy(RIDERS)]
	ALL_GRAPHS    = [G,G,G]
	ALL_SOLUTIONS = [[],[],[]]
	ALL_TIMES     = [[],[],[]]

	# parameters for plot function "figure_4"
	T_t = []
	T_d = []

	C_t = []
	C_d = []

	I_t = []
	I_d = []

	T_d_inf = []
	C_d_inf = []
	I_d_inf = []

	EFFECTIVE_RIDERS = [[],[],[]]
	EFFECTIVE_TIMES = [[],[],[]]
	EFFECTIVE_SOLUTIONS = [[],[],[]]
	EFFECTIVE_DRIVERS = [[],[],[]]

	print("______________________CURRENT SYSTEM_________________________________")
	for r in tqdm(range(len(ALL_RIDERS[1]))):

		
		
		#print("___________________FOR RIDER : ",ALL_RIDERS[1][r].get_id(),"_________________________")
		time, solution = current_system(ALL_RIDERS[1][r],ALL_DRIVERS[1],ALL_GRAPHS[1])
		ALL_TIMES[1].append(time)
		ALL_SOLUTIONS[1].append(solution)

		if ALL_RIDERS[1][r].born_time <= 60:
			EFFECTIVE_RIDERS[1].append(ALL_RIDERS[1][r])
			EFFECTIVE_TIMES[1].append(time)
			EFFECTIVE_SOLUTIONS[1].append(solution)
		
	for driver in ALL_DRIVERS[1]:
		if driver.born_time <= 60 :
			EFFECTIVE_DRIVERS[1].append(driver)	


	print("______________________INTEGRATED SYSTEM_________________________________")
	for r in tqdm(range(len(ALL_RIDERS[2]))):
		#print("___________________FOR RIDER : ",ALL_RIDERS[2][r].get_id(),"_________________________")
		#print("sanity check")
		#for i in range(len(ALL_DRIVERS[2])):
			#print("driver capacity = ",ALL_DRIVERS[2][i].current_capacity)
		time, solution = integrated_system(ALL_RIDERS[2][r],ALL_DRIVERS[2],ALL_GRAPHS[2])
		ALL_TIMES[2].append(time)
		ALL_SOLUTIONS[2].append(solution)

		if ALL_RIDERS[2][r].born_time <= 60:
			EFFECTIVE_RIDERS[2].append(ALL_RIDERS[2][r])
			EFFECTIVE_TIMES[2].append(time)
			EFFECTIVE_SOLUTIONS[2].append(solution)

	for driver in ALL_DRIVERS[2]:
		if driver.born_time <= 60 :
			EFFECTIVE_DRIVERS[2].append(driver)	


	print("_________________NO CARPOOLING SYSTEM_________________")
	for r in tqdm(range(len(ALL_RIDERS[0]))):
		#print("___________________FOR RIDER : ",ALL_RIDERS[0][r].get_id(),"_________________________")
		time, solution = no_carpooling_system(ALL_RIDERS[0][r],ALL_GRAPHS[0])
		ALL_TIMES[0].append(time)
		ALL_SOLUTIONS[0].append(solution)

		if ALL_RIDERS[0][r].born_time <= 60:
			EFFECTIVE_RIDERS[0].append(ALL_RIDERS[0][r])
			EFFECTIVE_TIMES[0].append(time)
			EFFECTIVE_SOLUTIONS[0].append(solution)

	for driver in ALL_DRIVERS[0]:
		if driver.born_time <= 60 :
			EFFECTIVE_DRIVERS[0].append(driver)	

	for i in tqdm(range(len(EFFECTIVE_RIDERS[0]))):

		rider_T = EFFECTIVE_RIDERS[0][i]
		rider_C = EFFECTIVE_RIDERS[1][i]
		rider_I = EFFECTIVE_RIDERS[2][i]

		distance_T = ALL_GRAPHS[0].get_distance(ALL_GRAPHS[0].get_node(rider_T.get_pos_depart()),ALL_GRAPHS[0].get_node(rider_T.get_pos_arrivee()))
		distance_C = ALL_GRAPHS[1].get_distance(ALL_GRAPHS[1].get_node(rider_C.get_pos_depart()),ALL_GRAPHS[1].get_node(rider_C.get_pos_arrivee()))
		distance_I = ALL_GRAPHS[2].get_distance(ALL_GRAPHS[2].get_node(rider_I.get_pos_depart()),ALL_GRAPHS[2].get_node(rider_I.get_pos_arrivee()))

		time_T = EFFECTIVE_TIMES[0][i]
		time_C = EFFECTIVE_TIMES[1][i]
		time_I = EFFECTIVE_TIMES[2][i]

		faster_than_foot = 0
		slower_than_foot = 0
		if time_T != np.inf and time_T<=distance_T*60/4.5:# accounting for circuity
			T_t.append(time_T)
			T_d.append(distance_T)
		else:
			T_d_inf.append(distance_T)

		if time_C != np.inf and time_C<=distance_C*60/4.5:
			C_t.append(time_C)
			C_d.append(distance_C)
		else:
			C_d_inf.append(distance_C)

		if time_I != np.inf and time_I<=distance_I*60/4.5:
			I_t.append(time_I)
			I_d.append(distance_I)
		else:
			I_d_inf.append(distance_I)
	'''
		for i in range(len(I_t)):
			if I_t[i] > 5*distance_I[i]:
				slower_than_foot +=1
	'''

	# CAMEMBERTS!!!!!
	camembert_function(EFFECTIVE_SOLUTIONS)
	better_camembert(EFFECTIVE_SOLUTIONS,save_path)
	
	# THE "pattes de mouches"
	figure_4(T_t,T_d, C_t,C_d, I_t,I_d, T_d_inf,C_d_inf,I_d_inf,save_path)

	# CUMULATIVE DISTRIBUTION
	#frequency2(EFFECTIVE_TIMES,save_path=save_path)

	# TRAVEL TIMES
	#travel_time_integrated_current2(EFFECTIVE_TIMES,save_path)
	better_waiting_walking_times(EFFECTIVE_RIDERS,save_path)


	#maximum vehicle occupancy

	max_curr = vehicle_maximum_occupancy(EFFECTIVE_DRIVERS[1],system = "Current",save_path=save_path)
	
	#average_walking_and_waiting_time(EFFECTIVE_RIDERS[1],system="Current",save_path=save_path)


	max_int = vehicle_maximum_occupancy(EFFECTIVE_DRIVERS[2],system = "Integrated",save_path=save_path)
	print("current = ",max_curr)
	print("max_int = ",max_int)
	# average walking and waiting times

	#average_walking_and_waiting_time(EFFECTIVE_RIDERS[2],system="Integrated",save_path=save_path)

	#detours
	detour_plot(EFFECTIVE_DRIVERS[2],save_path=save_path)

	return 0

# uncomment to run the simulation	
# simulation(DRIVERS,RIDERS,G,save_path)