import pandas as pd
import numpy as np
from meansClasses import Foot
from helperFunctions import get_timetable
from current_system import current_system
from CSV_creation import DUREE_DE_SIM
from CSV_creation import NUMBER_OF_RIDERS
from statistics import vehicle_maximum_occupancy
from paper_algorithm_4 import algorithm_4
from paper_algorithm_3 import algorithm_3

from paper_algorithm_1 import algorithm_1
from paper_algorithm_2 import algorithm_2
from graphClasses import MeetingPoint, Station, Graph, Trajectory
from PersonClasses import Driver, Rider
from helperFunctions import Drive
from Integrated_system import integrated_system
import time
from figure_4 import figure_4



start = time.time()
# IMPORTATION DES CSVs
DF_graph_MPS = pd.read_csv('CSVs/Meeting_Points.csv',index_col="Unnamed: 0")
DF_graph_S   = pd.read_csv('CSVs/Stations.csv',index_col="Unnamed: 0")
DF_D         = pd.read_csv('CSVs/Drivers.csv',index_col="Unnamed: 0")
DF_R         = pd.read_csv('CSVs/Riders.csv',index_col="Unnamed: 0")

#constantes
TRAIN_FREQUENCY = 5
number_of_trains_per_sim = int(DUREE_DE_SIM/TRAIN_FREQUENCY)



NODES = []
DRIVERS = []
RIDERS = []

# CREATION MEETING POINTS
for i in DF_graph_MPS.values:
	NODES.append(MeetingPoint(ID=i[0],x_coord=i[1], y_coord=i[2]))

# CREATION DES STATIONS
list_id_stations = []
for i in DF_graph_S.values:
	list_id_stations.append(i[0])
	NODES.append(Station(ID=i[0],x_coord=i[1], y_coord=i[2]))

# CREATION DU GRAPH
G = Graph(node_list = NODES)

# TRAIN TIMETABLE
timetable_gauche , timetable_droite = get_timetable(G,80/60,list_id_stations,number_of_trains_per_sim)
# add timetables to stations
for i in range(len(list_id_stations)):
	G.get_node(list_id_stations[i]).liste_gauche = timetable_gauche[:,i].tolist()
	G.get_node(list_id_stations[i]).liste_droite = timetable_droite[:,i].tolist()

print("graph of this many nodes = ",len(G.node_list))

# CREATION DES DRIVERS
for index,i in enumerate(DF_D.values):
	d = Driver(pos_depart=i[1],
				pos_arrivee=i[2],
				ID_user = i[0],
				born_time = i[3],
				ID_car="C"+str(index),     # TODO : modifier si cela crée des bugs
				Speed=40/60,
				max_capacity=4,
				current_capacity=0,
				riders_list=[],
				trajectory=Trajectory())
	d.trajectory = Trajectory(means_list=[d],arr_time_list=[i[3]],dep_time_list=[i[3]],node_list=[i[1]])
	DRIVERS.append(d)

# CREATION DES RIDERS
for i in DF_R.values:
	r = Rider(pos_depart = i[1],
				pos_arrivee = i[2],
				ID = i[0],
				born_time=i[3],
				trajectory=Trajectory())
	r.trajectory = Trajectory(means_list=[Foot(Speed=5,ID="init "+r.get_id())],arr_time_list=[i[3]],dep_time_list=[i[3]],node_list=[i[1]])
	RIDERS.append(r)

print(G)
print(RIDERS)
print(DRIVERS)

# APPLICATION DE L'ALGORITHME 1
print("___________________ALGORITHM 1_________________________________")
for d in DRIVERS:
	journey = algorithm_1(d,G)
	print(journey)
	d.set_journey(journey)




# TOUTES LES LISTES DES DIFFERENTES SIMULATIONS
ALL_DRIVERS   = [DRIVERS.copy(),DRIVERS.copy(),DRIVERS.copy()]
ALL_RIDERS    = [RIDERS.copy(),RIDERS.copy(),RIDERS.copy()]
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


print("______________________CURRENT SYSTEM_________________________________")
for r in ALL_RIDERS[1]:
	
	print("___________________FOR RIDER : ",r.get_id(),"_________________________")
	time, solution = current_system(r,ALL_DRIVERS[1],ALL_GRAPHS[1])
	ALL_TIMES[1].append(time)
	ALL_SOLUTIONS[1].append(solution)

print("______________________INTEGRATED SYSTEM_________________________________")
for r in ALL_RIDERS[2]:
	print("___________________FOR RIDER : ",r.get_id(),"_________________________")
	time, solution = integrated_system(r,ALL_DRIVERS[2],ALL_GRAPHS[2])
	ALL_TIMES[2].append(time)
	ALL_SOLUTIONS[2].append(solution)


for i in range(len(ALL_RIDERS[0])):

	#rider_T = ALL_RIDERS[0][i]
	rider_C = ALL_RIDERS[1][i]
	rider_I = ALL_RIDERS[2][i]

	#distance_T = ALL_GRAPHS[0].get_distance(ALL_GRAPHS[0].get_node(rider_T.get_pos_depart()),ALL_GRAPHS[0].get_node(rider_T.get_pos_arrivee()))
	distance_C = ALL_GRAPHS[1].get_distance(ALL_GRAPHS[1].get_node(rider_C.get_pos_depart()),ALL_GRAPHS[1].get_node(rider_C.get_pos_arrivee()))
	distance_I = ALL_GRAPHS[2].get_distance(ALL_GRAPHS[2].get_node(rider_I.get_pos_depart()),ALL_GRAPHS[2].get_node(rider_I.get_pos_arrivee()))

	#time_T = ALL_TIMES[0][i]
	time_C = ALL_TIMES[1][i]
	time_I = ALL_TIMES[2][i]

	#if time_T != np.inf:
	#	T_t.append(time_T)
	#	T_d.append(distance_T)
	#else:
	#	T_d_inf.append(distance_T)

	if time_C != np.inf:
		C_t.append(time_C)
		C_d.append(distance_C)
	else:
		C_d_inf.append(distance_C)

	if time_I != np.inf:
		I_t.append(time_I)
		I_d.append(distance_I)
	else:
		I_d_inf.append(distance_I)


figure_4(T_t,T_d, C_t,C_d, I_t,I_d, T_d_inf,C_d_inf,I_d_inf)