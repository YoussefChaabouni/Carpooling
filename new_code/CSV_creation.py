"""
Ce fichier permet de générer automatiquement un scénario de simulation
Il comprend donc la création de 4 fichiers :
	- les paramètres des Meeting Points (Meeting_Points.csv)
	- les paramètres des Stations (Stations.csv)
	- les paramètres des Drivers (Drivers.csv)
	- les paramètres des Riders (Riders.csv)
"""
import pandas as pd
import numpy as np


# CONSTANTES
#-------------------------------------------#
NUMBER_OF_MPS      = 50
NUMBER_OF_STATIONS = 10
NUMBER_OF_DRIVERS  = 500
NUMBER_OF_RIDERS   = 1000
TAILLE_DE_MAP      = 10  # en km
DUREE_DE_SIM       = 180 # en minutes (3 heures)
#-------------------------------------------#


# CREATION DU GRAPH

x,y = np.random.random((2,NUMBER_OF_MPS)) * TAILLE_DE_MAP

IDs = np.array(list(map(lambda x : "MP"+str(x),list(range(NUMBER_OF_MPS)))))

DF_graph_MPS = pd.DataFrame(np.array([IDs,x,y]).T,columns=["IDs","x_coord","y_coord"])


x,y = np.random.random((2,NUMBER_OF_STATIONS)) * TAILLE_DE_MAP

IDs = np.array(list(map(lambda x : "S"+str(x),list(range(NUMBER_OF_STATIONS)))))

DF_graph_S = pd.DataFrame(np.array([IDs,x,y]).T,columns=["IDs","x_coord","y_coord"])


# CREATION DES DRIVERS

IDs  = np.array(list(map(lambda x : "D"+str(x),list(range(NUMBER_OF_DRIVERS)))))

DF_D = pd.DataFrame(IDs, columns = ["IDs"])

DF_D[["pos_depart","pos_arrivee"]] = ""
DF_D[["pos_depart","pos_arrivee"]] = DF_D[["pos_depart","pos_arrivee"]].apply(lambda x : x+DF_graph_MPS.sample(n=2)["IDs"].values,axis=1)
DF_D["born_time"] = np.random.randint(60, size=NUMBER_OF_DRIVERS)


# CREATION DES RIDERS

IDs  = np.array(list(map(lambda x : "R"+str(x),list(range(NUMBER_OF_RIDERS)))))

DF_R = pd.DataFrame(IDs, columns = ["IDs"])

DF_R[["pos_depart","pos_arrivee"]] = ""
DF_R[["pos_depart","pos_arrivee"]] = DF_R[["pos_depart","pos_arrivee"]].apply(lambda x : x+DF_graph_MPS.sample(n=2)["IDs"].values,axis=1)
DF_R["born_time"] = np.random.randint(20, size=NUMBER_OF_RIDERS)

DF_graph_MPS.to_csv('CSVs/Meeting_Points.csv')
DF_graph_S.to_csv('CSVs/Stations.csv')
DF_D.to_csv('CSVs/Drivers.csv')
DF_R.to_csv('CSVs/Riders.csv')

if __name__=="__main__":
	print(DF_graph_MPS)
	print(DF_graph_S)
	print(DF_D)
	print(DF_R)