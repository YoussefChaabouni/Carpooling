## this is the function that will generate the map according to the draft

from math import sqrt
import math
import numpy as np
from graphClasses import MeetingPoint, Station
from helperFunctions import get_timetable
from graphClasses import Node, Graph, Trajectory
from PersonClasses import Driver, Rider
from meansClasses import Foot
from tqdm import tqdm


def data_generation():

    #NUMBER_OF_MPS = 50
    NUMBER_OF_STATIONS = 10
    MAP_LENGTH = 15 # en km
    MAP_WIDTH = 8
    NB_Drivers = int(4.8*MAP_LENGTH*MAP_WIDTH*2) # 1728
    NB_riders = int(8.3*MAP_LENGTH*MAP_WIDTH*2)

 
    NODES = []

    #print(x,y)
    print("generating the first batch of MPS")
    for i in tqdm(range(int(MAP_LENGTH*MAP_WIDTH/3.55))): #so we get an average of 1 point per 3.55 square kilometer
        x = np.random.random() * MAP_LENGTH
        y = np.random.random() * MAP_WIDTH
        NODES.append(MeetingPoint(ID="MP"+str(i),x_coord=x, y_coord=y))

   
    duration_of_simulation = 60*5
    train_frequency = 5
    number_of_trains_per_sim = int(duration_of_simulation/train_frequency)

    list_id_stations = []
    
    STATIONS = []
    print("generating stations")
    for i in tqdm(range(NUMBER_OF_STATIONS)):
        x = i*MAP_LENGTH/(NUMBER_OF_STATIONS-1)
        y = MAP_WIDTH /2
        list_id_stations.append("S"+str(i))
        STATIONS.append(Station(ID="S"+str(i),x_coord=x, y_coord=y))

    # GENERATE THE 4 or 5 EXTRA MEETING POINTS
    counter = len(NODES) # counter for MP NAME
    print("Generating the second batch of MPS")
    for i in tqdm(range(len(STATIONS))) : 
        node = STATIONS[i]
        r = np.random.rand()
        if r == 0:
            number_of_extra_mps = 4
        else :
            number_of_extra_mps = 5

        R = 0.3 # 300m radius around MP

        r = R * sqrt(np.random.random())
        theta = np.random.random() * 2 * math.pi

        centerX = node.x_coordinate
        centerY = node.y_coordinate

        for i in range(number_of_extra_mps):
            x = centerX + r * math.cos(theta)
            y = centerY + r * math.sin(theta)
            NODES.append(MeetingPoint(ID="MP"+str(counter),x_coord=x, y_coord=y))
            counter +=1


    ## DRIVERS ORIGIN LIST
    ## The drivers are generated in meeting points
    drivers_origin_dest = []
    print("generating drivers origins")
    for i in tqdm(range(NB_Drivers)):
        r1 = np.random.randint(0,len(NODES))
        r2 = np.random.randint(0,len(NODES))
        while r1 == r2 :
            r2 = np.random.randint(0,len(NODES))
        drivers_origin_dest.append([NODES[r1],NODES[r2]])

    ## RIDERS ORIGIN
    ## The riders are generated uniformly at random in a node
    riders_origins = []
    riders_dest = []
    counter = 0
    print("generating riders origins and destinations")
    for i in tqdm(range(NB_riders)):
        x = np.random.random() * MAP_LENGTH
        y = np.random.random() * MAP_WIDTH

        x_dst = np.random.random() * MAP_LENGTH
        y_dst = np.random.random() * MAP_WIDTH
        
        riders_origins.append(Node(ID="ORG"+str(counter),x_coord=x, y_coord=y))
        riders_dest.append(Node(ID="DST"+str(counter),x_coord=x_dst,y_coord=y_dst))
        counter += 1



    # INITIALISATION DU GRAPH
    final_graph_list = NODES + STATIONS + riders_origins + riders_dest

    G = Graph(node_list = final_graph_list)

    timetable_gauche , timetable_droite = get_timetable(G,60,list_id_stations,number_of_trains_per_sim)

    # add timetables to stations
    print("adding timetables to stations")
    for i in tqdm(range(len(list_id_stations))):
        G.get_node(list_id_stations[i]).liste_gauche = timetable_gauche[:,i].tolist()
        G.get_node(list_id_stations[i]).liste_droite = timetable_droite[:,i].tolist()

    #print("liste gauche de S0 = ",G.get_node(list_id_stations[0]).liste_gauche)

    print("graph of this many nodes = ",len(G.node_list))

    # GENERATE DRIVERS AND RIDERS
    drivers = []
    print("generating drivers")
    for i in tqdm(range(NB_Drivers)):

        # generate random born time
        random_born_time = np.random.randint(0,180)


        # initialise drivers
        d = Driver(pos_depart=drivers_origin_dest[i][0].id,
        pos_arrivee=drivers_origin_dest[i][1].id,
        ID_user = "D"+str(i),
        born_time = random_born_time,
        ID_car="C"+str(i),
        Speed=40,
        max_capacity=4,
        current_capacity=[],
        riders_list=[],
        trajectory=Trajectory())

        d.trajectory = Trajectory(means_list=[d],arr_time_list=[d.born_time],dep_time_list=[d.born_time],node_list=[d.pos_depart])

        drivers.append(d)


    riders_list = []
    print("generating riders")

    for j in tqdm(range(NB_riders)):

        random_born_time = np.random.randint(0,180)
        
        

        r = Rider(pos_depart = riders_origins[j].id,pos_arrivee = riders_dest[j].id,ID = "R"+str(j),born_time=random_born_time,trajectory=Trajectory())
        r.trajectory = Trajectory(means_list=[Foot(Speed=5/60,ID="init "+r.get_id())],arr_time_list=[r.born_time],dep_time_list=[r.born_time],node_list=[r.pos_depart])
        riders_list.append(r)

    return riders_list, drivers, G