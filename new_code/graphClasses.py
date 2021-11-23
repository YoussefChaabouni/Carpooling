import sys
from typing import List
import numpy as np

from new_code.PersonClasses import User
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
      


class MeetingPoint(Node):
    #____________________________________________CLASS CONSTRUCTOR ______________________________________
    def __init__(self,ID, x_coord, y_coord):
        super().__init__(ID,x_coord, y_coord)



class Station(MeetingPoint):

    #___________________________________________ CLASS CONSTRUCTOR______________________________________________
    def __init__(self,ID, x_coord, y_coord):
        super().__init__(ID,x_coord, y_coord)
       


class Graph:
    
    #____________________________CONSTRUCTOR CLASSES _______________________________________
    def __init__(self,node_list):
        self.node_list = node_list
    
    def __init__(self):
        self.node_list = []

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

    # takes node ids
    def remove_node(self,node_id):
        if(self.get_node(node_id) in self.node_list):
            self.node_list.remove(self.get_node(node_id))
            
        else :
            print(" Tried deleting a node that isn't in the graph")
    
    # takes node ids
    def get_distance(self,Node_id_1,Node_id_2):
        Node1 = self.get_node(Node_id_1)
        Node2 = self.get_node(Node_id_2)
        return(np.sqrt((Node1.get_y_coord()-Node2.get_y_coord())**2 + (Node1.get_x_coord()-Node2.get_x_coord()**2)))
        
       
class Trajectory(Graph):

    def __init__(self,user,means_list,arr_time_list,dep_time_list,node_list):
        self.means_list = means_list
        self.arr_time_list = arr_time_list
        self.dep_time_list = dep_time_list      
        self.node_id_list = node_list # node list is the list of node IDs 

    def __init__(self,user):
        self.means_list = []
        self.arr_time_list = []
        self.node_id_list = []
        self.dep_time_list = []
    
    #_________________ GETTERS AND SETTERS ___________________
    def get_node_id_list(self):
        return self.node_id_list

   


