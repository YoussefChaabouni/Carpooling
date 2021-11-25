
from PersonClasses import Driver, Rider
from graphClasses import Graph, MeetingPoint, Node
from helperFunctions import walk
import numpy as np

def algorithm_2(rider:Rider,d:Driver, m_board:MeetingPoint, m_out:MeetingPoint, graph:Graph):

	z = rider.get_pos_depart()
	z_prime = rider.get_pos_arrivee()
	t = rider.get_born_time()

	# initialise to infinity
	t_arrivee = np.inf
	t_waiting = np.inf
	walk_distance = np.inf

	# check if there is a seat available
	idx_board = d.get_journey().index(m_board)
	idx_out = d.get_journey().index(m_out)

	# check the capacity in all stops between m_board and m_out
	for i in range(idx_board,idx_out):
		if d.max_capacity - d.get_current_capacity()[i] <= 0:
			return
	
	t_prime = t + walk(z,m_board)
	walk_distance = graph.get_distance(z,m_board)

	time_index = d.get_trajectory().node_list.index(m_board)
	if t_prime > d.get_trajectory().dep_time[time_index]:
		# the rider is gonna be late
		return
	else :
		t_waiting = d.get_trajectory().dep_time[time_index]

		time_index = d.get_trajectory().node_list.index(m_out)
		t_prime = d.get_trajectory().arr_time[time_index]

		walk_distance += graph.get_distance(m_out,z_prime)
		t_prime += walk(m_out,z_prime)

	return t_prime,t_waiting,walk_distance