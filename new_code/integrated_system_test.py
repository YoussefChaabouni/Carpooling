import numpy as np
from meansClasses import Foot
from helperFunctions import get_timetable
from current_system import current_system
from Integrated_system import integrated_system
from statistics import vehicle_maximum_occupancy, average_walking_and_waiting_time
from detour_plot import detour_plot
from paper_algorithm_4 import algorithm_4
from paper_algorithm_3 import algorithm_3

from paper_algorithm_1 import algorithm_1
from paper_algorithm_2 import algorithm_2
from graphClasses import MeetingPoint, Station, Graph, Trajectory
from PersonClasses import Driver, Rider
from helperFunctions import Drive
import time

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


riders_list = []
NUMBER_OF_RIDERS = 800
for j in range(NUMBER_OF_RIDERS):

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

carpooling = 0
foot = 0
transit = 0
no_solution = 0
integrated = 0


for r in riders_list:
    print("______________________INTEGRATED SYSTEM_________________________________")
    print("___________________FOR RIDER : ",r.get_id(),"_________________________")
    solution = integrated_system(r,drivers,G)[1]

    print("____________RIDER INFORMATION POST CURRENT SYSTEM______________________")
    print('rider trajectory = ',r.get_trajectory().node_id_list)
    print("arrival times of rider = ",r.get_trajectory().arr_time_list)
    print("waiting time of rider = ",r.waiting_time)
    print("walking distance of rider = ",r.walking_distance)

    if solution == "carpooling":
        carpooling +=1
    if solution == "transit":
        transit += 1
    if solution == "foot":
        foot += 1
    if solution == "no solution":
        no_solution +=1
    if solution == "integrated":
        integrated +=1

carpooling = carpooling / NUMBER_OF_RIDERS
foot = foot / NUMBER_OF_RIDERS
transit = transit / NUMBER_OF_RIDERS
no_solution = no_solution / NUMBER_OF_RIDERS
integrated = integrated / NUMBER_OF_RIDERS

end = time.time()

print("TIME OF SIMULATION = ",end - start)
print("carpooling ratio = ",carpooling*100,"%")
print("foot ratio = ",foot*100,"%")
print("transit ratio = ",transit*100,"%")
print("integrated ratio = ",integrated*100,"%")
print("no solution ratio = ",no_solution*100,"%")

from matplotlib import pyplot as plt
import numpy as np
 
 
# Creating dataset
labels = ['CARPOOLING', 'FOOT',
        'TRANSIT','INTEGRATED', 'NO SOLUTION']
 
data = [carpooling*100, foot*100, transit*100,integrated*100,no_solution*100]
 
# Creating plot
fig = plt.figure(figsize =(10, 7))
plt.pie(data, labels = labels)
 
# show plot
plt.show()


max_list = vehicle_maximum_occupancy(drivers,system = "Integrated")
print(max_list)

average_walking , average_waiting = average_walking_and_waiting_time(riders_list,system="Integrated")
print(average_walking)
print(average_waiting)

detour_plot(drivers)