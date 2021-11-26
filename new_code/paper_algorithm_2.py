
from PersonClasses import Driver, Rider
from graphClasses import Graph, MeetingPoint, Node
from helperFunctions import walk
import numpy as np

def algorithm_2(z,z_prime,t, d:Driver, m_board:MeetingPoint, m_out:MeetingPoint, graph:Graph):

	#z = rider.pos_depart
	#print("type(z) = ",type(z))
	#z_prime = rider.pos_arrivee
	#t = rider.get_born_time()

	# initialise to infinity
	t_arrivee = np.inf
	t_waiting = np.inf
	walk_distance = np.inf

	# check if there is a seat available
	idx_board = d.get_trajectory().node_id_list.index(m_board)
	idx_out = d.get_trajectory().node_id_list.index(m_out)

	print(z=="MP0")
	print(graph.get_node(z))

	# check the capacity in all stops between m_board and m_out
	for i in range(idx_board,idx_out):
		if d.get_current_capacity()[i] <= 0:
			print( "pas assez de place dans la voiture")
	
	t_prime = t + walk(graph.get_node(z),graph.get_node(m_board),graph,5)
	walk_distance = graph.get_distance(graph.get_node(z),graph.get_node(m_board))
	
	
	
	time_index = d.get_trajectory().node_id_list.index(m_board)
	if t_prime > d.get_trajectory().arr_time_list[time_index]:
		# the rider is gonna be late
		print("the rider arrives at ",t_prime," but the driver leaves at : ",d.get_trajectory().dep_time_list[time_index])
	else :
		print("the rider takes a car with driver ",d.get_id())
		t_waiting = d.get_trajectory().arr_time_list[time_index] - t_prime

		time_index = d.get_trajectory().node_id_list.index(m_out)
		t_prime = d.get_trajectory().arr_time_list[time_index]

		walk_distance += graph.get_distance(graph.get_node(m_out),graph.get_node(z_prime))
		t_prime += walk(graph.get_node(m_out),graph.get_node(z_prime),graph,5)

	return t_prime,t_waiting,walk_distance