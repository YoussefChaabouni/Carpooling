import numpy as np
from meansClasses import Foot
from helperFunctions import get_timetable
from paper_algorithm_4 import algorithm_4
from paper_algorithm_3 import algorithm_3

from paper_algorithm_1 import algorithm_1
from paper_algorithm_2 import algorithm_2
from graphClasses import MeetingPoint, Station, Graph, Trajectory
from PersonClasses import Driver, Rider
from helperFunctions import Drive

NUMBER_OF_MPS = 10
NUMBER_OF_STATIONS = 3
TAILLE_DE_MAP = 1000 # en mètres

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
duration_of_simulation = 180
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

# INITIALISATION DU DRIVER
d = Driver(pos_depart="MP0",
	pos_arrivee="MP5",
	ID_user = "D0",
	born_time = 10,
	ID_car="C0",
	Speed=40/60,
	max_capacity=4,
	current_capacity=[],
	riders_list=[],
	trajectory=Trajectory())

d.trajectory = Trajectory(means_list=[d],arr_time_list=[d.born_time],dep_time_list=[d.born_time],node_list=[d.pos_depart])

d1 = Driver(pos_depart="MP1",
	pos_arrivee="MP5",
	ID_user = "D1",
	born_time = 20,
	ID_car="C1",
	Speed=40/60,
	max_capacity=4,
	current_capacity=[],
	riders_list=[], 
	trajectory=Trajectory())

d1.trajectory = Trajectory(means_list=[d1],arr_time_list=[d1.born_time],dep_time_list=[d1.born_time],node_list=[d1.pos_depart])

'''
rider = Rider(pos_depart = "MP0",
	pos_arrivee="MP5",
	ID="R0",
	born_time=2,
	trajectory=Trajectory(),
	waiting_time =0,
	walking_distance = 0
	)
'''
r = Rider(pos_depart = "MP0",pos_arrivee = "MP5",ID = "R0",born_time=0,trajectory=Trajectory())
r.trajectory = Trajectory(means_list=[Foot(Speed=5,ID="init "+r.get_id())],arr_time_list=[r.born_time],dep_time_list=[r.born_time],node_list=[r.pos_depart])

journey = algorithm_1(d,G)
d.set_journey(journey)

journey = algorithm_1(d1,G)
d1.set_journey(journey)

liste3 = d.get_journey()
new_list = []

for i in liste3 :
	if i not in new_list:

		new_list.append(i)
print("_______________________________TIME TABLES_________________________________")
#print("gauche = ",timetable_gauche)
#print("droite = ",timetable_droite)



#print(new_list)
print("___________________1_________________________________")
print("trajectory of d = ",d.get_trajectory().node_id_list)
print("trajectory of d1 = ",d1.get_trajectory().node_id_list)

print(d.get_journey())


print("departure times of d = ",d.get_trajectory().dep_time_list)

print("____________________2_________________")


z = r.pos_depart
z_prime=r.pos_arrivee
t=r.born_time


print(algorithm_2(z ,z_prime,t, d = d, m_board = d.get_pos_depart(), m_out = "MP5", graph=G))
print("graph post algo 2 = ",G.node_list)
print("_____________________3________________")
# algo 3
'''
print(algorithm_3(drivers = [d],rider = r,graph = G))

print('rider trajectory = ',r.get_trajectory().node_id_list)
print("arrival times of rider = ",r.get_trajectory().arr_time_list)
print("waiting time of rider = ",r.waiting_time)
print("walking distance of rider = ",r.walking_distance)
print("graph post algo 3 = ",G.node_list)
'''
print("____________4________________________")

drivers = [d,d1]
t_prime = algorithm_4(drivers,r,G)
print("t_prime = ",t_prime)
print('rider trajectory = ',r.get_trajectory().node_id_list)
print("arrival times of rider = ",r.get_trajectory().arr_time_list)
print("waiting time of rider = ",r.waiting_time)
print("walking distance of rider = ",r.walking_distance)
print("graph post algo 4 = ",G.node_list)

