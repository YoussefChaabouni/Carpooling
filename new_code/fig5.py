import numpy as np
from numpy.core.function_base import linspace
from meansClasses import Foot
from helperFunctions import get_timetable
from current_system import current_system
from check_algorithm_3 import check_algorithm_3
from Integrated_system import integrated_system
from statistics import vehicle_maximum_occupancy, average_walking_and_waiting_time
from no_carpooling_system import no_carpooling_system
from paper_algorithm_4 import algorithm_4
from paper_algorithm_3 import algorithm_3

from paper_algorithm_1 import algorithm_1
from paper_algorithm_2 import algorithm_2
from graphClasses import MeetingPoint, Station, Graph, Trajectory
from PersonClasses import Driver, Rider
from helperFunctions import Drive
from matplotlib import pyplot as plt
from typing import List
import pandas as pd
import seaborn as sns

'''
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
NUMBER_OF_RIDERS = 100
for j in range(NUMBER_OF_RIDERS):

	random_born_time = np.random.randint(0,20)
	n_org = np.random.randint(0,NUMBER_OF_MPS-1)
	n_dest = n_org
	while n_dest == n_org :
		n_dest = np.random.randint(0,NUMBER_OF_MPS-1)

	r = Rider(pos_depart = "MP"+str(n_org),pos_arrivee = "MP"+str(n_dest),ID = "R"+str(j),born_time=random_born_time,trajectory=Trajectory())
	r.trajectory = Trajectory(means_list=[Foot(Speed=5/60,ID="init "+r.get_id())],arr_time_list=[r.born_time],dep_time_list=[r.born_time],node_list=[r.pos_depart])
	riders.append(r)


'''
def travel_time_integrated_current(riders : List[Rider],drivers : List[Driver],G: Graph) :
	integrated_travel_time=[]
	current_travel_time=[]
	riders_CS = riders.copy()
	drivers_CS = drivers.copy()
	riders_integrated = riders.copy()
	drivers_integrated = drivers.copy()
	screwed_up = []
	for i in range(len(riders_integrated)) :
		t_time = integrated_system(riders_integrated[i],drivers_integrated,G)[0] #- r.born_time
		#if t_time != np.Infinity:
			
		
		integrated_travel_time.append(t_time)
		#else :
		#	integrated_travel_time.append(0)
		
	for i in range(len(riders_CS)):
		t_time = current_system(riders_CS[i],drivers_CS,G)[0] #- r.born_time
		#if t_time != np.Infinity and t_time != 0:
			
		
		current_travel_time.append(t_time)
		#else :
		#	current_travel_time.append(0)
		#	screwed_up.append(i)

	#for item in screwed_up:
	#	riders_integrated[item] = 0

	
	print("current = ",current_travel_time)
	print("integrated = ",integrated_travel_time)
	df_dict = {"Current system travel time" : current_travel_time,
				"Integrated system travel time" : integrated_travel_time}
	df = pd.DataFrame(df_dict)
	sns.scatterplot(data=df, x="Current system travel time", y="Integrated system travel time")
	'''
	plt.plot(current_travel_time,integrated_travel_time)
	plt.xlabel('Current system travel time (min)')
	plt.ylabel('Integrated system travel time (min)')
	
	plt.show()
	'''
def frequency(riders,drivers,G):
	integrated_travel_time=[]
	current_travel_time=[]
	no_carpooling_time=[]
	riders_CS = riders.copy()
	drivers_CS = drivers.copy()
	riders_NC = riders.copy()
	drivers_NC = drivers.copy()
	riders_integrated = riders.copy()
	drivers_integrated = drivers.copy()
	screwed_up = []

	integrated_counter = 0
	carpooling_counter = 0
	no_carpooling_counter = 0
	for i in range(len(riders_integrated)) :
		t_time = integrated_system(riders_integrated[i],drivers_integrated,G)[0] #- r.born_time
		if t_time != np.Infinity:
			integrated_counter +=1
		integrated_travel_time.append(t_time)

		
	for i in range(len(riders_CS)):
		t_time = current_system(riders_CS[i],drivers_CS,G)[0] #- r.born_time
		if t_time != np.Infinity:
			carpooling_counter +=1
		current_travel_time.append(t_time)
	
	for i in range(len(riders_NC)):
		t_time = no_carpooling_system(riders_NC[i],drivers_NC,G)[0] #- r.born_time
		if t_time != np.Infinity:
			no_carpooling_counter +=1
		no_carpooling_time.append(t_time)
	
	freq_i = [0]*150
	freq_nc = [0]*150
	freq_cs = [0]*150

	for i in range(150):
		for j in range(len(riders_NC)):
			if integrated_travel_time[j]<= i:
				freq_i[i] +=1
			if no_carpooling_time[j]<= i:
				freq_nc[i] +=1 
			if current_travel_time[j]<= i:
				freq_cs[i] +=1 
	freq_i = [x/len(riders_CS) for x in freq_i]
	freq_nc = [x/len(riders_CS) for x in freq_nc]
	freq_cs = [x/len(riders_CS) for x in freq_cs]

	
	import matplotlib.pyplot as plt
	print("integrated = ",freq_i)
	print("no carpooling = ",freq_nc)
	print("freq cs = ",freq_cs)
	t = np.linspace(0,150,150)
	a = freq_i
	b = freq_nc
	c = freq_cs
	plt.title("Cumulative distribution")
	plt.xlabel("Travel time (min)")
	plt.ylabel("Frequency")

	plt1 = plt.plot(t,a, 'r') # plotting t, a separately 
	plt2 = plt.plot(t, b, 'b') # plotting t, b separately 
	plt3 = plt.plot(t, c, 'g') # plotting t, c separately
	#data = np.array([freq_i,freq_nc,freq_cs])

#	[a,b,c] = plt.plot(data)
	plt.legend([plt1,plt2,plt3], ["Integrated","no carpooling","current"])
	plt.show()
	'''
	#plt.plot(t,a, 'r') # plotting t, a separately 
	plt.plot(t, b, 'b') # plotting t, b separately 
	#plt.plot(t, c, 'g') # plotting t, c separately 
	plt.show()
	'''
#travel_time_integrated_current(riders,drivers,G)
#frequency(riders,drivers,G)