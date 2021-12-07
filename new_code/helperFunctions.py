


import numpy as np
from graphClasses import Graph, Node
from meansClasses import Foot, Car, Train
from graphClasses import Station


def walk(d:Node,m:Node,G:Graph,speed:float):

	distance = G.get_distance(d,m)
	return distance/speed
    
def Drive(a:Node,b:Node,G:Graph,speed:float):
    distance = G.get_distance(a,b)
    return distance/speed

def board_train(a:Station,b:Station,temps_darrivee):
    if a.get_id() < b.get_id():
        idx = get_next_train_index(a.get_liste_gauche(),temps_darrivee)
        return b.get_liste_gauche()[idx]
    else:
        idx = get_next_train_index(a.get_liste_droite(),temps_darrivee)    
        return b.get_liste_droite()[idx]

def get_next_train_index(liste_trains,temps_darrivee):
    for i in range(len(liste_trains)):
        if liste_trains[i] >= temps_darrivee :
            return i
    
    return "error"

def next_train_time(s_r_org : Station,s_r_dest : Station,arrival_time_station : float):
    if s_r_org.get_id() < s_r_dest.get_id():
        liste_trains = s_r_org.get_liste_gauche()    
    else:
        liste_trains = s_r_org.get_liste_droite()

    for i in range(len(liste_trains)):
        if liste_trains[i] >= arrival_time_station :
            return liste_trains[i]

def get_timetable(graph : Graph,vitesse_train : int,list_ids_stations,number_of_trains_per_sim):
    list_of_distances = np.array([0] + [graph.get_distance(graph.get_node(list_ids_stations[i]),graph.get_node(list_ids_stations[i+1])) for i in range(len(list_ids_stations)-1)])
    list_times = list_of_distances / vitesse_train

    print("list of distances = ",list_of_distances)
    print("list id stations = ",list_ids_stations)

    list_times_cumulated = [np.sum(list_times[:i+1]) for i in range(list_times.shape[0])]
    train_times = np.array(list_times_cumulated*number_of_trains_per_sim).reshape(-1,list_times.shape[0])
    train_times_gauche = train_times + np.array([i*5 for i in range(number_of_trains_per_sim)]).reshape(number_of_trains_per_sim,-1)
    train_times_droite = train_times_gauche[:,-1:] - train_times

    print("list times c = ",list_times_cumulated)
    return train_times_gauche , train_times_droite