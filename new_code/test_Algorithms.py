import numpy as np

from paper_algorithm_1 import algorithm_1
from graphClasses import MeetingPoint, Station, Graph, Trajectory
from PersonClasses import Driver
from helperFunctions import Drive

NUMBER_OF_MPS = 10
NUMBER_OF_STATIONS = 3
TAILLE_DE_MAP = 1000 # en mètres

# CREATION DES NODES
NODES = []
x,y = np.random.random((2,NUMBER_OF_MPS)) * TAILLE_DE_MAP
print(x,y)
for i in range(NUMBER_OF_MPS):
	NODES.append(MeetingPoint(ID="MP"+str(i),x_coord=x[i], y_coord=y[i]))

x,y = np.random.random((2,NUMBER_OF_STATIONS)) * TAILLE_DE_MAP
print(x,y)
for i in range(NUMBER_OF_STATIONS):
	NODES.append(Station(ID="S"+str(i),x_coord=x[i], y_coord=y[i]))

# INITIALISATION DU GRAPH
G = Graph(NODES)

# INITIALISATION DU DRIVER
d = Driver(pos_depart="MP0",
	pos_arrivee="MP5",
	ID_user = "D0",
	born_time = 0,
	ID_car="C0",
	Speed=40,
	max_capacity=4,
	current_capacity=0,
	riders_list=[],
	trajectory=Trajectory())

print(algorithm_1(d,G))