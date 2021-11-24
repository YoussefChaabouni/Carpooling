


from new_code.graphClasses import Graph, Node
from new_code.meansClasses import Foot, Car, Train


def walk(d:Node,m:Node):

	distance = Graph.get_distance(d,m)
	speed = Foot.get_speed()
	return distance/speed
    
def Drive(a:Node,b:Node):
    distance = Graph.get_distance(a,b)
    speed = Car.get_speed()
    return distance/speed

def board_train(a:Node,b:Node):
    distance = Graph.get_distance(a,b)
    speed = Train.get_speed()
    return distance/speed
    
