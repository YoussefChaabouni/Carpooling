


from graphClasses import Graph, Node
from meansClasses import Foot, Car, Train


def walk(d:Node,m:Node,G:Graph,speed:float):

	distance = G.get_distance(d,m)
	return distance/speed
    
def Drive(a:Node,b:Node,G:Graph,speed:float):
    distance = G.get_distance(a,b)
    return distance/speed

def board_train(a:Node,b:Node,G:Graph,speed:float):
    distance = G.get_distance(a,b)
    return distance/speed
    
