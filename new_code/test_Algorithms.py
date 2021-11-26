import numpy as np
from meansClasses import Foot
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
for i in range(NUMBER_OF_STATIONS):
	NODES.append(Station(ID="S"+str(i),x_coord=x[i], y_coord=y[i]))

# INITIALISATION DU GRAPH
G = Graph(node_list = NODES)
print("graph of this many nodes = ",len(G.node_list))
# INITIALISATION DU DRIVER
d = Driver(pos_depart="MP0",
	pos_arrivee="MP5",
	ID_user = "D0",
	born_time = 100,
	ID_car="C0",
	Speed=40,
	max_capacity=4,
	current_capacity=0,
	riders_list=[],
	trajectory=Trajectory())

d.trajectory = Trajectory(means_list=[d],arr_time_list=[d.born_time],dep_time_list=[d.born_time],node_list=[d.pos_depart])
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
liste3 = d.get_journey()
new_list = []

for i in liste3 :
	if i not in new_list:

		new_list.append(i)

#print(new_list)

print(d.get_trajectory().node_id_list)

print(d.get_journey())


print("departure times of d = ",d.get_trajectory().dep_time_list)
print("____________________2_________________")


z = r.pos_depart
z_prime=r.pos_arrivee
t=r.born_time


print(algorithm_2(z ,z_prime,t, d = d, m_board = d.get_pos_depart(), m_out = "MP5", graph=G))

print("_____________________3________________")
# algo 3
print(algorithm_3(drivers = [d],rider = r,graph = G))

print('rider trajectory = ',r.get_trajectory().node_id_list)
print("arrival times of rider = ",r.get_trajectory().arr_time_list)
print("waiting time of rider = ",r.waiting_time)
print("walking distance of rider = ",r.walking_distance)
