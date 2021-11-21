import numpy as np


def argmin_distance_user_MP(users_x_y,MPs_x_y):

	"""
	Input :
		users_x_y : coordinates XY of users on the map
		MPs_x_y : coordinates XY of Meeting Points on the map

	Output :
		argmin_distance : array of argmin distance between users and MPs
	"""

	u_x,mp_x = np.meshgrid(users_x_y[:,0],MPs_x_y[:,0])
	u_y,mp_y = np.meshgrid(users_x_y[:,1],MPs_x_y[:,1])


	argmin_distance = np.argmin((u_x-mp_x)**2 + (u_y-mp_y)**2,axis=0)

	return argmin_distance