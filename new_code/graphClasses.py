import sys
from typing import List
import numpy as np

from new_code.PersonClasses import User
from new_code.meansClasses import Mean_of_transportation
#import meansClasses.py

class Node:
    #_______________ CLASS CONSTRUCTOR _______________
    def __init__(self,ID : int,x_coord,y_coord):
        self.id = ID
        self.x_coordinate = x_coord
        self.y_coordinate = y_coord
    
    # We can allow instances without a neighbour list
    def __init__(self,x_coord,y_coord):
       
        self.x_coordinate = x_coord
        self.y_coordinate = y_coord

    #__________________________ REPRESENTATION ________________________
    def __repr__(self):
        return repr((self.x_coordinate, self.y_coordinate))

    #____________________________ GETTERS AND SETTERS ___________________________________
    def get_id(self):
        return self.id

    def get_x_coordinate(self):
        return self.x_coordinate

    def get_y_coordinate(self):
        return self.y_coordinate
    
    # returns array of [ x , y ]
    def get_xy_coordinate(self):
        return [self.get_x_coordinate,self.get_y_coordinate]
    

      


class MeetingPoint(Node):
    #____________________________________________CLASS CONSTRUCTOR ______________________________________
    def __init__(self,ID, x_coord, y_coord):
        super().__init__(ID,x_coord, y_coord)

        #_____________________________ verify if node is meeting point or station_________________
    def isStation(self):
        return type(self).__name__ == "Station"
    
    def isMeetingPoint(self):
        return type(self).___name___ == "MeetingPoint"

class Station(MeetingPoint):

    #___________________________________________ CLASS CONSTRUCTOR______________________________________________
    def __init__(self,ID, x_coord, y_coord):
        super().__init__(ID,x_coord, y_coord)
       
        #_____________________________ verify if node is meeting point or station_________________
    def isStation(self):
        return type(self).__name__ == "Station"
    
    def isMeetingPoint(self):
        return type(self).___name___ == "MeetingPoint"


class Graph:
    
    #____________________________CONSTRUCTOR CLASSES _______________________________________
    def __init__(self,node_list):
        self.node_list = node_list
        self.circuity = 1.2
    
    def __init__(self,node_list,circuity):
        self.node_list = node_list
        self.circuity = circuity

    def __init__(self):
        self.node_list = []
        self.circuity = 1.2

    #_____________________________ GETTERS AND SETTERS ___________________________________
    def get_node_list(self):
        return self.node_list
    
    
    #_________________________________ GRAPH METHODS____________________________________
    # adds node to the graph
    def add_node(self,Node):
        if(type(Node).__name__ == "Node"):
            self.node_list.append(Node)
        else :
            sys.out("Tried adding a non Node object to node_list")
    
    # get NODE from node_id
    def get_node(self,node_id):
        for node in self.node_list:
            if node.get_id == node_id:
                return(node)

    # takes node
    def remove_node(self,node):
        if(node in self.node_list):
            self.node_list.remove(node)
            
        else :
            print(" Tried deleting a node that isn't in the graph")
    
    # takes nodes Node1 Node2
    # returns Euclidian distance weighted with circuity constant
    def get_distance(self,Node1,Node2):
        
        return(self.circuity*np.sqrt((Node1.get_y_coord()-Node2.get_y_coord())**2 + (Node1.get_x_coord()-Node2.get_x_coord()**2)))

    
    def get_closest_MP_or_Station(self,origin,type_of_nodes):
        
        #enlever l'origine de la liste de nodes
        nodes = self.get_node_list.remove(origin)

        if type_of_nodes == "MPs":
            nodes = list(filter(lambda x : x.isMeetingPoint(),nodes))
        elif type_of_nodes == "Stations":
            nodes = list(filter(lambda x : x.isStation(),nodes))
        else:
            sys.exit("Bad node type in 'get_closest_MP_or_Station()' method, type : "+type_of_nodes)

        V = np.zeros((len(nodes),2))

        for i,n in enumerate(nodes):
            V[i] = nodes.get_xy_coordinate()

        argmin_node = np.argmin(np.linalg.norm(V - origin.get_xy_coordinate()))

        return nodes[argmin_node]    


class Trajectory(Graph):

    def __init__(self,means_list,arr_time_list,dep_time_list,node_list):
        self.means_list = means_list
        self.arr_time_list = arr_time_list
        self.dep_time_list = dep_time_list      
        self.node_id_list = node_list #list of node IDs 

    def __init__(self,user):
        self.means_list = []
        self.arr_time_list = []
        self.node_id_list = []
        self.dep_time_list = []
    
    #_________________ GETTERS AND SETTERS ___________________
    def get_node_id_list(self):
        return self.node_id_list

    def update_trajectory(self,new_mean : Mean_of_transportation,new_arr_time,new_dep_time,new_node_id : int):
        self.means_list.append(new_mean)
        self.arr_time_list.append(new_arr_time)
        self.dep_time_list.append(new_dep_time)
        self.node_id_list.append(new_node_id)

   


