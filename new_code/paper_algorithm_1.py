import numpy as np
from Carpooling.new_code.PersonClasses import Driver, Rider
from Carpooling.new_code.graphClasses import Graph, MeetingPoint, Node
from Carpooling.new_code.meansClasses import Foot
import graphClasses

def distance(a,b):
	# calcul la distance euclidienne entre deux points de coordonnées 'a' et 'b'
	return np.linalg.norm(np.array(a)-np.array(b))

def algorithm_1(m_org_d,m_dst_d, s_org_d,s_dst_d, org_d,dst_d, t_start):

	"""
	Inputs :
		m_org_d, m_dst_d, ... : positions [x,y]
		t_start : time in seconds
	Outputs :
		J_d : trajectory
	"""

	J_d = [org_d, m_org_d, m_dst_d, dst_d]

	r = np.random.randint(2)

	if r:
		# Try to add a detour close to the origin
		if  distance(m_org_d,s_org_d) + distance(s_org_d,m_dst_d) > 1.15 * distance(m_org_d,m_dst_d):
			# Add a detour through station s_org_d
			J_d = [org_d, m_org_d, s_org_d, m_dst_d, dst_d]
			if distance(m_org_d,s_org_d) + distance(s_org_d,s_dst_d) + distance(s_org_d,m_dst_d) > 1.15 * distance(m_org_d,m_dst_d):
				# Also add a detour through the station close to the driver destination
				J_d = [org_d, m_org_d, s_org_d, s_dst_d, m_dst_d, dst_d]
	else:
		# Try to add a detour close to the destination
		if  distance(m_org_d,s_dst_d) + distance(s_dst_d,m_dst_d) > 1.15 * distance(m_org_d,m_dst_d):
			# Add a detour through station s_dst_d
			J_d = [org_d, m_org_d, s_dst_d, m_dst_d, dst_d]
			if distance(m_org_d,s_org_d) + distance(s_org_d,s_dst_d) + distance(s_org_d,m_dst_d) > 1.15 * distance(m_org_d,m_dst_d):
				# Also add a detour through the station close to the driver origin
				J_d = [org_d, m_org_d, s_org_d, s_dst_d, m_dst_d, dst_d]

	return J_d


# define walk function


'''
define walk function
inputs : node1,node2
outputs : walking_time
'''
def walk(d:Node,m:Node):

	distance = Graph.get_distance(d,m)
	speed = Foot.get_speed
	return distance/speed


def algorithm_2(rider: Rider,d: Driver,m_board: MeetingPoint,m_out: MeetingPoint):

	z = rider.get_pos_depart
	z_prime = rider.get_pos_arrivee
	t = rider.get_born_time

	# initialise to infinity
	t_arrivee = float('inf')
	t_waiting = float("inf")
	walk_distance = float("inf")

	# check if there is a seat available
	idx_board = d.get_journey.index(m_board)
	idx_out = d.get_journey.index(m_out)

	# check the capacity in all stops between m_board and m_out
	for i in range(idx_board,idx_out):
		if d.max_capacity - d.get_current_capacity[i] <= 0:
			return
	
	t_prime = t + walk(z,m_board)
	walk_distance = Graph.get_distance(z,m_board)

	##'''if t_prime > d.get_trajectory.get_trajectory_list




	return 0