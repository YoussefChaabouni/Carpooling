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

# POUR LE CAMEMBERT
carpooling = 0
foot = 0
transit = 0
no_solution = 0
integrated = 0

for r in RIDERS:
    print("______________________INTEGRATED SYSTEM_________________________________")
    print("___________________FOR RIDER : ",r.get_id(),"_________________________")
    solution = integrated_system(r,DRIVERS,G)[1]

    print("____________RIDER INFORMATION POST INTEGRATED SYSTEM______________________")
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
end = time.time()

from matplotlib import pyplot as plt
import numpy as np
 
# CAMEMBERT 
'''
# Creating dataset
labels = ['CARPOOLING', 'FOOT',
        'TRANSIT', 'NO SOLUTION']
 
data = [carpooling*100, foot*100, transit*100,no_solution*100]
 
# Creating plot
fig = plt.figure(figsize =(10, 7))
plt.pie(data, labels = labels)
 
# show plot
plt.show()
'''
#fig, ax = plt.subplots(figsize=(8, 4), subplot_kw=dict(aspect="equal"))

labels = ['CARPOOLING', 'FOOT',
        'TRANSIT','INTEGRATED', 'NO SOLUTION']

data = [carpooling*100, foot*100, transit*100,integrated*100,no_solution*100]


explode = (0, 0, 0, 0, 0) 

fig1, ax1 = plt.subplots(figsize=(10, 7))
ax1.pie(data, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=0)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.legend()

plt.show()

max_list = vehicle_maximum_occupancy(DRIVERS,system = "Integrated")
print(max_list)