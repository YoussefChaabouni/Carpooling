import sys
import numpy as np
#import meansClasses.py

class Node:
    #_______________ CLASS CONSTRUCTOR _______________
    def __init__(self,neighbours_dict,x_coord,y_coord):
        self.neighbours_dict = neighbours_dict
        self.x_coordinate = x_coord
        self.y_coordinate = y_coord
    
    # We can allow instances without a neighbour list
    def __init__(self,x_coord,y_coord):
        self.neighbours_dict = {}
        self.x_coordinate = x_coord
        self.y_coordinate = y_coord

    #__________________________ REPRESENTATION ________________________
    def __repr__(self):
        return repr((self.x_coordinate, self.y_coordinate))

    #____________________________ GETTERS AND SETTERS ___________________________________
    def set_neighbours_dict(self,new_neighbours_dict):
        self.neighbours_dict = new_neighbours_dict

    def get_neighbours_dict(self):
        return self.neighbours_dict

    def get_x_coordinate(self):
        return self.x_coordinate

    def get_y_coordinate(self):
        return self.y_coordinate
      


class MeetingPoint(Node):
    #____________________________________________CLASS CONSTRUCTOR ______________________________________
    def __init__(self, x_coord, y_coord):
        super().__init__(x_coord, y_coord)



class Station(MeetingPoint):

    #___________________________________________ CLASS CONSTRUCTOR______________________________________________
    def __init__(self, x_coord, y_coord,trains_list):
        super().__init__(x_coord, y_coord)
        self.trains_list = trains_list
    
    # we allow a constructor with empty trains_dict
    def __init__(self, x_coord, y_coord):
        super().__init__(x_coord, y_coord)

    #____________________________________________GETTERS AND SETTERS__________________________________
    def get_trains_list(self):
        return self.trains_list
    
    def set_trains_list(self,new_trains_list):
        self.trains_list = new_trains_list
    
    #__________________________________________ADD A TRAIN TO THE STATION___________________________
    def add_to_trains_list(self,new_train):

        # Check if we're adding a train instance
        if(type(new_train).__name__ == "Train"):
            self.trains_list.append(new_train)
        else:
            sys.out("You must add objects of type Train to the list of trains of a station")
    

class Graph:
    
    #____________________________CONSTRUCTOR CLASSES _______________________________________
    def __init__(self,node_list):
        self.node_list = node_list
    
    def __init__(self):
        self.node_list = []

    #_____________________________ GETTERS AND SETTERS ___________________________________
    def get_node_list(self):
        return self.node_list
    
    def set_node_list(self,new_node_list):
        for item in new_node_list:
            if(type(new_node_list).__name__ != "Node"):
                sys.out("the attribute node_list is a list of nodes")
        self.node_list = new_node_list
    
    #_________________________________ GRAPH METHODS____________________________________
    def add_node(self,Node):
        if(type(Node).__name__ == "Node"):
            self.node_list.append(Node)
        else :
            sys.out("Tried adding a non Node object to node_list")
    
    def remove_node(self,Node):
        if(Node in self.node_list):
            self.node_list.remove(Node)
        else :
            print(" Tried deleting a node that isn't in the graph")
    
    def get_distance(self,Node1,Node2):
        return( np.sqrt(Node1.get_y_coord()-Node2.get_y_coord()))
        



