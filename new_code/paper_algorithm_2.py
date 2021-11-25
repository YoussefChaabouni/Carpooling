
'''
define walk function
inputs : node1,node2
outputs : walking_time
'''
from new_code.PersonClasses import Driver, Rider
from new_code.graphClasses import Graph, MeetingPoint, Node
from new_code.meansClasses import Foot
import numpy as np
from new_code.helperFunctions import walk

def algorithm_2(z:Node,z_prime:Node,t:int,d:Driver,m_board:Node,m_out:Node,graph:Graph):


	# initialise to infinity
	t_arrivee = np.inf
	t_waiting = np.inf
	walk_distance = np.inf

	# check if there is a seat available
	idx_board = d.get_journey.index(m_board.get_id())
	idx_out = d.get_journey.index(m_out.get_id())

	# check the capacity in all stops between m_board and m_out
	for i in range(idx_board,idx_out):
		if d.max_capacity - d.get_current_capacity[i] <= 0:
			return
	
	# update d current capacity for the nodes where the rider will go
	for i in range(idx_board,idx_out):
		d.current_capacity[i] += 1

	


	t_prime = t + walk(z,m_board)
	walk_distance = Graph.get_distance(z,m_board)

	time_index = d.get_trajectory.node_list.index(m_board)
	if t_prime > d.get_trajectory.dep_time[time_index]:
		# the rider is gonna be late
		return
	else :
		t_waiting = d.get_trajectory.dep_time[time_index]

		time_index = d.get_trajectory.node_list.index(m_out)
		t_prime = d.get_trajectory.arr_time[time_index]

		walk_distance += Graph.get_distance(m_out,z_prime)
		t_prime += walk(m_out,z_prime)

	return t_prime,t_waiting,walk_distance