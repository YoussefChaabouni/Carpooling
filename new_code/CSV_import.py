import numpy as np
import pandas as pd
from graphClasses import MeetingPoint, Station, Graph, Trajectory
from PersonClasses import Driver, Rider
from meansClasses import Foot
from paper_algorithm_1 import algorithm_1


# IMPORTATION DES CSVs
DF_graph_MPS = pd.read_csv('CSVs/Meeting_Points.csv',index_col="Unnamed: 0")
DF_graph_S   = pd.read_csv('CSVs/Stations.csv',index_col="Unnamed: 0")
DF_D         = pd.read_csv('CSVs/Drivers.csv',index_col="Unnamed: 0")
DF_R         = pd.read_csv('CSVs/Riders.csv',index_col="Unnamed: 0")


NODES = []
DRIVERS = []
RIDERS = []

# CREATION MEETING POINTS
for i in DF_graph_MPS.values:
	NODES.append(MeetingPoint(ID=i[0],x_coord=i[1], y_coord=i[2]))

# CREATION DES STATIONS
for i in DF_graph_S.values:
	NODES.append(Station(ID=i[0],x_coord=i[1], y_coord=i[2]))

# CREATION DU GRAPH
G = Graph(node_list = NODES)

# CREATION DES DRIVERS
for index,i in enumerate(DF_D.values):
	d = Driver(pos_depart=i[1],
				pos_arrivee=i[2],
				ID_user = i[0],
				born_time = i[3],
				ID_car="C"+str(index),     # TODO : modifier si cela crée des bugs
				Speed=40,
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
for d in DRIVERS:
	journey = algorithm_1(d,G)
	print(journey)
	d.set_journey(journey)
