import numpy as np

def algorithm_2(z,z_prime,t,driver,m,m_prime):

	t_prime = wt = wd = np.inf

	"""for m_prime_prime in driver.journey(m,m_prime):  # PARTIE DE L'ALGO INCOMPREHENSIBLE
					if driver.available_places(m_prime_prime) <= 0:
						return t_prime
	"""

	# VERIFICATION DE LA CAPACITE DE LA VOITURE EN m

	t_prime = t + walk(z,m)

	wd = distance(z,m)

	if t_prime > d.time(m): # le rider arrive après que le driver soit partie
		return None
	else:


