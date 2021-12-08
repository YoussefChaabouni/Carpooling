import numpy as np
from meansClasses import Foot
from helperFunctions import get_timetable
from current_system import current_system
from paper_algorithm_4 import algorithm_4
from paper_algorithm_3 import algorithm_3

from paper_algorithm_1 import algorithm_1
from paper_algorithm_2 import algorithm_2
from graphClasses import MeetingPoint, Station, Graph, Trajectory
from PersonClasses import Driver, Rider
from helperFunctions import Drive

NUMBER_OF_MPS = 10
NUMBER_OF_STATIONS = 5
TAILLE_DE_MAP = 3 # en km

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
'''
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
# try out many drivers
drivers = []
for i in range(50):

    # generate random origin, destination and born time
    random_born_time = np.random.randint(0,20)
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
for j in range(3):

	random_born_time = np.random.randint(0,20)
	n_org = np.random.randint(0,NUMBER_OF_MPS-1)
	n_dest = n_org
	while n_dest == n_org :
		n_dest = np.random.randint(0,NUMBER_OF_MPS-1)

	r = Rider(pos_depart = "MP"+str(n_org),pos_arrivee = "MP"+str(n_dest),ID = "R"+str(j),born_time=random_born_time,trajectory=Trajectory())
	r.trajectory = Trajectory(means_list=[Foot(Speed=5/60,ID="init "+r.get_id())],arr_time_list=[r.born_time],dep_time_list=[r.born_time],node_list=[r.pos_depart])
	riders_list.append(r)



#print(new_list)
print("___________________ALGORITHM 1_________________________________")

for d in drivers :
    journey = algorithm_1(d,G)
    d.set_journey(journey)
    print("trajectory of ",d.get_id()," = ",d.get_trajectory().node_id_list)

for r in riders_list:
	print("______________________CURRENT SYSTEM_________________________________")
	print("___________________FOR RIDER : ",r.get_id(),"_________________________")
	print(current_system(r,drivers,G))

	print("____________RIDER INFORMATION POST CURRENT SYSTEM______________________")
	print('rider trajectory = ',r.get_trajectory().node_id_list)
	print("arrival times of rider = ",r.get_trajectory().arr_time_list)
	print("waiting time of rider = ",r.waiting_time)
	print("walking distance of rider = ",r.walking_distance)