import numpy as np

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
		if  distance(m_org_d,s_org_d) + distance(s_org_d,m_dst_d) <= 1.15 * distance(m_org_d,m_dst_d):
			# Add a detour through station s_org_d
			J_d = [org_d, m_org_d, s_org_d, m_dst_d, dst_d]
			if distance(m_org_d,s_org_d) + distance(s_org_d,s_dst_d) + distance(s_org_d,m_dst_d) <= 1.15 * distance(m_org_d,m_dst_d):
				# Also add a detour through the station close to the driver destination
				J_d = [org_d, m_org_d, s_org_d, s_dst_d, m_dst_d, dst_d]
	else:
		# Try to add a detour close to the destination
		if  distance(m_org_d,s_dst_d) + distance(s_dst_d,m_dst_d) <= 1.15 * distance(m_org_d,m_dst_d):
			# Add a detour through station s_dst_d
			J_d = [org_d, m_org_d, s_dst_d, m_dst_d, dst_d]
			if distance(m_org_d,s_org_d) + distance(s_org_d,s_dst_d) + distance(s_org_d,m_dst_d) <= 1.15 * distance(m_org_d,m_dst_d):
				# Also add a detour through the station close to the driver origin
				J_d = [org_d, m_org_d, s_org_d, s_dst_d, m_dst_d, dst_d]

	return J_d