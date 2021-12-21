import numpy as np
from meansClasses import Foot
from helperFunctions import get_timetable
from current_system import current_system
from check_algorithm_3 import check_algorithm_3
from Integrated_system import integrated_system
from statistics import vehicle_maximum_occupancy, average_walking_and_waiting_time
from paper_algorithm_4 import algorithm_4
from paper_algorithm_3 import algorithm_3

from paper_algorithm_1 import algorithm_1
from paper_algorithm_2 import algorithm_2
from graphClasses import MeetingPoint, Station, Graph, Trajectory
from PersonClasses import Driver, Rider
from helperFunctions import Drive
from matplotlib import pyplot as plt
from typing import List


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

drivers = []
for i in range(500):

    # generate random origin, destination and born time
    random_born_time = np.random.randint(0,60)
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

riders = []
NUMBER_OF_RIDERS = 300
for j in range(NUMBER_OF_RIDERS):

	random_born_time = np.random.randint(0,20)
	n_org = np.random.randint(0,NUMBER_OF_MPS-1)
	n_dest = n_org
	while n_dest == n_org :
		n_dest = np.random.randint(0,NUMBER_OF_MPS-1)

	r = Rider(pos_depart = "MP"+str(n_org),pos_arrivee = "MP"+str(n_dest),ID = "R"+str(j),born_time=random_born_time,trajectory=Trajectory())
	r.trajectory = Trajectory(means_list=[Foot(Speed=5/60,ID="init "+r.get_id())],arr_time_list=[r.born_time],dep_time_list=[r.born_time],node_list=[r.pos_depart])
	riders.append(r)



def travel_time_integrated_current(riders : List[Rider],drivers : List[Driver],G: Graph) :
	integrated_travel_time=[]
	current_travel_time=[]
	riders_CS = riders.copy()
	drivers_CS = drivers.copy()
	riders_integrated = riders.copy()
	drivers_integrated = drivers.copy()
	for r in riders_integrated :
		integrated_travel_time.append(integrated_system(r,drivers_integrated,G)[0] - r.born_time)
	for r in riders_CS:
		current_travel_time.append(current_system(r,drivers_CS,G)[0] - r.born_time)
	plt.plot(integrated_travel_time,current_travel_time)
	plt.xlabel('Current system travel time (min)')
	plt.ylabel('Integrated system travel time (min)')
	plt.show()

travel_time_integrated_current(riders,drivers,G)